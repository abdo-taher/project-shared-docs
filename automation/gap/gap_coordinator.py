#!/usr/bin/env python3
"""Capitalix API gap coordinator: GitHub gap issues (shared docs) <-> GitHub backend issues (capitalix).

  python3 scripts/gap/gap_coordinator.py sync [--dry-run] [--issue N ...] [--replay N ...]
  python3 scripts/gap/gap_coordinator.py ensure-labels

One run (idempotent; safe to repeat, interrupt and re-run):

  1. read every open GitHub issue that is (or looks like) an API gap request;
  2. parse it (CLI JSON block or issue form) and validate it strictly against
     capitalix.api-gap.v1 and the published contract (version, sha256, operation,
     actor namespace); reject secrets and personal data;
  3. decide trust from GitHub itself (the author's repository permission, and
     label events by trusted maintainers) — never from the issue text;
  4. fingerprint the gap; one backend (capitalix) issue per fingerprint, every consumer
     report linked to it (re-runs find the existing issue; racing creations
     converge on the oldest one);
  5. derive each request's state from the backend issue (pull requests, triage labels) and from the
     published contract (release evidence + resolution checks), then the
     consumer's verification comment;
  6. write the state back: one exclusive gap:* label, a state comment edited
     in place, and a history comment on every transition.

The coordinator never executes request content, never writes contracts, never
approves or merges anything, and never starts a coding agent (that is
gap_dispatch.py, on a host with an approved agent runtime).

Credentials (environment): API_GAP_GITHUB_TOKEN (Issues read/write on the
intake repository) and API_GAP_BACKEND_TOKEN (fine-grained, Issues read/write and Pull requests read on the
backend repository only). --dry-run needs neither and changes nothing.

Exit codes: 0 ok; 1 some requests failed to synchronize; 3 usage/config error;
4 another coordinator holds the lock.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import gap_core as core  # noqa: E402
from gap_contract import IntegrityError, PublishedContracts, actor_of, evaluate_check, find_operation  # noqa: E402
from gap_http import ApiError  # noqa: E402
from gap_github_backend import GitHubBackend, STATE_LABELS as BACKEND_STATE_LABELS  # noqa: E402
from gap_platforms import STATE_LABELS, GitHub  # noqa: E402
from gap_policy import sensitivity_reasons  # noqa: E402

HERE = Path(__file__).resolve().parent
STATE_MARKER = "capitalix-gap-coordinator:v1"
HISTORY_MARKER = "capitalix-gap-history:v1"
VERIFY_MARKER = "capitalix-gap-verification:v1"
CONSUMER_MARKER = "capitalix-gap-consumer"
RESOLUTION_SCHEMA = "capitalix.api-gap-resolution.v1"
ROOT_CAUSES = {
    "A": "endpoint truly missing",
    "B": "backend operation exists but is not in the published contract",
    "C": "backend behavior is incorrect",
    "D": "contract inference is incorrect",
    "E": "consumer implementation is incorrect",
    "F": "business requirement is incomplete",
    "G": "authentication/permission behavior needs an architectural decision",
}
TERMINAL_CLOSE = {"DUPLICATE", "RESOLVED"}
STATES = ("SUBMITTED", "VALIDATING", "NEEDS_TRIAGE", "ACCEPTED", "DUPLICATE", "REJECTED", "IN_PROGRESS",
          "CONTRACT_PUBLISHED", "CONSUMER_VERIFIED", "RESOLVED", "BLOCKED")


def label_of(state: str) -> str:
    return "gap:" + state.lower().replace("_", "-")


def load_policy(path: Path) -> dict:
    policy = json.loads(path.read_text(encoding="utf-8"))
    if policy.get("schema") != "capitalix.api-gap-policy.v1":
        raise ValueError("unsupported policy schema")
    return policy


def marker_json(text: str, marker: str):
    match = re.search(r"<!-- " + re.escape(marker) + r" (\{.*?\}) -->", text or "", re.S)
    if not match:
        return None
    try:
        value = json.loads(match.group(1))
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def fence(text: str, lang: str = "text") -> str:
    """Untrusted text as an inert block: longer fence than any backtick run, every line indented
    (so nothing can close the block, mention anyone)."""
    longest = max((len(m) for m in re.findall(r"`+", text)), default=0)
    ticks = "`" * max(3, longest + 1)
    body = "\n".join("  " + line for line in text.replace("\r", "").splitlines())
    return f"{ticks}{lang}\n{body}\n{ticks}"


# --------------------------------------------------------------------------- per-request evaluation

@dataclass
class Intake:
    number: int
    author: str
    state: str = "VALIDATING"
    reason: str = ""
    details: list = field(default_factory=list)
    request: dict | None = None
    fingerprint: str | None = None
    sensitive: bool = False
    resolution: dict | None = None
    backend: int | None = None
    backend_closed: bool = False
    previous: dict = field(default_factory=dict)
    state_comment: dict | None = None
    error: str | None = None


def looks_like_gap(issue: dict) -> bool:
    body = issue.get("body") or ""
    names = {l["name"] for l in issue.get("labels", [])}
    return "api-gap" in names or core.BODY_MARKER in body or bool(re.search(r"^### Gap type\s*$", body, re.M))


def trusted_label(events: list[dict], present: set[str], label: str, is_trusted) -> bool:
    """True when `label` is on the issue and its most recent add was by a trusted actor."""
    if label not in present:
        return False
    adds = [e for e in events if e.get("event") == "labeled" and (e.get("label") or {}).get("name") == label]
    return bool(adds) and is_trusted((adds[-1].get("actor") or {}).get("login", ""))


class Coordinator:
    def __init__(self, policy: dict, github: GitHub, backend: GitHubBackend | None, contracts: PublishedContracts,
                 *, dry_run: bool = False, now=None, log=print):
        self.policy = policy
        self.gh = github
        self.gl = backend
        self.contracts = contracts
        self.dry_run = dry_run
        self.now = now or (lambda: datetime.now(timezone.utc))
        self.log = log
        self.actions: list[str] = []
        self._permission: dict[str, str] = {}
        self.counters: dict[str, int] = {}

    # ----------------------------------------------------------------- helpers

    def count(self, key: str, n: int = 1) -> None:
        self.counters[key] = self.counters.get(key, 0) + n

    def act(self, description: str, fn, *args, **kwargs):
        self.actions.append(("DRY-RUN " if self.dry_run else "") + description)
        if self.dry_run:
            return None
        return fn(*args, **kwargs)

    def trusted_github(self, login: str) -> bool:
        if not login:
            return False
        if login in self.policy.get("trusted_github_users", []):
            return True
        if login not in self._permission:
            try:
                self._permission[login] = self.gh.permission(login)
            except ApiError as exc:
                if exc.status in (401, 403) and not self.gh.can_write:
                    # No credential (a dry run): trust cannot be verified, so nobody is trusted.
                    self._permission[login] = "unverifiable"
                    self.count("trust_unverifiable")
                else:
                    raise
        return self._permission[login] in self.policy.get("trusted_github_permissions", [])

    def sensitive(self, request: dict) -> bool:
        return bool(sensitivity_reasons(self.policy, request))

    # ----------------------------------------------------------------- pass 1: intake

    def evaluate(self, issue: dict, comments: list[dict]) -> Intake:
        number = issue["number"]
        author = (issue.get("user") or {}).get("login", "")
        intake = Intake(number=number, author=author)
        own = [c for c in comments if (c.get("user") or {}).get("login") == self.policy["coordinator_github_login"]]
        for comment in own:
            if marker_json(comment.get("body"), STATE_MARKER) is not None:
                intake.state_comment = comment
                intake.previous = marker_json(comment["body"], STATE_MARKER)
        labels = {l["name"] for l in issue.get("labels", [])}
        events = self.gh.label_events(number) if labels & {"gap:triage-approved", "gap:triage-rejected"} else []
        approved = trusted_label(events, labels, "gap:triage-approved", self.trusted_github)
        if trusted_label(events, labels, "gap:triage-rejected", self.trusted_github):
            return self._final(intake, "REJECTED", "TRIAGE_REJECTED", ["a maintainer rejected this request"])

        request, problems = core.parse_issue_body(issue.get("body") or "", number, issue.get("created_at", ""))
        if problems:
            return self._final(intake, "REJECTED", "INVALID_REQUEST", problems)
        errors = core.validate(request)
        if errors:
            sensitive = [e for e in errors if core.is_sensitive_evidence_error(e)]
            if sensitive:
                return self._final(intake, "REJECTED", "SENSITIVE_DATA", sensitive)
            return self._final(intake, "REJECTED", "INVALID_REQUEST", errors)
        intake.request = request

        version, digest = request["contract"]["version"], request["contract"]["sha256"]
        entry = self.contracts.entry(version)
        if entry is None:
            return self._final(intake, "REJECTED", "UNKNOWN_CONTRACT_VERSION",
                               [f"contract version {version} is not published"])
        if entry.get("sha256") != digest:
            return self._final(intake, "REJECTED", "CONTRACT_SHA_MISMATCH",
                               [f"contract.sha256 does not match published version {version}"])
        document = self.contracts.document(version)

        if request["gap_type"] == "MISSING_OPERATION":
            proposed = request.get("proposed") or {}
            if proposed.get("method") and proposed.get("path"):
                if find_operation(document, proposed):
                    return self._final(intake, "REJECTED", "OPERATION_EXISTS",
                                       [f"{proposed['method']} {proposed['path']} exists in {version}; "
                                        "report a mismatch type instead"])
                current = self.contracts.current()
                found = find_operation(self.contracts.document(current["version"]), proposed)
                if found:
                    intake.resolution = {"version": current["version"], "sha256": current["sha256"],
                                         "operation_id": found[2].get("operationId"),
                                         "summary": "the operation is available in a newer published contract",
                                         "already_available": True}
        elif request.get("operation"):
            found = find_operation(document, request["operation"])
            if found is None:
                return self._final(intake, "REJECTED", "OPERATION_NOT_IN_CONTRACT",
                                   [f"the operation is not in contract {version}; use MISSING_OPERATION"])
            method, path, op, _ = found
            actor = actor_of(path, op)
            if actor is None:
                return self._final(intake, "REJECTED", "DEPRECATED_ALIAS",
                                   ["the operation is a deprecated /api/v1 alias; report the canonical operation"])
            if actor != request["actor"]:
                return self._final(intake, "REJECTED", "ACTOR_MISMATCH",
                                   [f"the operation belongs to actor namespace {actor}"])
            if op.get("operationId"):
                request["operation"] = {"operation_id": op["operationId"], "method": method, "path": path}

        intake.fingerprint = core.fingerprint(request)
        intake.sensitive = self.sensitive(request)
        flags = []
        capability = request.get("capability_id")
        if capability and not any(capability.startswith(p + "-") for p in self.policy["capability_prefixes"]):
            flags.append("UNKNOWN_CAPABILITY")
        if any(core.suspicious_instructions(text) for _, text in core.free_text(request)):
            flags.append("SUSPICIOUS_CONTENT")
        if not self.trusted_github(author):
            flags.append("UNTRUSTED_REPORTER")
        if flags and not approved:
            intake.state, intake.reason = "NEEDS_TRIAGE", flags[0]
            intake.details = [f"waiting for a maintainer: {', '.join(flags)} "
                              "(a trusted maintainer adds gap:triage-approved or gap:triage-rejected)"]
            if self._permission.get(author) == "unverifiable":
                intake.details.append("reporter trust could not be verified without a GitHub credential (dry run); "
                                      "treated as untrusted")
            return intake
        intake.state, intake.reason = "ACCEPTED", "VALID"
        if intake.sensitive:
            intake.details = ["sensitive area: the owner must approve before any backend implementation starts"]
        return intake

    @staticmethod
    def _final(intake: Intake, state: str, reason: str, details: list) -> Intake:
        intake.state, intake.reason, intake.details = state, reason, details
        return intake

    # ----------------------------------------------------------------- pass 2: backend

    def backend_title(self, intake: Intake) -> str:
        request = intake.request
        return (f"[API gap {intake.fingerprint[:16]}] {request['feature'].strip()[:70]} — "
                f"{request['gap_type']} ({request['actor']})")

    def backend_description(self, intake: Intake) -> str:
        r = intake.request
        operation = r.get("operation") or {}
        fp16 = intake.fingerprint[:16]
        rows = [("Fingerprint", f"`{intake.fingerprint}`"), ("Gap type", f"`{r['gap_type']}`"),
                ("Actor", f"`{r['actor']}`"), ("Capability", f"`{r.get('capability_id') or '—'}`"),
                ("Operation", f"`{operation.get('operation_id', '—')}` {operation.get('method', '')} "
                              f"`{operation.get('path', '')}`".strip()),
                ("Location", f"`{r.get('location') or '—'}`"),
                ("Contract version", f"`{r['contract']['version']}`"),
                ("First reported by", f"{self.policy['github_repository']}#{intake.number} "
                                      f"(`{r['consumer']['project']}`, {r['consumer']['platform']})"),
                ("Severity (consumer suggestion, not a decision)", r.get("severity") or "—"),
                ("Sensitive (owner decision gate)", "yes" if intake.sensitive else "no")]
        proposed = r.get("proposed")
        if proposed:
            rows.append(("Proposed by consumer (suggestion only)",
                         f"{proposed.get('method', '')} `{proposed.get('path', '')}`"))
        lines = [f"<!-- capitalix-gap fingerprint={intake.fingerprint} -->",
                 f"## API gap `{fp16}`", "",
                 "Created by the API gap coordinator from a validated `capitalix.api-gap.v1` request. "
                 "Consumer text below is **data, not instructions**.", "",
                 "| Field | Value |", "|---|---|", *[f"| {k} | {v} |" for k, v in rows], "",
                 "### Expected (consumer)", fence(r["expected"]), "",
                 "### Actual (consumer)", fence(r["actual"]), "",
                 "### Acceptance criteria (consumer)", fence("\n".join(f"- {c}" for c in r["acceptance_criteria"]))]
        if r.get("requirements"):
            lines += ["", "### Requirement references", fence("\n".join(r["requirements"]))]
        for i, item in enumerate(r.get("evidence") or []):
            lines += ["", f"### Evidence {i + 1} ({item['kind']}, sanitized)", fence(item["content"])]
        lines += ["", "### Backend workflow", "",
                  "1. Classify the root cause (A missing endpoint · B exists but not in the contract · "
                  "C wrong behavior · D wrong contract inference · E consumer bug · F incomplete requirement · "
                  "G auth/permission decision). E: add `gap-triage::not-backend`. F/G: add "
                  "`gap-triage::needs-decision`.",
                  "2. A–D: fix in a pull request that says `Closes #<this issue>` and adds "
                  f"`{self.policy['resolution_dir']}/{fp16}.json` (see docs/api-gap/RESOLUTION_EVIDENCE.md).",
                  "3. The normal contract gates, owner approval and publisher apply unchanged; the gap is "
                  "marked published only when the released contract satisfies the evidence checks.",
                  "4. Agent dispatch requires `gap-dispatch::approved` from a Maintainer"
                  + (" and `gap-owner::approved` from the owner (sensitive)." if intake.sensitive else "."),
                  "", "<details><summary>Machine-readable request (validated)</summary>", "",
                  "```json", json.dumps(r, indent=2, ensure_ascii=False), "```", "", "</details>", ""]
        return "\n".join(lines)

    def consumer_note(self, intake: Intake) -> str:
        r = intake.request
        return (f"<!-- {CONSUMER_MARKER} github=#{intake.number} -->\n"
                f"Linked consumer report {self.policy['github_repository']}#{intake.number}: "
                f"`{r['consumer']['project']}` ({r['consumer']['platform']}), feature "
                f"{fence(r['feature'])}\ncontract `{r['contract']['version']}`.")

    def ensure_backend_issue(self, intake: Intake, group: list[Intake]) -> dict | None:
        found = self.gl.find_by_fingerprint(intake.fingerprint)
        if not found:
            labels = ["api-gap", "gap::accepted", "gap-type::" + intake.request["gap_type"].lower(),
                      "gap-actor::" + intake.request["actor"]] + (["gap-sensitive"] if intake.sensitive else [])
            created = self.act(f"create backend issue for {intake.fingerprint[:16]} (github #{intake.number})",
                               self.gl.create_issue, self.backend_title(intake), self.backend_description(intake),
                               labels)
            if created is None:
                return None
            self.count("backend_issues_created")
            # Converge on the oldest issue if another worker created one concurrently.
            found = self.gl.find_by_fingerprint(intake.fingerprint) or [created]
        primary, extras = found[0], found[1:]
        for extra in extras:
            if extra.get("state") == "opened":
                self.act(f"close backend duplicate #{extra['iid']} of #{primary['iid']}", self._close_duplicate,
                         extra["iid"], primary["iid"])
        notes = None
        for member in group:
            marker = f"<!-- {CONSUMER_MARKER} github=#{member.number} -->"
            if member.number == intake.number and f"#{member.number} " in (primary.get("description") or ""):
                continue
            if notes is None:
                notes = self.gl.notes(primary["iid"])
            if not any(marker in (n.get("body") or "") for n in notes):
                self.act(f"link github #{member.number} to backend #{primary['iid']}", self.gl.add_note,
                         primary["iid"], self.consumer_note(member))
                self.count("consumer_links_added")
        return primary

    def _close_duplicate(self, iid: int, primary: int) -> None:
        self.gl.add_note(iid, f"Duplicate of #{primary} (same API gap fingerprint); closed by the coordinator.")
        self.gl.update_issue(iid, state_event="close", add_labels="gap::blocked")

    def trusted_backend_label(self, iid: int, events: list[dict], present: set[str], label: str,
                             usernames: list[str] | None = None) -> bool:
        if label not in present:
            return False
        adds = [e for e in events if e.get("action") == "add" and (e.get("label") or {}).get("name") == label]
        if not adds:
            return False
        user = adds[-1].get("user") or {}
        if usernames is not None:
            return user.get("username") in usernames
        return self.gl.access_level(int(user.get("id", 0))) >= self.policy["dispatch_min_access_level"]

    def backend_state(self, gl_issue: dict, fingerprint: str) -> tuple[str, str, dict | None]:
        """(state, reason, resolution) of the backend issue."""
        iid = gl_issue["iid"]
        present = set(gl_issue.get("labels") or [])
        events = self.gl.label_events(iid) if present & {"gap-triage::not-backend", "gap-triage::needs-decision"} else []
        if self.trusted_backend_label(iid, events, present, "gap-triage::not-backend"):
            return "REJECTED", "NOT_A_BACKEND_GAP", None
        if self.trusted_backend_label(iid, events, present, "gap-triage::needs-decision"):
            return "BLOCKED", "OWNER_DECISION_REQUIRED", None
        resolution, reason = self.detect_resolution(gl_issue, fingerprint)
        if resolution:
            return "CONTRACT_PUBLISHED", "PUBLISHED_AND_VERIFIED", resolution
        mrs = self._mrs.get(iid, [])
        if any(mr.get("state") == "opened" for mr in mrs) or "gap::in-progress" in present \
                or reason in ("MERGED_NOT_PUBLISHED", "PUBLICATION_NOT_CONFIRMED", "PUBLISHED_SCHEMA_INCORRECT",
                              "RESOLUTION_EVIDENCE_MISSING", "RESOLUTION_EVIDENCE_INVALID",
                              "RESOLUTION_EVIDENCE_VACUOUS"):
            return "IN_PROGRESS", reason, None
        return "ACCEPTED", reason, None

    def detect_resolution(self, issue: dict, fingerprint: str) -> tuple[dict | None, str]:
        """Resolved only with evidence: an approved implementation merged into the development branch, its
        resolution-evidence file at the merge commit, and the *currently published, verified* contract
        satisfying every check (while the reporter's contract version did not: no vacuous evidence).

        Boundary: the contract is published by infrastructure outside GitHub. Which commit it was built from
        is not verifiable here, so publication is proven by the contract content, not by release provenance."""
        iid = issue["iid"]
        prs = self.gl.related_merge_requests(iid)
        self._mrs[iid] = prs
        bases = {self.policy["development"]["base_branch"], self.policy["development"].get("review_base")}
        merged = sorted((p for p in prs if p.get("state") == "merged" and p.get("target_branch") in bases),
                        key=lambda p: p.get("merged_at") or "", reverse=True)
        if not merged:
            return None, "NO_MERGED_MR" if prs else "NO_MR"
        change = merged[0]
        merge_sha = change.get("merge_commit_sha") or change["sha"]
        raw = self.gl.file_at(f"{self.policy['resolution_dir']}/{fingerprint[:16]}.json", merge_sha)
        if raw is None:
            return None, "RESOLUTION_EVIDENCE_MISSING"
        evidence, problem = parse_resolution(raw, fingerprint, iid)
        if problem:
            return None, "RESOLUTION_EVIDENCE_INVALID"
        pointer = self.contracts.current()
        document = self.contracts.document(pointer["version"])
        failures = [f for f in (evaluate_check(document, c) for c in evidence.get("checks", [])) if f]
        if failures:
            self._failures[iid] = failures
            return None, "MERGED_NOT_PUBLISHED"
        request = self._requests.get(fingerprint)
        if request is not None and self.policy.get("evidence", {}).get("require_failing_on_published", True):
            reported = self.contracts.document(request["contract"]["version"])
            if not any(evaluate_check(reported, c) for c in evidence.get("checks", [])):
                return None, "RESOLUTION_EVIDENCE_VACUOUS"
        summary = evidence.get("summary", "")
        return {"version": pointer["version"], "sha256": pointer["sha256"], "backend_commit": merge_sha,
                "merge_request": change["iid"], "promoted_from_development": False,
                "publication_proof": self.policy.get("publication_proof", "contract-evidence"),
                "root_cause": evidence["root_cause"],
                "summary": summary if not core.sensitive_findings(summary) else "",
                "checks": len(evidence.get("checks", []))}, "PUBLISHED_AND_VERIFIED"

    def consumer_verified(self, intake: Intake, comments: list[dict]) -> bool:
        resolution = intake.resolution or {}
        target = self.contracts.position(resolution.get("version", ""))
        if target < 0:
            return False
        for comment in comments:
            payload = marker_json(comment.get("body"), VERIFY_MARKER)
            login = (comment.get("user") or {}).get("login", "")
            if payload is None or not (login == intake.author or self.trusted_github(login)):
                continue
            entry = self.contracts.entry(str(payload.get("version", "")))
            if payload.get("fingerprint") == intake.fingerprint and entry \
                    and entry.get("sha256") == payload.get("sha256") \
                    and self.contracts.position(payload["version"]) >= target and payload.get("tests_passed") is True:
                return True
        return False

    # ----------------------------------------------------------------- write-back

    def state_body(self, intake: Intake, attempts: int) -> str:
        state = {"fingerprint": intake.fingerprint, "state": intake.state, "reason": intake.reason,
                 "backend": intake.backend if self.policy.get("public_backend_reference") else None,
                 "resolution": intake.resolution, "attempts": attempts, "last_error": intake.error,
                 "updated_at": core.utc_now()}
        lines = [f"<!-- {STATE_MARKER} {json.dumps(state, sort_keys=True)} -->",
                 f"**API gap coordinator** — state **{intake.state}** (`{intake.reason}`)"]
        if intake.fingerprint:
            lines.append(f"- Gap fingerprint: `{intake.fingerprint[:16]}`")
        if intake.backend and self.policy.get("public_backend_reference"):
            lines.append(f"- Backend ticket: BE-{intake.backend}")
        lines += [f"- {d}" for d in intake.details]
        if intake.resolution:
            lines += self.resolution_lines(intake)
        lines.append("\n_This comment is maintained by the coordinator; editing it changes nothing._")
        return "\n".join(lines)

    def resolution_lines(self, intake: Intake) -> list[str]:
        r = intake.resolution
        out = [f"- Published contract: `{r['version']}` (sha256 `{r['sha256'][:16]}…`)"]
        if r.get("summary"):
            out.append(f"- Change: {r['summary'][:300]}")
        if r.get("backend_commit"):
            out.append(f"- Backend change released from commit `{r['backend_commit'][:12]}`")
        if r.get("publication_proof"):
            out.append("- Publication proof: the published contract satisfies the fix's evidence checks "
                       "(the contract is released outside GitHub; its build provenance is not verified here)")
        if intake.state == "CONTRACT_PUBLISHED":
            out += ["- **Required consumer action** (your pin never moves on its own):",
                    f"  1. `python3 tool/capitalix_contract.py update --version {r['version']}`",
                    "  2. run your contract checks and integration tests",
                    f"  3. `python3 tool/capitalix_gap.py confirm {intake.number} --tests-passed`"]
        return out

    def apply(self, intake: Intake, issue: dict) -> None:
        number = intake.number
        present = {l["name"] for l in issue.get("labels", [])}
        target = label_of(intake.state)
        wanted_add = [l for l in ("api-gap", target) if l not in present]
        wanted_remove = [l for l in STATE_LABELS if l in present and l != target]
        if wanted_add or wanted_remove:
            self.act(f"github #{number}: labels +{wanted_add} -{wanted_remove}", self.gh.set_labels,
                     number, wanted_add, wanted_remove)
        changed = (intake.previous.get("state"), intake.previous.get("reason")) != (intake.state, intake.reason) \
            or (intake.previous.get("resolution") or {}).get("version") != (intake.resolution or {}).get("version")
        attempts = 0 if intake.error is None else int(intake.previous.get("attempts", 0)) + 1
        body = self.state_body(intake, attempts)
        if intake.state_comment is None:
            self.act(f"github #{number}: create state comment", self.gh.comment, number, body)
        elif changed or attempts != int(intake.previous.get("attempts", 0)):
            self.act(f"github #{number}: update state comment", self.gh.edit_comment, intake.state_comment["id"], body)
        if changed:
            history = {"from": intake.previous.get("state"), "to": intake.state, "reason": intake.reason,
                       "at": core.utc_now()}
            text = [f"<!-- {HISTORY_MARKER} {json.dumps(history, sort_keys=True)} -->",
                    f"API gap state: **{intake.previous.get('state') or 'SUBMITTED'} → {intake.state}** "
                    f"(`{intake.reason}`)"]
            if intake.state == "CONTRACT_PUBLISHED":
                text += ["", "A published, approved contract now contains the fix for this gap."]
                text += self.resolution_lines(intake)
            self.act(f"github #{number}: history comment {history['from']} -> {intake.state}", self.gh.comment,
                     number, "\n".join(text))
            self.count("transitions")
        if (intake.state in TERMINAL_CLOSE or intake.reason == "TRIAGE_REJECTED") and issue.get("state") == "open":
            reason = "completed" if intake.state == "RESOLVED" else "not_planned"
            self.act(f"github #{number}: close ({reason})", self.gh.close, number, reason)

    def sync_backend_labels(self, gl_issue: dict, members: list[Intake]) -> None:
        states = {m.state for m in members}
        present = set(gl_issue.get("labels") or [])
        if members and states == {"RESOLVED"}:
            target = "gap::resolved"
        elif states & {"CONTRACT_PUBLISHED", "CONSUMER_VERIFIED", "RESOLVED"}:
            target = "gap::contract-published"
        elif "BLOCKED" in states:
            target = "gap::blocked"
        elif "IN_PROGRESS" in states:
            target = "gap::in-progress"
        else:
            target = "gap::accepted"
        if target not in present:
            remove = [l for l in BACKEND_STATE_LABELS if l in present and l != target]
            self.act(f"backend #{gl_issue['iid']}: label {target}", self.gl.update_issue, gl_issue["iid"],
                     add_labels=target, remove_labels=",".join(remove))
            if target == "gap::contract-published":
                versions = sorted({m.resolution["version"] for m in members if m.resolution})
                self.act(f"backend #{gl_issue['iid']}: publication note", self.gl.add_note, gl_issue["iid"],
                         "The coordinator verified a published contract containing this fix: "
                         + ", ".join(f"`{v}`" for v in versions) + ". Consumers were notified.")

    # ----------------------------------------------------------------- run

    def run(self, only: set[int] | None = None, replay: set[int] | None = None) -> dict:
        self._mrs: dict[int, list] = {}
        self._requests: dict[str, dict] = {}
        self._failures: dict[int, list] = {}
        replay = replay or set()
        issues = self.gh.open_issues()
        for number in sorted((only or set()) | replay):
            if number not in {i["number"] for i in issues}:
                issues.append(self.gh.issue(number))
        if only:
            issues = [i for i in issues if i["number"] in only | replay]
        issues = sorted((i for i in issues if looks_like_gap(i)), key=lambda i: i["number"])
        self.count("requests_seen", len(issues))
        intakes: list[tuple[Intake, dict, list]] = []
        failures = 0
        for issue in issues:
            try:
                comments = self.gh.comments(issue["number"])
                intake = self.evaluate(issue, comments)
            except (ApiError, IntegrityError) as exc:
                failures += 1
                self.count("sync_failures")
                self.log(f"github #{issue['number']}: intake failed: {exc}")
                continue
            if intake.previous.get("state") == "BLOCKED" and intake.previous.get("reason") == "PERMANENT_FAILURE" \
                    and issue["number"] not in replay:
                intake.state, intake.reason = "BLOCKED", "PERMANENT_FAILURE"
                intake.details = ["synchronization failed repeatedly; a maintainer can replay it"]
                intake.error = intake.previous.get("last_error")
                self.count("blocked_permanent")
                intakes.append((intake, issue, comments))
                continue
            intakes.append((intake, issue, comments))

        # Same consumer reporting the same gap twice: later reports are duplicates.
        first_by_consumer: dict[tuple, int] = {}
        for intake, _, _ in intakes:
            if intake.state in ("ACCEPTED", "NEEDS_TRIAGE") and intake.fingerprint:
                key = (intake.fingerprint, intake.request["consumer"]["project"])
                if key in first_by_consumer:
                    intake.state, intake.reason = "DUPLICATE", "SAME_CONSUMER_DUPLICATE"
                    intake.details = [f"already reported by the same consumer in #{first_by_consumer[key]}"]
                else:
                    first_by_consumer[key] = intake.number

        backend_issues: dict[str, tuple[dict, list[Intake]]] = {}
        groups: dict[str, list[Intake]] = {}
        for intake, _, _ in intakes:
            if intake.state == "ACCEPTED":
                groups.setdefault(intake.fingerprint, []).append(intake)

        for fp, members in groups.items():
            primary = members[0]
            # "Already available" only when no backend work is tracked for this gap; once a backend
            # issue exists, only release evidence can mark it published (and all members agree).
            available = next((m.resolution for m in members if m.resolution
                              and m.resolution.get("already_available")), None)
            for member in members:
                member.resolution = None
            try:
                if self.gl is None:
                    self.actions.append(f"DRY-RUN (no backend credential) would create/link backend issue for {fp[:16]}")
                    continue
                if available and not self.gl.find_by_fingerprint(fp):
                    for member in members:
                        member.state, member.reason, member.resolution = \
                            "CONTRACT_PUBLISHED", "ALREADY_AVAILABLE", available
                        member.details = ["no backend work is needed: upgrade your pin explicitly"]
                    continue
                gl_issue = self.ensure_backend_issue(primary, members)
                if gl_issue is None:
                    continue
                self._requests[fp] = primary.request
                state, reason, resolution = self.backend_state(gl_issue, fp)
                backend_issues[fp] = (gl_issue, members)
                for member in members:
                    member.backend = gl_issue["iid"]
                    member.backend_closed = gl_issue.get("state") == "closed"
                    if state != "ACCEPTED" or reason not in ("NO_MR", "NO_MERGED_MR"):
                        member.state, member.reason, member.resolution = state, reason, resolution
                    if state == "REJECTED":
                        member.details = ["the backend team classified this as a consumer-side issue (root cause E)"]
                    elif state == "BLOCKED":
                        member.details = ["an owner/business decision is required before backend work (F/G)"]
                    elif reason == "MERGED_NOT_PUBLISHED":
                        member.details = ["the backend change is merged; no approved contract containing it is "
                                          "published yet"]
                if reason == "MERGED_NOT_PUBLISHED":
                    self._note_check_failures(gl_issue["iid"])
            except (ApiError, IntegrityError) as exc:
                failures += 1
                self.count("sync_failures")
                self.log(f"fingerprint {fp[:16]}: backend sync failed: {exc}")
                for member in members:
                    member.error = str(exc)[:200]
                    member.state = member.previous.get("state") or "VALIDATING"
                    member.reason = member.previous.get("reason") or "SYNC_PENDING"
                    # Bounded: after max_attempts failing runs the request is parked until a replay.
                    attempts = int(member.previous.get("attempts", 0)) + 1
                    if attempts >= self.policy["max_attempts"]:
                        member.state, member.reason = "BLOCKED", "PERMANENT_FAILURE"
                        member.details = ["synchronization failed repeatedly; a maintainer can replay it"]

        # Consumer confirmation, then completion criteria.
        for intake, _, comments in intakes:
            if intake.state == "CONTRACT_PUBLISHED" and intake.error is None:
                try:
                    verified = self.consumer_verified(intake, comments)
                except (ApiError, IntegrityError) as exc:
                    self.log(f"github #{intake.number}: verification check failed: {exc}")
                    verified = False
                if verified:
                    intake.state, intake.reason = "CONSUMER_VERIFIED", "CONSUMER_CONFIRMED"
                    if intake.backend_closed:
                        intake.state, intake.reason = "RESOLVED", "VERIFIED_AND_CLOSED"
                    else:
                        intake.details = ["confirmed by the consumer; waiting for the backend issue to be closed"]
        for gl_issue, members in backend_issues.values():
            try:
                self.sync_backend_labels(gl_issue, members)
            except ApiError as exc:
                failures += 1
                self.count("sync_failures")
                self.log(f"backend #{gl_issue['iid']}: label sync failed: {exc}")

        for intake, issue, _ in intakes:
            self.count(f"state:{intake.state}")
            if self.gh.can_write or self.dry_run:
                try:
                    self.apply(intake, issue)
                except ApiError as exc:
                    failures += 1
                    self.count("sync_failures")
                    self.log(f"github #{intake.number}: write-back failed: {exc}")
        return self.report(intakes, failures)

    def _note_check_failures(self, iid: int) -> None:
        failures = self._failures.get(iid) or []
        digest = hashlib.sha256("\n".join(failures).encode()).hexdigest()[:16]
        key = f"capitalix-gap-check-failure {digest}"
        notes = self.gl.notes(iid)
        if not any(key in (n.get("body") or "") for n in notes):
            self.act(f"backend #{iid}: note failing resolution checks", self.gl.add_note, iid,
                     f"<!-- {key} -->\nThe currently published contract does not (yet) satisfy this gap's resolution checks:\n"
                     + "\n".join(f"- {f}" for f in failures))

    def report(self, intakes: list, failures: int) -> dict:
        now = self.now()
        stale_days = self.policy["stale_after_days"]
        stale = []
        for intake, issue, _ in intakes:
            created = issue.get("created_at")
            if created and intake.state not in ("RESOLVED", "REJECTED", "DUPLICATE"):
                age = (now - datetime.strptime(created, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)).days
                if age >= stale_days:
                    stale.append({"issue": intake.number, "age_days": age, "state": intake.state})
        states = {s: self.counters.get(f"state:{s}", 0) for s in STATES}
        return {
            "schema": "capitalix.api-gap-report.v1",
            "generated_at": core.utc_now(),
            "dry_run": self.dry_run,
            "summary": {
                "requests_received": self.counters.get("requests_seen", 0),
                "invalid": sum(1 for i, _, _ in intakes if i.reason in ("INVALID_REQUEST", "SENSITIVE_DATA",
                                                                         "UNKNOWN_CONTRACT_VERSION",
                                                                         "CONTRACT_SHA_MISMATCH")),
                "duplicates": states["DUPLICATE"],
                "awaiting_triage": states["NEEDS_TRIAGE"],
                "backend_issues_created": self.counters.get("backend_issues_created", 0),
                "backend_in_progress": states["IN_PROGRESS"],
                "merge_requests_open": sum(1 for mrs in self._mrs.values() for mr in mrs if mr.get("state") == "opened"),
                "published_resolutions": states["CONTRACT_PUBLISHED"],
                "consumer_verified": states["CONSUMER_VERIFIED"] + states["RESOLVED"],
                "failed_synchronizations": failures,
                "stale_unresolved": len(stale),
            },
            "states": states,
            "requests": [{"issue": i.number, "state": i.state, "reason": i.reason,
                          "fingerprint": (i.fingerprint or "")[:16] or None, "backend": i.backend,
                          "sensitive": i.sensitive, "error": i.error} for i, _, _ in intakes],
            "stale": stale,
            "actions": self.actions,
        }


def parse_resolution(raw: bytes, fingerprint: str, iid: int) -> tuple[dict | None, str | None]:
    try:
        evidence = json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None, "not JSON"
    if not isinstance(evidence, dict) or evidence.get("schema") != RESOLUTION_SCHEMA:
        return None, "unsupported schema"
    if evidence.get("fingerprint") != fingerprint or evidence.get("backend_issue") != iid:
        return None, "fingerprint or issue mismatch"
    cause = evidence.get("root_cause")
    if cause not in ("A", "B", "C", "D"):
        return None, "root cause must be A-D (E/F/G use triage labels)"
    checks, tests = evidence.get("checks", []), evidence.get("tests", [])
    if not isinstance(checks, list) or not isinstance(tests, list):
        return None, "checks/tests must be lists"
    if cause in ("A", "B", "D") and not checks:
        return None, "A/B/D need at least one contract check"
    if cause == "C" and not tests:
        return None, "C needs the backend tests proving the behavior"
    if not isinstance(evidence.get("summary", ""), str) or len(evidence.get("summary", "")) > 500:
        return None, "summary must be a string of at most 500 characters"
    return evidence, None


def render_markdown(report: dict) -> str:
    s = report["summary"]
    lines = ["# API gap coordinator report", "", f"Generated {report['generated_at']}"
             + (" (dry run: nothing changed)" if report["dry_run"] else ""), "",
             "| Metric | Count |", "|---|---|", *[f"| {k.replace('_', ' ')} | {v} |" for k, v in s.items()], "",
             "| Issue | State | Reason | Fingerprint | Backend |", "|---|---|---|---|---|"]
    lines += [f"| #{r['issue']} | {r['state']} | {r['reason']} | {r['fingerprint'] or '–'} | "
              f"{('BE-' + str(r['backend'])) if r['backend'] else '–'} |" for r in report["requests"]]
    if report["stale"]:
        lines += ["", "## Unresolved for too long", *[f"- #{x['issue']}: {x['state']} for {x['age_days']} days"
                                                     for x in report["stale"]]]
    if report["actions"]:
        lines += ["", "## Actions", *[f"- {a}" for a in report["actions"]]]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Capitalix API gap coordinator")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("sync", "ensure-labels"):
        p = sub.add_parser(name)
        p.add_argument("--policy", default=str(HERE / "policy.json"))
        p.add_argument("--lock-file", default=os.environ.get("API_GAP_LOCK_FILE", "/tmp/capitalix-api-gap.lock"))
    sync = sub.choices["sync"]
    sync.add_argument("--dry-run", action="store_true", help="read only: report the actions without taking them")
    sync.add_argument("--issue", type=int, action="append", default=[], help="only these GitHub issues")
    sync.add_argument("--replay", type=int, action="append", default=[],
                      help="re-process these issues even after a permanent failure")
    sync.add_argument("--report-json")
    sync.add_argument("--report-md")
    args = parser.parse_args(argv)
    try:
        policy = load_policy(Path(args.policy))
    except (OSError, ValueError) as exc:
        print(f"ERROR: policy: {exc}", file=sys.stderr)
        return 3
    github_token = os.environ.get("API_GAP_GITHUB_TOKEN") or None
    backend_token = os.environ.get("API_GAP_BACKEND_TOKEN") or None
    dry_run = getattr(args, "dry_run", False)
    if not dry_run and not (github_token and backend_token):
        print("ERROR: API_GAP_GITHUB_TOKEN and API_GAP_BACKEND_TOKEN are required (or use --dry-run)",
              file=sys.stderr)
        return 3
    lock = open(args.lock_file, "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print("another coordinator run holds the lock; nothing done", file=sys.stderr)
        return 4
    github = GitHub(policy["github_repository"], github_token)
    backend = GitHubBackend(policy["backend_repository"], backend_token) if backend_token else None
    try:
        if args.command == "ensure-labels":
            github.ensure_labels()
            backend.ensure_labels()
            print("labels ensured")
            return 0
        if not dry_run:
            viewer = github.viewer()
            if viewer != policy["coordinator_github_login"]:
                print("ERROR: the GitHub credential does not belong to the configured coordinator login",
                      file=sys.stderr)
                return 3
            github.ensure_labels()
            backend.ensure_labels()
        coordinator = Coordinator(policy, github, backend, PublishedContracts(policy["contract_source"]),
                                  dry_run=dry_run, log=lambda m: print(m, file=sys.stderr))
        report = coordinator.run(set(args.issue) or None, set(args.replay))
    except (ApiError, IntegrityError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    for path, text in ((args.report_json, json.dumps(report, indent=2) + "\n"),
                       (args.report_md, render_markdown(report))):
        if path:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            Path(path).write_text(text, encoding="utf-8")
    print(json.dumps(report["summary"], sort_keys=True))
    return 1 if report["summary"]["failed_synchronizations"] else 0


if __name__ == "__main__":
    sys.exit(main())
