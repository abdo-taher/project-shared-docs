#!/usr/bin/env python3
"""Semantic OpenAPI contract compatibility analysis (Capitalix contract CI/CD v4).

Compares a baseline OpenAPI 3.x document (the approved/committed contract)
with a candidate document (the current generation) and classifies every
difference:

  BREAKING            consumers can break (removed/changed responses, newly
                      required inputs, removed accepted inputs, auth changes,
                      operationId changes that rename SDK methods, ...)
  NON_BREAKING        safe additive changes (new operations, new optional
                      inputs, new response fields, widened request values, ...)

Requests and responses are judged by one rule: a narrower set of accepted
values breaks requests and is safe for responses; a wider set is the reverse
(e.g. null newly returned, or a response field that became optional, is
BREAKING). A schema shared by requests and responses breaks either way.
  DOCUMENTATION_ONLY  text/metadata/deprecation-marking changes that do not
                      change the runtime contract
  UNKNOWN             a difference the classifier cannot definitively
                      interpret (oneOf rewrites, allOf/anyOf member-count
                      changes, unrecognized keywords, unresolvable $refs, ...)

UNKNOWN is never treated as safe. When a definitive compatibility decision
is required (--fail-on-unknown), any UNKNOWN fails the run (exit 2).
Breaking changes fail only with --fail-on-breaking (exit 1).

Shared components are diffed with transitive $ref resolution: a changed
component lists every operation reachable from it, so the blast radius of a
shared-schema edit is part of the report.

Outputs: machine-readable JSON (--json-out) and human-readable Markdown
(--markdown-out). The tool never modifies either document.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from typing import Any, Callable

BREAKING = "BREAKING"
NON_BREAKING = "NON_BREAKING"
DOCUMENTATION_ONLY = "DOCUMENTATION_ONLY"
UNKNOWN = "UNKNOWN"

_SEVERITY = {BREAKING: 3, UNKNOWN: 2, NON_BREAKING: 1, DOCUMENTATION_ONLY: 0}

HTTP_METHODS = ("get", "put", "post", "delete", "options", "head", "patch", "trace")

# Operation-object keywords with a dedicated handler; anything else that
# differs and has no handler becomes UNKNOWN (never silently safe).
OPERATION_KEYWORDS_WITH_HANDLERS = {
    "tags", "summary", "description", "externalDocs", "operationId",
    "parameters", "requestBody", "responses", "callbacks", "deprecated",
    "security", "servers",
}

# Schema keywords the classifier interprets. Any *other* schema keyword that
# differs falls through to UNKNOWN.
SCHEMA_KEYWORDS_INTERPRETED = {
    "type", "format", "properties", "required", "items", "enum", "const",
    "additionalProperties", "description", "summary", "title", "default",
    "example", "examples", "nullable", "deprecated", "readOnly", "writeOnly",
    "$ref", "$comment", "discriminator", "xml", "externalDocs", "allOf",
    "oneOf", "anyOf", "not",
    "minLength", "maxLength", "minItems", "maxItems", "minProperties",
    "maxProperties", "minimum", "maximum", "pattern",
}

# Numeric bounds: an absent bound is the loosest one (0 for counts, unbounded
# for minimum/maximum). Non-numeric values fall through to UNKNOWN.
LOWER_BOUNDS = {"minLength": 0, "minItems": 0, "minProperties": 0, "minimum": float("-inf")}
UPPER_BOUNDS = {"maxLength": float("inf"), "maxItems": float("inf"),
                "maxProperties": float("inf"), "maximum": float("inf")}

NULL_SCHEMA = {"type": "null"}

DOC_ONLY_SCHEMA_KEYS = {"description", "summary", "title", "example", "examples",
                        "$comment", "xml", "externalDocs", "default", "deprecated"}


def severity_max(*categories: str) -> str:
    return max(categories, key=lambda c: _SEVERITY[c])


def value_set_category(narrowed: bool, direction: str) -> str:
    """A narrower accepted value set breaks requests (clients may send what is
    now rejected) and is safe for responses; a wider one is the reverse. A
    schema shared by requests and responses breaks either way."""
    if direction == "both":
        return BREAKING
    if direction == "request":
        return BREAKING if narrowed else NON_BREAKING
    return NON_BREAKING if narrowed else BREAKING


class RefResolver:
    """Resolves local `#/...` JSON pointers inside one document."""

    def __init__(self, document: dict):
        self.document = document

    def resolve(self, ref: str) -> Any:
        if not isinstance(ref, str) or not ref.startswith("#/"):
            raise KeyError(f"external or malformed $ref: {ref!r}")
        node: Any = self.document
        for segment in ref[2:].split("/"):
            segment = segment.replace("~1", "/").replace("~0", "~")
            if not isinstance(node, dict) or segment not in node:
                raise KeyError(f"unresolvable $ref: {ref}")
            node = node[segment]
        return node

    def deref(self, schema: Any) -> Any:
        """Follows a single-level $ref (chains resolved iteratively)."""
        seen = set()
        while isinstance(schema, dict) and "$ref" in schema:
            ref = schema["$ref"]
            if ref in seen:
                raise KeyError(f"circular $ref: {ref}")
            seen.add(ref)
            schema = self.resolve(ref)
        return schema


class Change:
    def __init__(self, category: str, kind: str, location: str,
                 description: str, before: Any = None, after: Any = None,
                 path: str | None = None, method: str | None = None,
                 affected_operations: list[str] | None = None):
        self.category = category
        self.kind = kind
        self.location = location
        self.description = description
        self.before = before
        self.after = after
        self.path = path
        self.method = method
        self.affected_operations = affected_operations or []

    def to_dict(self) -> dict:
        d = {
            "category": self.category,
            "kind": self.kind,
            "location": self.location,
            "description": self.description,
        }
        if self.path is not None:
            d["path"] = self.path
        if self.method is not None:
            d["method"] = self.method
        if self.before is not None:
            d["before"] = self.before
        if self.after is not None:
            d["after"] = self.after
        if self.affected_operations:
            d["affected_operations"] = self.affected_operations[:50]
            d["affected_operations_count"] = len(self.affected_operations)
        return d


class SchemaDiffer:
    """Context-aware recursive schema comparison.

    direction: "request" | "response" | "both".
    A callback `emit(change)` receives classified differences.
    """

    def __init__(self, baseline_resolver: RefResolver, candidate_resolver: RefResolver,
                 emit: Callable[[Change], None]):
        self.baseline_resolver = baseline_resolver
        self.candidate_resolver = candidate_resolver
        self.emit = emit

    # ------------------------------------------------------------------ util
    @staticmethod
    def _type_set(schema: dict) -> set[str]:
        t = schema.get("type")
        if t is None:
            return set()
        if isinstance(t, str):
            return {t}
        if isinstance(t, list) and all(isinstance(x, str) for x in t):
            return set(t)
        return set()

    def _resolve_pair(self, base: Any, cand: Any, loc: str) -> tuple[Any, Any, str | None]:
        """Dereferences both sides; returns (base, cand, note)."""
        note = None
        base_ref = base.get("$ref") if isinstance(base, dict) else None
        cand_ref = cand.get("$ref") if isinstance(cand, dict) else None
        try:
            if base_ref and cand_ref and base_ref == cand_ref:
                return self.baseline_resolver.deref(base), self.candidate_resolver.deref(cand), "same_ref"
            if base_ref or cand_ref:
                note = "ref_shape_changed"
            return self.baseline_resolver.deref(base), self.candidate_resolver.deref(cand), note
        except KeyError as exc:
            raise UnresolvableRef(f"{loc}: {exc}") from exc

    # ------------------------------------------------------------- main entry
    def diff(self, base: Any, cand: Any, loc: str, direction: str,
             kind_prefix: str = "schema") -> None:
        try:
            base_r, cand_r, note = self._resolve_pair(base, cand, loc)
        except UnresolvableRef as exc:
            self.emit(Change(UNKNOWN, f"{kind_prefix}_unresolvable_ref", loc,
                             f"cannot resolve $ref for comparison: {exc}",
                             before=_brief(base), after=_brief(cand)))
            return

        try:
            base_r = self._collapse_nullable_any_of(base_r, self.baseline_resolver)
            cand_r = self._collapse_nullable_any_of(cand_r, self.candidate_resolver)
        except KeyError as exc:
            self.emit(Change(UNKNOWN, f"{kind_prefix}_unresolvable_ref", loc,
                             f"cannot resolve $ref for comparison: {loc}: {exc}",
                             before=_brief(base), after=_brief(cand)))
            return

        if base_r == cand_r:
            return

        if not isinstance(base_r, dict) or not isinstance(cand_r, dict):
            if type(base_r) is not type(cand_r) or base_r != cand_r:
                self.emit(Change(BREAKING, f"{kind_prefix}_changed", loc,
                                 "schema value changed incompatibly",
                                 before=_brief(base_r), after=_brief(cand_r)))
            return

        if note == "ref_shape_changed":
            self.emit(Change(DOCUMENTATION_ONLY, f"{kind_prefix}_reference_shape", loc,
                             "schema moved between $ref and inline definition (same effective shape)",
                             before=_brief(base), after=_brief(cand)))

        self._diff_object_schema(base_r, cand_r, loc, direction, kind_prefix)

    @staticmethod
    def _collapse_nullable_any_of(schema: Any, resolver: RefResolver) -> Any:
        """`anyOf: [X, {type: null}]` is the OpenAPI 3.1 spelling of a nullable
        X. Returns X with null admitted (in `type`, and in `enum` when X is an
        enum) so it compares against the inline `type: [.., "null"]` form.
        Anything else is returned unchanged."""
        if not isinstance(schema, dict):
            return schema
        members = schema.get("anyOf")
        if (not isinstance(members, list) or len(members) != 2
                or members.count(NULL_SCHEMA) != 1
                or set(schema) - {"anyOf"} - DOC_ONLY_SCHEMA_KEYS):
            return schema
        target = resolver.deref(members[1] if members[0] == NULL_SCHEMA else members[0])
        if (not isinstance(target, dict) or not isinstance(target.get("type"), (str, list))
                or {"allOf", "oneOf", "anyOf", "not", "const"} & set(target)):
            return schema
        types = target["type"] if isinstance(target["type"], list) else [target["type"]]
        collapsed = {**target, **{k: v for k, v in schema.items() if k != "anyOf"}}
        collapsed["type"] = types + ([] if "null" in types else ["null"])
        if isinstance(target.get("enum"), list) and None not in target["enum"]:
            collapsed["enum"] = target["enum"] + [None]
        return collapsed

    def _diff_object_schema(self, b: dict, c: dict, loc: str, direction: str,
                            kind_prefix: str) -> None:
        # type ----------------------------------------------------------------
        b_types, c_types = self._type_set(b), self._type_set(c)
        if b_types != c_types or ("type" in b) != ("type" in c):
            self._classify_type_change(b, c, b_types, c_types, loc, direction, kind_prefix)

        # format --------------------------------------------------------------
        if b.get("format") != c.get("format"):
            if b.get("format") is None or c.get("format") is None:
                # Adding a format narrows the documented values (and typed SDKs
                # switch to e.g. DateTime); removing one widens them.
                added = b.get("format") is None
                self.emit(Change(value_set_category(added, direction),
                                 f"{kind_prefix}_format_{'added' if added else 'removed'}", loc,
                                 f"format changed ({b.get('format')!r} -> {c.get('format')!r})",
                                 before=b.get("format"), after=c.get("format")))
            else:
                self.emit(Change(BREAKING, f"{kind_prefix}_format_changed", loc,
                                 f"format changed ({b.get('format')!r} -> {c.get('format')!r})",
                                 before=b.get("format"), after=c.get("format")))

        # enum ----------------------------------------------------------------
        self._diff_enum(b, c, loc, direction, kind_prefix)

        # bounds and pattern ---------------------------------------------------
        self._diff_constraints(b, c, loc, direction, kind_prefix)

        # const ---------------------------------------------------------------
        if b.get("const") != c.get("const") and ("const" in b or "const" in c):
            self.emit(Change(BREAKING, f"{kind_prefix}_const_changed", loc,
                             "const constraint changed",
                             before=_brief(b.get("const")), after=_brief(c.get("const"))))

        # properties / required ----------------------------------------------
        self._diff_properties(b, c, loc, direction, kind_prefix)

        # items ---------------------------------------------------------------
        if "items" in b or "items" in c:
            if "items" not in b or "items" not in c:
                self.emit(Change(BREAKING, f"{kind_prefix}_items_changed", loc,
                                 "array items schema removed or added",
                                 before="items" in b, after="items" in c))
            else:
                self.diff(b["items"], c["items"], loc + ".items", direction, kind_prefix)

        # additionalProperties ------------------------------------------------
        def _ap_normalized(schema: dict) -> Any:
            ap = schema.get("additionalProperties", True)
            # `{}` (empty schema) permits anything, same as `true`.
            return True if ap == {} else ap

        if _ap_normalized(b) != _ap_normalized(c):
            bp, cp = _ap_normalized(b), _ap_normalized(c)
            disabling = bp in (True,) and cp is False
            enabling = bp is False and cp in (True,)
            if disabling:
                self.emit(Change(BREAKING, f"{kind_prefix}_additional_properties_disabled", loc,
                                 "additionalProperties: false now rejects extra properties",
                                 before=bp, after=cp))
            elif enabling:
                self.emit(Change(NON_BREAKING, f"{kind_prefix}_additional_properties_enabled", loc,
                                 "additionalProperties now accepts extra properties",
                                 before=bp, after=cp))
            else:
                self.diff(bp, cp, loc + ".additionalProperties", direction, kind_prefix)

        # compositions --------------------------------------------------------
        # allOf/anyOf lists of the same length are compared member by member:
        # an intersection (allOf) or union (anyOf) of members that each got
        # narrower is narrower, and of members that each got wider is wider, so
        # the per-member classification carries over. oneOf is not monotone
        # (widening a member can make a value match two), and a changed member
        # count has no pairing: both stay UNKNOWN.
        for comp in ("allOf", "oneOf", "anyOf"):
            if b.get(comp) != c.get(comp):
                b_list, c_list = b.get(comp), c.get(comp)
                if (comp != "oneOf" and isinstance(b_list, list) and isinstance(c_list, list)
                        and len(b_list) == len(c_list)):
                    for i, (b_member, c_member) in enumerate(zip(b_list, c_list)):
                        if (isinstance(b_member, dict) and isinstance(c_member, dict)
                                and b_member.get("$ref") and b_member == c_member):
                            continue  # shared-component change is reported at component level
                        self.diff(b_member, c_member, f"{loc}.{comp}[{i}]", direction, kind_prefix)
                    continue
                if b.get(comp) is None or c.get(comp) is None:
                    self.emit(Change(UNKNOWN, f"{kind_prefix}_{comp}_changed", loc,
                                     f"{comp} composition added or removed",
                                     before=_brief(b.get(comp)), after=_brief(c.get(comp))))
                else:
                    self.emit(Change(UNKNOWN, f"{kind_prefix}_{comp}_changed", loc,
                                     f"{comp} composition changed (unclassified rewrite)",
                                     before=_brief(b.get(comp)), after=_brief(c.get(comp))))
        if b.get("not") != c.get("not"):
            self.emit(Change(UNKNOWN, f"{kind_prefix}_not_changed", loc,
                             "'not' composition changed", before=_brief(b.get("not")),
                             after=_brief(c.get("not"))))
        if b.get("discriminator") != c.get("discriminator"):
            self.emit(Change(UNKNOWN, f"{kind_prefix}_discriminator_changed", loc,
                             "discriminator changed", before=_brief(b.get("discriminator")),
                             after=_brief(c.get("discriminator"))))

        # nullable (3.0 style) ------------------------------------------------
        if bool(b.get("nullable")) != bool(c.get("nullable")):
            added = bool(c.get("nullable"))
            self.emit(Change(
                value_set_category(not added, direction),
                f"{kind_prefix}_nullable_changed", loc,
                "nullable " + ("added" if added else "removed"),
                before=bool(b.get("nullable")), after=bool(c.get("nullable"))))

        # readOnly / writeOnly ------------------------------------------------
        for flag in ("readOnly", "writeOnly"):
            if bool(b.get(flag)) != bool(c.get(flag)):
                self.emit(Change(UNKNOWN, f"{kind_prefix}_{flag}_changed", loc,
                                 f"{flag} changed", before=bool(b.get(flag)),
                                 after=bool(c.get(flag))))

        # everything else -----------------------------------------------------
        for key in set(b) | set(c):
            if key in SCHEMA_KEYWORDS_INTERPRETED or key in DOC_ONLY_SCHEMA_KEYS:
                continue
            if b.get(key) != c.get(key):
                self.emit(Change(UNKNOWN, f"{kind_prefix}_keyword_changed", loc,
                                 f"unrecognized schema keyword [{key}] changed",
                                 before=_brief(b.get(key)), after=_brief(c.get(key))))

        # documentation-only leftovers ----------------------------------------
        for key in DOC_ONLY_SCHEMA_KEYS:
            if b.get(key) != c.get(key):
                self.emit(Change(DOCUMENTATION_ONLY, f"{kind_prefix}_documentation", loc,
                                 f"{key} changed", before=_brief(b.get(key)),
                                 after=_brief(c.get(key))))

    def _diff_constraints(self, b: dict, c: dict, loc: str, direction: str,
                          kind_prefix: str) -> None:
        for key, loosest in {**LOWER_BOUNDS, **UPPER_BOUNDS}.items():
            bv, cv = b.get(key), c.get(key)
            if bv == cv:
                continue
            if not all(v is None or (isinstance(v, (int, float)) and not isinstance(v, bool))
                       for v in (bv, cv)):
                self.emit(Change(UNKNOWN, f"{kind_prefix}_keyword_changed", loc,
                                 f"unrecognized schema keyword [{key}] changed",
                                 before=_brief(bv), after=_brief(cv)))
                continue
            be = loosest if bv is None else bv
            ce = loosest if cv is None else cv
            if be == ce:
                self.emit(Change(DOCUMENTATION_ONLY, f"{kind_prefix}_constraint_restated", loc,
                                 f"[{key}] {bv!r} -> {cv!r} (same effective bound)",
                                 before=bv, after=cv))
                continue
            narrowed = ce > be if key in LOWER_BOUNDS else ce < be
            self.emit(Change(value_set_category(narrowed, direction),
                             f"{kind_prefix}_constraint_{'narrowed' if narrowed else 'widened'}", loc,
                             f"[{key}] {bv!r} -> {cv!r}", before=bv, after=cv))

        bp, cp = b.get("pattern"), c.get("pattern")
        if bp != cp:
            if bp is not None and cp is not None:
                # Two regular expressions cannot be compared for inclusion.
                self.emit(Change(BREAKING, f"{kind_prefix}_pattern_changed", loc,
                                 "pattern replaced (inclusion cannot be proven)",
                                 before=bp, after=cp))
            else:
                narrowed = bp is None
                self.emit(Change(value_set_category(narrowed, direction),
                                 f"{kind_prefix}_pattern_{'added' if narrowed else 'removed'}", loc,
                                 f"pattern {'added' if narrowed else 'removed'}",
                                 before=bp, after=cp))

    def _classify_type_change(self, b: dict, c: dict, b_types: set[str], c_types: set[str],
                              loc: str, direction: str, kind_prefix: str) -> None:
        # An absent `type` admits every type, so adding one narrows the value
        # set and removing one widens it.
        if "type" not in b or "type" not in c:
            added = "type" not in b
            self.emit(Change(value_set_category(added, direction),
                             f"{kind_prefix}_type_{'added' if added else 'removed'}", loc,
                             f"type {'added' if added else 'removed'} "
                             f"({sorted(b_types) or 'any'} -> {sorted(c_types) or 'any'})",
                             before=sorted(b_types), after=sorted(c_types)))
            return
        added, removed = c_types - b_types, b_types - c_types
        if added == {"null"} and not removed:
            # request: null newly accepted -> NON_BREAKING
            # response: null may now reach clients that never received it -> BREAKING
            self.emit(Change(value_set_category(False, direction),
                             f"{kind_prefix}_nullability_added", loc,
                             "type now also accepts/returns null",
                             before=sorted(b_types), after=sorted(c_types)))
            return
        if removed == {"null"} and not added:
            # request: clients may still send null -> server got stricter: BREAKING
            # response: null no longer returned -> clients may handle it: NON_BREAKING
            self.emit(Change(value_set_category(True, direction),
                             f"{kind_prefix}_nullability_removed", loc,
                             "type no longer accepts/returns null",
                             before=sorted(b_types), after=sorted(c_types)))
            return
        if b_types and c_types and not added:
            category = value_set_category(True, direction)
        elif b_types and c_types and not removed:
            category = value_set_category(False, direction)
        else:
            category = BREAKING
        self.emit(Change(category, f"{kind_prefix}_type_changed", loc,
                         f"type changed ({sorted(b_types)} -> {sorted(c_types)})",
                         before=sorted(b_types), after=sorted(c_types)))

    def _diff_enum(self, b: dict, c: dict, loc: str, direction: str,
                   kind_prefix: str) -> None:
        b_enum, c_enum = b.get("enum"), c.get("enum")
        if b_enum == c_enum:
            return
        if b_enum is None and c_enum is None:
            return
        if b_enum is None or c_enum is None:
            # No enum means any value of the type: adding one narrows, removing widens.
            added = b_enum is None
            self.emit(Change(value_set_category(added, direction),
                             f"{kind_prefix}_enum_{'added' if added else 'removed'}", loc,
                             "enum constraint " + ("added" if added else "removed"),
                             before=_brief(b_enum), after=_brief(c_enum)))
            return
        b_set = set(map(json.dumps, b_enum))
        c_set = set(map(json.dumps, c_enum))
        lost, gained = b_set - c_set, c_set - b_set
        if direction == "request":
            if lost:
                self.emit(Change(BREAKING, f"{kind_prefix}_enum_value_removed", loc,
                                 "previously accepted enum value no longer accepted",
                                 before=sorted(lost), after=None))
            if gained:
                self.emit(Change(NON_BREAKING, f"{kind_prefix}_enum_value_added", loc,
                                 "newly accepted enum value", before=None, after=sorted(gained)))
        else:  # response / both
            if gained:
                self.emit(Change(BREAKING, f"{kind_prefix}_enum_value_added", loc,
                                 "response may now contain a value clients do not handle",
                                 before=None, after=sorted(gained)))
            if lost:
                self.emit(Change(NON_BREAKING, f"{kind_prefix}_enum_value_removed", loc,
                                 "response no longer contains a previously possible value",
                                 before=sorted(lost), after=None))

    def _diff_properties(self, b: dict, c: dict, loc: str, direction: str,
                         kind_prefix: str) -> None:
        b_props = b.get("properties") if isinstance(b.get("properties"), dict) else {}
        c_props = c.get("properties") if isinstance(c.get("properties"), dict) else {}
        b_req = set(b.get("required") or [])
        c_req = set(c.get("required") or [])

        for name in sorted(set(b_props) | set(c_props)):
            ploc = f"{loc}.properties.{name}"
            in_b, in_c = name in b_props, name in c_props

            if in_b and not in_c:
                self.emit(Change(BREAKING, f"{kind_prefix}_field_removed", ploc,
                                 f"field [{name}] removed", before=_brief(b_props[name])))
                continue
            if in_c and not in_b:
                # A new required field narrows the accepted objects: requests that
                # omit it are now rejected, responses now always carry it.
                if name in c_req:
                    self.emit(Change(value_set_category(True, direction),
                                     f"{kind_prefix}_required_field_added", ploc,
                                     f"new REQUIRED field [{name}]",
                                     after=_brief(c_props[name])))
                else:
                    self.emit(Change(NON_BREAKING, f"{kind_prefix}_field_added", ploc,
                                     f"new optional field [{name}]",
                                     after=_brief(c_props[name])))
                continue

            was_req, is_req = name in b_req, name in c_req
            if not was_req and is_req:
                self.emit(Change(value_set_category(True, direction),
                                 f"{kind_prefix}_field_became_required", ploc,
                                 f"field [{name}] became required",
                                 before={"required": False}, after={"required": True}))
            elif was_req and not is_req:
                self.emit(Change(value_set_category(False, direction),
                                 f"{kind_prefix}_field_became_optional", ploc,
                                 f"field [{name}] became optional",
                                 before={"required": True}, after={"required": False}))

            self.diff(b_props[name], c_props[name], ploc, direction, kind_prefix)


class UnresolvableRef(Exception):
    pass


def _brief(value: Any, limit: int = 400) -> Any:
    """Compact a value for the report."""
    try:
        text = json.dumps(value, sort_keys=True, ensure_ascii=False)
    except (TypeError, ValueError):
        return repr(value)[:limit]
    return text[:limit] + ("…" if len(text) > limit else "")


def _operations(document: dict) -> dict[tuple[str, str], dict]:
    ops = {}
    for path, item in (document.get("paths") or {}).items():
        if not isinstance(item, dict):
            continue
        for method, operation in item.items():
            if method in HTTP_METHODS and isinstance(operation, dict):
                ops[(path, method)] = operation
    return ops


def _security_requirements(operation: dict) -> list[frozenset] | None:
    """Canonical form of an operation's security list; None when absent."""
    if "security" not in operation:
        return None
    raw = operation.get("security")
    if not isinstance(raw, list):
        return [frozenset({("<invalid>", ())})]
    result = []
    for requirement in raw:
        if isinstance(requirement, dict):
            result.append(frozenset(
                (scheme, tuple(sorted(map(str, scopes or []))))
                for scheme, scopes in requirement.items()))
        else:
            result.append(frozenset({("<invalid>", ())}))
    return sorted(result, key=lambda r: sorted(r))


def _referrer_components(document: dict) -> dict[str, set[str]]:
    """component pointer ('#/components/schemas/X') -> set of component
    pointers that reference it (inside components only)."""
    graph: dict[str, set[str]] = {}

    components = document.get("components") or {}
    for section, entries in components.items():
        if not isinstance(entries, dict):
            continue
        for name, body in entries.items():
            owner = f"#/components/{section}/{name}"

            def walk_owner(node: Any, owner: str = owner) -> None:
                if isinstance(node, dict):
                    ref = node.get("$ref")
                    if isinstance(ref, str) and ref.startswith("#/components/"):
                        graph.setdefault(ref, set()).add(owner)
                    for value in node.values():
                        walk_owner(value)
                elif isinstance(node, list):
                    for item in node:
                        walk_owner(item)

            walk_owner(body)
    return graph


def _operations_referencing(document: dict, pointer: str, graph: dict[str, set[str]]) -> list[str]:
    """All operations (directly or transitively through components) that use
    the component at `pointer`."""
    # Transitive closure over component refs.
    reachable: set[str] = set()
    frontier = [pointer]
    while frontier:
        current = frontier.pop()
        for owner in graph.get(current, set()):
            if owner not in reachable:
                reachable.add(owner)
                frontier.append(owner)

    result = []
    for (path, method), operation in sorted(_operations(document).items()):
        blob = json.dumps(operation, sort_keys=True)
        direct = f'"$ref":"{pointer}"' in blob.replace(" ", "")
        if direct or any(f'"$ref":"{r}"' in blob.replace(" ", "") for r in reachable):
            result.append(f"{method.upper()} {path}")
    return result


def _reachable_refs(document: dict, nodes: list[Any]) -> set[str]:
    """Every local $ref reachable from the given nodes, following referenced
    components transitively."""
    seen: set[str] = set()
    stack = list(nodes)
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            ref = node.get("$ref")
            if isinstance(ref, str) and ref.startswith("#/") and ref not in seen:
                seen.add(ref)
                try:
                    stack.append(RefResolver(document).resolve(ref))
                except KeyError:
                    pass
            stack.extend(node.values())
        elif isinstance(node, list):
            stack.extend(node)
    return seen


class CompatibilityAnalyzer:
    def __init__(self, baseline: dict, candidate: dict):
        self.baseline = baseline
        self.candidate = candidate
        self.changes: list[Change] = []
        self.baseline_resolver = RefResolver(baseline)
        self.candidate_resolver = RefResolver(candidate)
        self.graph = _referrer_components(baseline)
        self._usage: dict[str, set[str]] | None = None
        self.schema_differ = SchemaDiffer(
            self.baseline_resolver, self.candidate_resolver, self.changes.append)

    # ------------------------------------------------------------------ emit
    def emit(self, change: Change) -> None:
        self.changes.append(change)

    # ------------------------------------------------------------------- run
    def analyze(self) -> list[Change]:
        self._diff_global()
        self._diff_operations()
        self._diff_components()
        self.changes.sort(key=lambda ch: (-_SEVERITY[ch.category], ch.location,
                                          ch.kind, ch.path or "", ch.method or ""))
        return self.changes

    # ---------------------------------------------------------------- global
    def _diff_global(self) -> None:
        b_info, c_info = self.baseline.get("info") or {}, self.candidate.get("info") or {}
        for key in ("title", "version", "description", "contact", "license", "termsOfService"):
            if b_info.get(key) != c_info.get(key):
                self.emit(Change(DOCUMENTATION_ONLY, "info_changed", f"info.{key}",
                                 f"info.{key} changed",
                                 before=_brief(b_info.get(key)), after=_brief(c_info.get(key))))
        if self.baseline.get("openapi") != self.candidate.get("openapi"):
            self.emit(Change(DOCUMENTATION_ONLY, "openapi_version_changed", "openapi",
                             f"OpenAPI version {self.baseline.get('openapi')!r} -> "
                             f"{self.candidate.get('openapi')!r}",
                             before=self.baseline.get("openapi"),
                             after=self.candidate.get("openapi")))
        if self.baseline.get("servers") != self.candidate.get("servers"):
            self.emit(Change(BREAKING, "servers_changed", "servers",
                             "server list changed — clients may be pointed elsewhere",
                             before=_brief(self.baseline.get("servers")),
                             after=_brief(self.candidate.get("servers"))))

    # ------------------------------------------------------------ operations
    def _diff_operations(self) -> None:
        b_ops, c_ops = _operations(self.baseline), _operations(self.candidate)

        for key in sorted(set(b_ops) - set(c_ops)):
            path, method = key
            self.emit(Change(BREAKING, "operation_removed", f"paths.{path}.{method}",
                             f"{method.upper()} {path} removed from the contract",
                             path=path, method=method,
                             before=_brief(b_ops[key], 200)))

        for key in sorted(set(c_ops) - set(b_ops)):
            path, method = key
            self.emit(Change(NON_BREAKING, "operation_added", f"paths.{path}.{method}",
                             f"{method.upper()} {path} added to the contract",
                             path=path, method=method,
                             after=_brief(c_ops[key], 200)))

        for key in sorted(set(b_ops) & set(c_ops)):
            path, method = key
            self._diff_operation(path, method, b_ops[key], c_ops[key])

    def _diff_operation(self, path: str, method: str, b: dict, c: dict) -> None:
        loc = f"paths.{path}.{method}"
        kw: dict[str, Any] = {"path": path, "method": method}

        # operationId -------------------------------------------------------
        if b.get("operationId") != c.get("operationId"):
            self.emit(Change(BREAKING, "operation_id_changed", loc + ".operationId",
                             "operationId changed — generated SDK methods/clients break",
                             before=b.get("operationId"), after=c.get("operationId"), **kw))

        # deprecation -------------------------------------------------------
        b_dep, c_dep = bool(b.get("deprecated")), bool(c.get("deprecated"))
        if b_dep != c_dep:
            self.emit(Change(
                DOCUMENTATION_ONLY if c_dep else NON_BREAKING,
                "operation_deprecated" if c_dep else "operation_undeprecated",
                loc + ".deprecated",
                "operation marked deprecated" if c_dep else "operation no longer deprecated",
                before=b_dep, after=c_dep, **kw))

        # documentation -----------------------------------------------------
        for key in ("summary", "description", "externalDocs"):
            if b.get(key) != c.get(key):
                self.emit(Change(DOCUMENTATION_ONLY, "operation_documentation", loc + "." + key,
                                 f"{key} changed", before=_brief(b.get(key)),
                                 after=_brief(c.get(key)), **kw))
        if b.get("tags") != c.get("tags"):
            self.emit(Change(DOCUMENTATION_ONLY, "operation_tags_changed", loc + ".tags",
                             "tags changed", before=_brief(b.get("tags")),
                             after=_brief(c.get("tags")), **kw))

        # security ----------------------------------------------------------
        self._diff_security(b, c, loc, **kw)

        # parameters --------------------------------------------------------
        self._diff_parameters(b, c, loc, **kw)

        # requestBody -------------------------------------------------------
        self._diff_request_body(b, c, loc, **kw)

        # responses ---------------------------------------------------------
        self._diff_responses(b, c, loc, **kw)

        # residual keywords -------------------------------------------------
        for key in set(b) | set(c):
            if key in OPERATION_KEYWORDS_WITH_HANDLERS:
                continue
            if key.startswith("x-"):
                if b.get(key) != c.get(key):
                    self.emit(Change(DOCUMENTATION_ONLY, "operation_extension_changed",
                                     f"{loc}.{key}", f"vendor extension [{key}] changed",
                                     before=_brief(b.get(key)), after=_brief(c.get(key)), **kw))
                continue
            if b.get(key) != c.get(key):
                self.emit(Change(UNKNOWN, "operation_keyword_changed", f"{loc}.{key}",
                                 f"operation keyword [{key}] changed (unclassified)",
                                 before=_brief(b.get(key)), after=_brief(c.get(key)), **kw))
        for key in ("callbacks", "servers"):
            if b.get(key) != c.get(key) and key in ("callbacks",):
                self.emit(Change(UNKNOWN, "operation_keyword_changed", f"{loc}.{key}",
                                 f"operation keyword [{key}] changed (unclassified)",
                                 before=_brief(b.get(key)), after=_brief(c.get(key)), **kw))

    def _diff_security(self, b: dict, c: dict, loc: str, **kw: Any) -> None:
        b_sec, c_sec = _security_requirements(b), _security_requirements(c)
        if b_sec == c_sec:
            return
        b_set = set(b_sec or [])
        c_set = set(c_sec or [])

        if b_sec is None and c_sec is not None:
            category = BREAKING if c_sec else NON_BREAKING
            self.emit(Change(category, "operation_security_added", loc + ".security",
                             "operation now requires authentication" if c_sec
                             else "operation explicitly public",
                             before="inherit", after=_brief(c_sec), **kw))
            return
        if c_sec is None and b_sec is not None:
            self.emit(Change(UNKNOWN, "operation_security_removed", loc + ".security",
                             "operation-level security removed (now inherits document security)",
                             before=_brief(b_sec), after="inherit", **kw))
            return

        if not b_sec and c_sec:
            self.emit(Change(BREAKING, "operation_became_protected", loc + ".security",
                             "public operation now requires authentication",
                             before=[], after=_brief(c_sec), **kw))
            return
        if b_sec and not c_sec:
            self.emit(Change(NON_BREAKING, "operation_became_public", loc + ".security",
                             "protected operation is now public",
                             before=_brief(b_sec), after=[], **kw))
            return

        for req in sorted(b_set - c_set, key=lambda r: sorted(map(str, r))):
            self.emit(Change(BREAKING, "security_requirement_removed", loc + ".security",
                             "an accepted authentication alternative was removed "
                             f"({', '.join(sorted(s for s, _ in req)) or 'none'})",
                             before=sorted(map(list, req)), **kw))
        for req in sorted(c_set - b_set, key=lambda r: sorted(map(str, r))):
            self.emit(Change(NON_BREAKING, "security_requirement_added", loc + ".security",
                             "a new authentication alternative was added "
                             f"({', '.join(sorted(s for s, _ in req)) or 'none'})",
                             after=sorted(map(list, req)), **kw))

    def _diff_parameters(self, b: dict, c: dict, loc: str, **kw: Any) -> None:
        def index(operation: dict) -> dict[tuple[str, str], dict]:
            result = {}
            for parameter in operation.get("parameters") or []:
                if isinstance(parameter, dict) and isinstance(parameter.get("name"), str):
                    result[(parameter["name"], parameter.get("in", ""))] = parameter
            return result

        b_params, c_params = index(b), index(c)

        for key in sorted(set(b_params) - set(c_params)):
            name, where = key
            self.emit(Change(BREAKING, "parameter_removed", f"{loc}.parameters.{name}",
                             f"parameter [{name}] (in {where}) removed",
                             before=_brief(b_params[key], 200), **kw))

        for key in sorted(set(c_params) - set(b_params)):
            name, where = key
            required = bool(c_params[key].get("required"))
            self.emit(Change(BREAKING if required else NON_BREAKING,
                             "required_parameter_added" if required else "optional_parameter_added",
                             f"{loc}.parameters.{name}",
                             f"{'required' if required else 'optional'} parameter [{name}] (in {where}) added",
                             after=_brief(c_params[key], 200), **kw))

        for key in sorted(set(b_params) & set(c_params)):
            name, where = key
            bp, cp = b_params[key], c_params[key]
            ploc = f"{loc}.parameters.{name}"

            if bp.get("$ref") == cp.get("$ref") and bp.get("$ref"):
                continue  # shared-parameter change is reported at component level

            if bool(bp.get("required")) != bool(cp.get("required")):
                became_required = bool(cp.get("required"))
                self.emit(Change(BREAKING if became_required else NON_BREAKING,
                                 "parameter_became_required" if became_required
                                 else "parameter_became_optional",
                                 ploc + ".required",
                                 f"parameter [{name}] became "
                                 + ("required" if became_required else "optional"),
                                 before=bool(bp.get("required")),
                                 after=bool(cp.get("required")), **kw))

            for meta in ("description", "style", "explode", "example", "examples",
                         "allowEmptyValue", "allowReserved", "deprecated", "content"):
                if bp.get(meta) != cp.get(meta) and meta in ("description", "example",
                                                             "examples", "deprecated"):
                    self.emit(Change(DOCUMENTATION_ONLY, "parameter_documentation",
                                     f"{ploc}.{meta}", f"parameter {meta} changed",
                                     before=_brief(bp.get(meta)), after=_brief(cp.get(meta)), **kw))
                elif bp.get(meta) != cp.get(meta):
                    self.emit(Change(UNKNOWN, "parameter_keyword_changed", f"{ploc}.{meta}",
                                     f"parameter {meta} changed (unclassified)",
                                     before=_brief(bp.get(meta)), after=_brief(cp.get(meta)), **kw))

            if bp.get("schema") != cp.get("schema"):
                self.schema_differ.diff(bp.get("schema"), cp.get("schema"),
                                        ploc + ".schema", "request", "parameter_schema")
            elif "schema" not in bp and "schema" not in cp and bp != cp:
                self.emit(Change(UNKNOWN, "parameter_changed", ploc,
                                 "parameter changed (no schema to classify)",
                                 before=_brief(bp), after=_brief(cp), **kw))

    def _diff_request_body(self, b: dict, c: dict, loc: str, **kw: Any) -> None:
        rb_loc = loc + ".requestBody"
        b_rb, c_rb = b.get("requestBody"), c.get("requestBody")

        if b_rb is None and c_rb is None:
            return
        if b_rb is not None and c_rb is None:
            self.emit(Change(BREAKING, "request_body_removed", rb_loc,
                             "request body removed from the contract",
                             before=_brief(b_rb, 200), **kw))
            return
        if b_rb is None and c_rb is not None:
            required = bool(self._deref_rb(c_rb, candidate=True).get("required"))
            self.emit(Change(BREAKING if required else NON_BREAKING,
                             "required_request_body_added" if required
                             else "optional_request_body_added",
                             rb_loc,
                             "request body added and REQUIRED" if required
                             else "request body added (optional)",
                             after=_brief(c_rb, 200), **kw))
            return

        b_body, c_body = self._deref_rb(b_rb), self._deref_rb(c_rb, candidate=True)
        if bool(b_body.get("required")) != bool(c_body.get("required")):
            became = bool(c_body.get("required"))
            self.emit(Change(BREAKING if became else NON_BREAKING,
                             "request_body_became_required" if became
                             else "request_body_became_optional",
                             rb_loc + ".required",
                             "request body became " + ("required" if became else "optional"),
                             before=bool(b_body.get("required")),
                             after=bool(c_body.get("required")), **kw))

        b_content = b_body.get("content") or {}
        c_content = c_body.get("content") or {}
        for media in sorted(set(b_content) - set(c_content)):
            self.emit(Change(BREAKING, "request_media_type_removed",
                             f"{rb_loc}.content.{media}",
                             f"request media type [{media}] removed", **kw))
        for media in sorted(set(c_content) - set(b_content)):
            self.emit(Change(NON_BREAKING, "request_media_type_added",
                             f"{rb_loc}.content.{media}",
                             f"request media type [{media}] added", **kw))
        for media in sorted(set(b_content) & set(c_content)):
            b_schema = (b_content[media] or {}).get("schema")
            c_schema = (c_content[media] or {}).get("schema")
            if b_schema != c_schema:
                self.schema_differ.diff(b_schema, c_schema,
                                        f"{rb_loc}.content.{media}.schema", "request",
                                        "request_schema")
            if ((b_content[media] or {}).get("example")
                    != (c_content[media] or {}).get("example")):
                self.emit(Change(DOCUMENTATION_ONLY, "request_example_changed",
                                 f"{rb_loc}.content.{media}.example",
                                 "request example changed", **kw))

    def _deref_rb(self, body: Any, candidate: bool = False) -> dict:
        if not isinstance(body, dict):
            return {}
        resolver = self.candidate_resolver if candidate else self.baseline_resolver
        if "$ref" in body:
            try:
                resolved = resolver.deref(body)
            except KeyError:
                resolved = body
        else:
            resolved = body
        return resolved if isinstance(resolved, dict) else {}

    def _diff_responses(self, b: dict, c: dict, loc: str, **kw: Any) -> None:
        r_loc = loc + ".responses"
        b_resp = b.get("responses") or {}
        c_resp = c.get("responses") or {}

        def is_success(status: str) -> bool:
            return status == "default" or (status.isdigit() and 200 <= int(status) < 300)

        for status in sorted(set(b_resp) - set(c_resp)):
            category = BREAKING if is_success(status) else DOCUMENTATION_ONLY
            self.emit(Change(category, "response_status_removed", f"{r_loc}.{status}",
                             f"response [{status}] removed from the contract",
                             before=_brief(b_resp[status], 200), **kw))
        for status in sorted(set(c_resp) - set(b_resp)):
            category = NON_BREAKING if is_success(status) else DOCUMENTATION_ONLY
            self.emit(Change(category, "response_status_added", f"{r_loc}.{status}",
                             f"response [{status}] added to the contract",
                             after=_brief(c_resp[status], 200), **kw))

        for status in sorted(set(b_resp) & set(c_resp)):
            sloc = f"{r_loc}.{status}"
            b_entry, c_entry = b_resp[status], c_resp[status]
            if not isinstance(b_entry, dict) or not isinstance(c_entry, dict):
                if b_entry != c_entry:
                    self.emit(Change(UNKNOWN, "response_changed", sloc,
                                     "response changed", before=_brief(b_entry),
                                     after=_brief(c_entry), **kw))
                continue

            if b_entry.get("$ref") == c_entry.get("$ref") and b_entry.get("$ref"):
                continue  # shared response change reported at component level

            b_resolved = self._deref_entry(b_entry)
            c_resolved = self._deref_entry(c_entry, candidate=True)

            if b_resolved.get("description") != c_resolved.get("description"):
                self.emit(Change(DOCUMENTATION_ONLY, "response_description_changed",
                                 sloc + ".description", "response description changed",
                                 before=_brief(b_resolved.get("description")),
                                 after=_brief(c_resolved.get("description")), **kw))

            if b_resolved.get("headers") != c_resolved.get("headers"):
                self._diff_headers(b_resolved.get("headers") or {},
                                   c_resolved.get("headers") or {}, sloc + ".headers", **kw)

            b_content = b_resolved.get("content") or {}
            c_content = c_resolved.get("content") or {}
            for media in sorted(set(b_content) - set(c_content)):
                self.emit(Change(BREAKING if is_success(status) else DOCUMENTATION_ONLY,
                                 "response_media_type_removed", f"{sloc}.content.{media}",
                                 f"response media type [{media}] removed", **kw))
            for media in sorted(set(c_content) - set(b_content)):
                self.emit(Change(NON_BREAKING if is_success(status) else DOCUMENTATION_ONLY,
                                 "response_media_type_added", f"{sloc}.content.{media}",
                                 f"response media type [{media}] added", **kw))
            for media in sorted(set(b_content) & set(c_content)):
                b_schema = (b_content[media] or {}).get("schema")
                c_schema = (c_content[media] or {}).get("schema")
                if b_schema != c_schema:
                    self.schema_differ.diff(b_schema, c_schema,
                                            f"{sloc}.content.{media}.schema", "response",
                                            "response_schema")
            if b_resolved.get("links") != c_resolved.get("links"):
                self.emit(Change(DOCUMENTATION_ONLY, "response_links_changed",
                                 sloc + ".links", "response links changed", **kw))

            for key in set(b_resolved) | set(c_resolved):
                if key in ("description", "headers", "content", "links", "$ref"):
                    continue
                if b_resolved.get(key) != c_resolved.get(key):
                    self.emit(Change(UNKNOWN, "response_keyword_changed", f"{sloc}.{key}",
                                     f"response keyword [{key}] changed (unclassified)",
                                     before=_brief(b_resolved.get(key)),
                                     after=_brief(c_resolved.get(key)), **kw))

    def _deref_entry(self, entry: dict, candidate: bool = False) -> dict:
        resolver = self.candidate_resolver if candidate else self.baseline_resolver
        if "$ref" in entry:
            try:
                resolved = resolver.deref(entry)
                return resolved if isinstance(resolved, dict) else {}
            except KeyError:
                return entry
        return entry

    def _diff_headers(self, b_headers: dict, c_headers: dict, loc: str, **kw: Any) -> None:
        for name in sorted(set(b_headers) - set(c_headers)):
            self.emit(Change(BREAKING, "response_header_removed", f"{loc}.{name}",
                             f"response header [{name}] removed", **kw))
        for name in sorted(set(c_headers) - set(b_headers)):
            self.emit(Change(NON_BREAKING, "response_header_added", f"{loc}.{name}",
                             f"response header [{name}] added", **kw))
        for name in sorted(set(b_headers) & set(c_headers)):
            b_h = self._deref_entry(b_headers[name] or {})
            c_h = self._deref_entry(c_headers[name] or {}, candidate=True)
            if bool(b_h.get("required")) != bool(c_h.get("required")):
                became = bool(c_h.get("required"))
                self.emit(Change(BREAKING if became else NON_BREAKING,
                                 "response_header_required_changed", f"{loc}.{name}.required",
                                 f"response header [{name}] became "
                                 + ("required" if became else "optional"), **kw))
            if b_h.get("schema") != c_h.get("schema"):
                self.schema_differ.diff(b_h.get("schema"), c_h.get("schema"),
                                        f"{loc}.{name}.schema", "response", "header_schema")

    # ------------------------------------------------------------ components
    def _diff_components(self) -> None:
        b_comp = self.baseline.get("components") or {}
        c_comp = self.candidate.get("components") or {}

        for section in sorted(set(b_comp) | set(c_comp)):
            b_section = b_comp.get(section) or {}
            c_section = c_comp.get(section) or {}
            if not isinstance(b_section, dict):
                b_section = {}
            if not isinstance(c_section, dict):
                c_section = {}

            for name in sorted(set(b_section) - set(c_section)):
                pointer = f"#/components/{section}/{name}"
                affected = self._affected_operations(pointer)
                if section == "securitySchemes":
                    category = BREAKING if affected else DOCUMENTATION_ONLY
                    kind = "security_scheme_removed"
                elif affected:
                    category = BREAKING
                    kind = "shared_component_removed"
                else:
                    category = DOCUMENTATION_ONLY
                    kind = "unused_component_removed"
                self.emit(Change(category, kind, f"components.{section}.{name}",
                                 f"component [{section}.{name}] removed"
                                 + (f" — {len(affected)} operation(s) referenced it"
                                    if affected else " (unreferenced)"),
                                 before=_brief(b_section[name], 200),
                                 affected_operations=affected))

            for name in sorted(set(c_section) - set(b_section)):
                self.emit(Change(NON_BREAKING, "shared_component_added",
                                 f"components.{section}.{name}",
                                 f"component [{section}.{name}] added",
                                 after=_brief(c_section[name], 200)))

            for name in sorted(set(b_section) & set(c_section)):
                if b_section[name] == c_section[name]:
                    continue
                self._diff_component(section, name, b_section[name], c_section[name])

    def _affected_operations(self, pointer: str) -> list[str]:
        return _operations_referencing(self.baseline, pointer, self.graph)

    def _diff_component(self, section: str, name: str, b: Any, c: Any) -> None:
        loc = f"components.{section}.{name}"
        pointer = f"#/components/{section}/{name}"
        affected = self._affected_operations(pointer)

        if section == "securitySchemes":
            self.emit(Change(BREAKING, "security_scheme_changed", loc,
                             f"security scheme [{name}] changed — authentication semantics may differ",
                             before=_brief(b, 300), after=_brief(c, 300),
                             affected_operations=affected))
            return

        if section == "schemas":
            before_count = len(self.changes)
            direction = self._usage_direction(pointer)
            self.schema_differ.diff(b, c, loc, direction, "component_schema")
            for change in self.changes[before_count:]:
                change.affected_operations = affected
            return

        if section == "responses":
            b_res = self._deref_entry(b if isinstance(b, dict) else {})
            c_res = self._deref_entry(c if isinstance(c, dict) else {}, candidate=True)
            b_content = b_res.get("content") or {}
            c_content = c_res.get("content") or {}
            for media in sorted(set(b_content) | set(c_content)):
                b_schema = (b_content.get(media) or {}).get("schema")
                c_schema = (c_content.get(media) or {}).get("schema")
                if b_schema != c_schema:
                    before_count = len(self.changes)
                    self.schema_differ.diff(b_schema, c_schema,
                                            f"{loc}.content.{media}.schema", "response",
                                            "component_response_schema")
                    for change in self.changes[before_count:]:
                        change.affected_operations = affected
            if b_res.get("description") != c_res.get("description"):
                self.emit(Change(DOCUMENTATION_ONLY, "component_response_description",
                                 loc + ".description", "shared response description changed",
                                 before=_brief(b_res.get("description")),
                                 after=_brief(c_res.get("description")),
                                 affected_operations=affected))
            return

        if section == "parameters":
            before_count = len(self.changes)
            if (b if isinstance(b, dict) else {}).get("schema") != \
                    (c if isinstance(c, dict) else {}).get("schema"):
                self.schema_differ.diff((b or {}).get("schema"), (c or {}).get("schema"),
                                        loc + ".schema", "request", "component_parameter_schema")
            b_req = bool((b if isinstance(b, dict) else {}).get("required"))
            c_req = bool((c if isinstance(c, dict) else {}).get("required"))
            if b_req != c_req:
                self.emit(Change(BREAKING if c_req else NON_BREAKING,
                                 "component_parameter_required_changed",
                                 loc + ".required",
                                 "shared parameter became " + ("required" if c_req else "optional"),
                                 before=b_req, after=c_req))
            for change in self.changes[before_count:]:
                if not change.affected_operations:
                    change.affected_operations = affected
            return

        # Any other component section: opaque comparison.
        self.emit(Change(UNKNOWN, "component_changed", loc,
                         f"component [{section}.{name}] changed (unclassified section)",
                         before=_brief(b, 300), after=_brief(c, 300),
                         affected_operations=affected))

    def _usage_direction(self, pointer: str) -> str:
        """Whether the shared schema is used in requests, responses, or both.

        Follows $refs transitively (a schema nested in a request body through
        other components is used in requests) in both documents. A schema no
        operation reaches is judged as "both", the strictest direction."""
        if self._usage is None:
            self._usage = {}
            for document in (self.baseline, self.candidate):
                for operation in _operations(document).values():
                    parts = {"response": [operation.get("responses")],
                             "request": [operation.get("requestBody"), operation.get("parameters")]}
                    for side, nodes in parts.items():
                        for ref in _reachable_refs(document, nodes):
                            self._usage.setdefault(ref, set()).add(side)
        sides = self._usage.get(pointer, set())
        if sides == {"response"}:
            return "response"
        if sides == {"request"}:
            return "request"
        return "both"


def build_report(baseline: dict, candidate: dict,
                 baseline_label: str, candidate_label: str) -> dict:
    analyzer = CompatibilityAnalyzer(baseline, candidate)
    changes = analyzer.analyze()
    summary = {BREAKING: 0, NON_BREAKING: 0, DOCUMENTATION_ONLY: 0, UNKNOWN: 0}
    for change in changes:
        summary[change.category] += 1
    kinds: dict[str, int] = {}
    for change in changes:
        kinds[change.kind] = kinds.get(change.kind, 0) + 1
    return {
        "tool": "capitalix-openapi-compatibility",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "baseline": baseline_label,
        "candidate": candidate_label,
        "summary": {
            **summary,
            "total": len(changes),
            "by_kind": dict(sorted(kinds.items())),
        },
        "operations": {
            "baseline": len(_operations(baseline)),
            "candidate": len(_operations(candidate)),
        },
        "changes": [change.to_dict() for change in changes],
    }


def render_markdown(report: dict) -> str:
    s = report["summary"]
    lines = [
        "# OpenAPI Contract Compatibility Report",
        "",
        f"- Baseline: `{report['baseline']}` ({report['operations']['baseline']} operations)",
        f"- Candidate: `{report['candidate']}` ({report['operations']['candidate']} operations)",
        f"- Generated: {report['generated_at']}",
        "",
        "## Summary",
        "",
        "| Category | Count |",
        "|---|---|",
        f"| BREAKING | {s[BREAKING]} |",
        f"| UNKNOWN | {s[UNKNOWN]} |",
        f"| NON_BREAKING | {s[NON_BREAKING]} |",
        f"| DOCUMENTATION_ONLY | {s[DOCUMENTATION_ONLY]} |",
        f"| **total** | **{s['total']}** |",
        "",
    ]

    for category, title in ((BREAKING, "Breaking changes"),
                            (UNKNOWN, "Unclassified changes (fail closed)"),
                            (NON_BREAKING, "Non-breaking changes"),
                            (DOCUMENTATION_ONLY, "Documentation-only changes")):
        changes = [c for c in report["changes"] if c["category"] == category]
        lines.append(f"## {title} ({len(changes)})")
        lines.append("")
        if not changes:
            lines.append("_None._")
            lines.append("")
            continue
        lines.append("| Kind | Location | Detail |")
        lines.append("|---|---|---|")
        for change in changes[:400]:
            detail = change["description"].replace("|", "\\|")
            lines.append(f"| `{change['kind']}` | `{change['location']}` | {detail} |")
        if len(changes) > 400:
            lines.append("")
            lines.append(f"_… and {len(changes) - 400} more (see the JSON report)._")
        lines.append("")

    if s[UNKNOWN]:
        lines += [
            "> **Fail closed:** unclassified changes require an explicit",
            "> compatibility decision before this contract may be approved.",
            "",
        ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--baseline", required=True, help="approved OpenAPI document (JSON)")
    parser.add_argument("--candidate", required=True, help="candidate OpenAPI document (JSON)")
    parser.add_argument("--baseline-label", default=None)
    parser.add_argument("--candidate-label", default=None)
    parser.add_argument("--json-out", default=None, help="write the JSON report here")
    parser.add_argument("--markdown-out", default=None, help="write the Markdown report here")
    parser.add_argument("--fail-on-breaking", action="store_true",
                        help="exit 1 when BREAKING changes exist")
    parser.add_argument("--fail-on-unknown", action="store_true",
                        help="exit 2 when UNKNOWN changes exist (takes precedence)")
    args = parser.parse_args(argv)

    try:
        with open(args.baseline, encoding="utf-8") as fh:
            baseline = json.load(fh)
        with open(args.candidate, encoding="utf-8") as fh:
            candidate = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"openapi_compatibility: cannot load documents: {exc}", file=sys.stderr)
        return 3

    report = build_report(baseline, candidate,
                          args.baseline_label or args.baseline,
                          args.candidate_label or args.candidate)

    json_text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    markdown_text = render_markdown(report)

    if args.json_out:
        _write(args.json_out, json_text)
    if args.markdown_out:
        _write(args.markdown_out, markdown_text)

    s = report["summary"]
    print(f"OPENAPI COMPATIBILITY: {s[BREAKING]} breaking, {s[UNKNOWN]} unknown, "
          f"{s[NON_BREAKING]} non-breaking, {s[DOCUMENTATION_ONLY]} documentation-only "
          f"({s['total']} changes)")
    if args.json_out:
        print(f"JSON report: {args.json_out}")
    if args.markdown_out:
        print(f"Markdown report: {args.markdown_out}")

    if s[UNKNOWN] and args.fail_on_unknown:
        print("COMPATIBILITY FAILED: unclassified changes require an explicit decision "
              "(fail closed on UNKNOWN)", file=sys.stderr)
        return 2
    if s[BREAKING] and args.fail_on_breaking:
        print("COMPATIBILITY FAILED: breaking changes present (--fail-on-breaking)",
              file=sys.stderr)
        return 1
    return 0


def _write(path: str, text: str) -> None:
    import os
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


if __name__ == "__main__":
    sys.exit(main())
