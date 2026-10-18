#!/usr/bin/env python3
"""capitalix-contract: pin, verify, and query the approved Capitalix API contract.

Stdlib only (Python >= 3.9). Copy this file into a consumer project, then:

  python3 capitalix_contract.py init              pin the current approved contract
  python3 capitalix_contract.py status            pinned version, integrity, newer version?
  python3 capitalix_contract.py verify            local digest check (add --remote for provenance)
  python3 capitalix_contract.py list owner/sales  compact operation index (filter optional)
  python3 capitalix_contract.py inspect customers operations + resolved schemas for a feature
  python3 capitalix_contract.py check lib/        API paths used in code exist in the contract?
  python3 capitalix_contract.py update            move the pin to the newest approved version
  python3 capitalix_contract.py validate traffic.json  recorded requests/responses conform?
  python3 capitalix_contract.py sample OPERATION_ID   example response from the contract schema
  python3 capitalix_contract.py sync              restore pinned files from contract.lock
  python3 capitalix_contract.py gap BACKEND_API.md  requirements-to-contract gap report

Pinned files live in .capitalix-contract/ (override with --dir):
  openapi.json   the exact approved contract bytes
  manifest.json  version, digest, source commit, approval evidence
  contract.lock  what is pinned, and the digests that must match

Sources:
  github:OWNER/REPO[@REF]  GitHub contents API; uses $GITHUB_TOKEN, else the `gh` CLI login
  file:/path/to/checkout   a local shared-docs checkout (offline / mirrors / tests)

Exit codes: 0 ok; 1 check failed (digest mismatch, unknown paths, outdated with
--fail-if-outdated); 2 source unreachable; 3 usage or input error.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

TOOL_VERSION = "1.0.0"
DEFAULT_SOURCE = "github:abdo-taher/project-shared-docs"
DEFAULT_DIR = ".capitalix-contract"
PUBLISHED_ROOT = "api/implemented"
METHODS = ("get", "post", "put", "patch", "delete", "head", "options")


class SourceError(Exception):
    """The contract source could not be reached or returned unusable data."""


class CheckFailed(Exception):
    """An integrity or contract check failed."""


# --------------------------------------------------------------------------- sources

def fetch(source: str, path: str) -> bytes:
    """Return the bytes of a published file, relative to the shared-docs root."""
    if source.startswith("file:"):
        target = Path(source[5:]) / path
        try:
            return target.read_bytes()
        except OSError as exc:
            raise SourceError(f"cannot read {target}: {exc}") from exc
    if not source.startswith("github:"):
        raise SourceError(f"unsupported source [{source}] (use github:OWNER/REPO or file:PATH)")
    spec = source[7:]
    repo, _, ref = spec.partition("@")
    api_path = f"repos/{repo}/contents/{path}" + (f"?ref={ref}" if ref else "")
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        request = urllib.request.Request(
            f"https://api.github.com/{api_path}",
            headers={"Accept": "application/vnd.github.raw+json",
                     "Authorization": f"Bearer {token}",
                     "User-Agent": f"capitalix-contract/{TOOL_VERSION}"})
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            raise SourceError(f"GitHub returned HTTP {exc.code} for {path} "
                              "(check that the token can read the repository)") from exc
        except urllib.error.URLError as exc:
            raise SourceError(f"cannot reach GitHub: {exc.reason}") from exc
    if shutil.which("gh"):
        result = subprocess.run(
            ["gh", "api", "-H", "Accept: application/vnd.github.raw+json", api_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return result.stdout
        raise SourceError(f"gh api failed for {path}: {result.stderr.decode().strip()}")
    raise SourceError("no GitHub credentials: set GITHUB_TOKEN or run `gh auth login`")


def fetch_json(source: str, path: str) -> dict:
    try:
        return json.loads(fetch(source, path))
    except json.JSONDecodeError as exc:
        raise SourceError(f"{path} is not valid JSON: {exc}") from exc


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def resolve_version(source: str, version: str) -> tuple[dict, bytes, bytes]:
    """Fetch and cross-check manifest + contract for a version ('current' allowed)."""
    if version == "current":
        pointer = fetch_json(source, f"{PUBLISHED_ROOT}/current.json")
        version = pointer["version"]
        expected = pointer["sha256"]
    else:
        index = fetch_json(source, f"{PUBLISHED_ROOT}/index.json")
        entry = next((v for v in index.get("versions", []) if v["version"] == version), None)
        if entry is None:
            raise CheckFailed(f"version [{version}] is not published")
        expected = entry["sha256"]
    manifest_bytes = fetch(source, f"{PUBLISHED_ROOT}/versions/{version}/manifest.json")
    manifest = json.loads(manifest_bytes)
    contract = fetch(source, f"{PUBLISHED_ROOT}/versions/{version}/openapi.json")
    digest = sha256(contract)
    if manifest.get("version") != version or manifest.get("sha256") != expected:
        raise CheckFailed(f"manifest for {version} does not match the published index/pointer")
    if digest != expected:
        raise CheckFailed(f"downloaded contract digest {digest} does not match the "
                          f"published digest {expected} for {version}")
    return manifest, manifest_bytes, contract


# --------------------------------------------------------------------------- pin files

def pin_dir(args) -> Path:
    return Path(args.dir)


def read_lock(directory: Path) -> dict:
    lock_path = directory / "contract.lock"
    if not lock_path.is_file():
        raise CheckFailed(f"no pinned contract: {lock_path} is missing — run `init` first")
    return json.loads(lock_path.read_text(encoding="utf-8"))


def write_pin(directory: Path, source: str, manifest: dict, manifest_bytes: bytes,
              contract: bytes) -> dict:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "openapi.json").write_bytes(contract)
    (directory / "manifest.json").write_bytes(manifest_bytes)
    lock = {
        "schema": "capitalix-contract-lock/1",
        "source": source,
        "version": manifest["version"],
        "sha256": manifest["sha256"],
        "manifest_sha256": sha256(manifest_bytes),
        "source_repository": manifest.get("source", {}).get("repository"),
        "source_commit": manifest.get("source", {}).get("commit"),
        "operations": manifest.get("operations"),
        "tool_version": TOOL_VERSION,
    }
    (directory / "contract.lock").write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
    return lock


def verify_local(directory: Path) -> dict:
    lock = read_lock(directory)
    contract_path = directory / "openapi.json"
    manifest_path = directory / "manifest.json"
    if not contract_path.is_file() or not manifest_path.is_file():
        raise CheckFailed(f"pinned files are missing in {directory}")
    if sha256(contract_path.read_bytes()) != lock["sha256"]:
        raise CheckFailed("openapi.json does not match the digest in contract.lock "
                          "(edited or corrupted) — never edit the pinned contract")
    if sha256(manifest_path.read_bytes()) != lock["manifest_sha256"]:
        raise CheckFailed("manifest.json does not match contract.lock")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("sha256") != lock["sha256"] or manifest.get("version") != lock["version"]:
        raise CheckFailed("manifest.json describes a different version than contract.lock")
    return lock


def load_contract(directory: Path) -> dict:
    verify_local(directory)
    return json.loads((directory / "openapi.json").read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- contract model

def operations(document: dict):
    for path, item in document.get("paths", {}).items():
        for method in METHODS:
            if method in item:
                yield method.upper(), path, item[method], item


def ref_target(document: dict, ref: str) -> Any:
    node: Any = document
    for part in ref.lstrip("#/").split("/"):
        node = node[part.replace("~1", "/").replace("~0", "~")]
    return node


def deref(document: dict, node: Any) -> Any:
    """Follow top-level $ref pointers only; nested refs stay real JSON pointers."""
    seen = set()
    while isinstance(node, dict) and str(node.get("$ref", "")).startswith("#/") and node["$ref"] not in seen:
        seen.add(node["$ref"])
        node = ref_target(document, node["$ref"])
    return node


def resolve(document: dict, node: Any, depth: int, seen: tuple = ()) -> Any:
    """Inline $refs up to depth; cycles and the depth limit become {'$ref': Name}."""
    if isinstance(node, dict):
        if "$ref" in node:
            ref = node["$ref"]
            name = ref.rsplit("/", 1)[-1]
            if ref in seen or depth <= 0:
                return {"$ref": name}
            return {"$ref": name, **resolve(document, ref_target(document, ref),
                                            depth - 1, seen + (ref,))}
        return {k: resolve(document, v, depth, seen) for k, v in node.items()}
    if isinstance(node, list):
        return [resolve(document, v, depth, seen) for v in node]
    return node


def path_regex(template: str) -> re.Pattern:
    parts = re.split(r"(\{[^}]+\})", template)
    body = "".join("[^/]+" if p.startswith("{") else re.escape(p) for p in parts)
    return re.compile(f"^{body}/?$")


def normalize_template(path: str) -> str:
    return re.sub(r"\{[^}]+\}", "{}", "/" + path.strip().strip("/"))


def matches(query_terms: list[str], method: str, path: str, op: dict) -> bool:
    haystack = " ".join([method, path, op.get("operationId", ""), op.get("summary", ""),
                         " ".join(op.get("tags", []))]).lower()
    return all(term.lower() in haystack for term in query_terms)


def describe(document: dict, method: str, path: str, op: dict, item: dict, depth: int) -> dict:
    params = [resolve(document, p, depth) for p in item.get("parameters", []) + op.get("parameters", [])]
    entry = {
        "method": method,
        "path": path,
        "operationId": op.get("operationId"),
        "tags": op.get("tags", []),
        "deprecated": bool(op.get("deprecated")),
        "security": op.get("security", document.get("security", [])),
        "access": op.get("x-access"),
        "parameters": [
            {k: p.get(k) for k in ("name", "in", "required", "schema", "description") if k in p}
            for p in params],
    }
    if "requestBody" in op:
        entry["requestBody"] = resolve(document, op["requestBody"], depth)
    entry["responses"] = {status: resolve(document, response, depth)
                          for status, response in op.get("responses", {}).items()}
    return entry


# --------------------------------------------------------------------------- commands

def cmd_init(args) -> int:
    directory = pin_dir(args)
    if (directory / "contract.lock").exists() and not args.force:
        print(f"{directory}/contract.lock already exists — use `update` to change the pin",
              file=sys.stderr)
        return 3
    manifest, manifest_bytes, contract = resolve_version(args.source, args.version)
    lock = write_pin(directory, args.source, manifest, manifest_bytes, contract)
    print(f"pinned Capitalix contract {lock['version']}")
    print(f"  sha256        {lock['sha256']}")
    print(f"  source commit {lock['source_repository']}@{lock['source_commit']}")
    print(f"  operations    {lock['operations']}")
    print(f"  files         {directory}/openapi.json, manifest.json, contract.lock")
    print("commit these files; agents and tests read the pinned copy, not the network")
    return 0


def cmd_verify(args) -> int:
    lock = verify_local(pin_dir(args))
    print(f"local pin OK: {lock['version']} sha256 {lock['sha256']}")
    if args.remote:
        manifest, _, _ = resolve_version(lock["source"], lock["version"])
        if manifest["sha256"] != lock["sha256"]:
            raise CheckFailed("the published manifest for the pinned version has a different digest")
        print(f"published manifest OK: {manifest['version']} from "
              f"{manifest['source']['repository']}@{manifest['source']['commit']}, "
              f"approved by {manifest['approval']['approved_by']} "
              f"({manifest['approval']['trusted_approval_id']})")
    return 0


def cmd_verify_remote(args) -> int:
    manifest, _, contract = resolve_version(args.source, args.version)
    if args.expect_sha256 and sha256(contract) != args.expect_sha256:
        raise CheckFailed(f"published {manifest['version']} has sha256 {sha256(contract)}, "
                          f"expected {args.expect_sha256}")
    print(f"published contract OK: {manifest['version']} sha256 {manifest['sha256']} "
          f"source {manifest['source']['repository']}@{manifest['source']['commit']}")
    return 0


def cmd_status(args) -> int:
    lock = verify_local(pin_dir(args))
    print(f"pinned   {lock['version']}  sha256 {lock['sha256'][:16]}…  "
          f"source {lock['source_repository']}@{(lock['source_commit'] or '')[:12]}")
    print("integrity OK (openapi.json and manifest.json match contract.lock)")
    try:
        pointer = fetch_json(lock["source"], f"{PUBLISHED_ROOT}/current.json")
    except SourceError as exc:
        print(f"latest   unknown — source unreachable ({exc}); the pinned contract still works offline")
        return 0
    if pointer["sha256"] == lock["sha256"]:
        print(f"latest   {pointer['version']} — up to date")
        return 0
    index = fetch_json(lock["source"], f"{PUBLISHED_ROOT}/index.json")
    newer = [v for v in index.get("versions", [])
             if v["source_commit_date"] > next((x["source_commit_date"] for x in index["versions"]
                                                if x["version"] == lock["version"]), "")]
    print(f"latest   {pointer['version']} — {len(newer)} newer approved version(s):")
    for entry in newer:
        c = entry.get("compatibility", {})
        print(f"  {entry['version']}  breaking={c.get('BREAKING', '?')} unknown={c.get('UNKNOWN', '?')} "
              f"non_breaking={c.get('NON_BREAKING', '?')}")
    print("run `update` deliberately (not during unrelated feature work) to move the pin")
    return 1 if args.fail_if_outdated else 0


def cmd_update(args) -> int:
    directory = pin_dir(args)
    old = verify_local(directory)
    old_doc = json.loads((directory / "openapi.json").read_text(encoding="utf-8"))
    manifest, manifest_bytes, contract = resolve_version(old["source"], args.version)
    if manifest["sha256"] == old["sha256"]:
        print(f"already pinned to {old['version']}")
        return 0
    new_doc = json.loads(contract)
    before = {(m, p) for m, p, _, _ in operations(old_doc)}
    after = {(m, p) for m, p, _, _ in operations(new_doc)}
    lock = write_pin(directory, old["source"], manifest, manifest_bytes, contract)
    print(f"updated pin {old['version']} -> {lock['version']}")
    print(f"  compatibility vs its approved baseline: {manifest.get('compatibility')}")
    print(f"  operations added {len(after - before)}, removed {len(before - after)}")
    for method, path in sorted(before - after):
        print(f"  REMOVED {method} {path}")
    for method, path in sorted(after - before)[:50]:
        print(f"  added   {method} {path}")
    print("review the changes, run your tests and `check`, then commit the new pin")
    return 0


def cmd_list(args) -> int:
    document = load_contract(pin_dir(args))
    count = 0
    for method, path, op, _ in operations(document):
        if args.filter and not matches(args.filter, method, path, op):
            continue
        if not args.include_deprecated and op.get("deprecated"):
            continue
        count += 1
        print(f"{method:6} {path}  [{op.get('operationId', '-')}]")
    print(f"{count} operation(s)", file=sys.stderr)
    return 0


def cmd_inspect(args) -> int:
    directory = pin_dir(args)
    lock = verify_local(directory)
    document = load_contract(directory)
    found = []
    for method, path, op, item in operations(document):
        if args.method and method != args.method.upper():
            continue
        if not args.include_deprecated and op.get("deprecated"):
            continue
        if matches(args.query, method, path, op):
            found.append(describe(document, method, path, op, item, args.depth))
    if len(found) > args.limit:
        print(f"{len(found)} operations match {args.query!r}; showing {args.limit}. "
              "Narrow the query (more terms, --method) or raise --limit.", file=sys.stderr)
        found = found[:args.limit]
    result = {"contract": {"version": lock["version"], "sha256": lock["sha256"]},
              "query": args.query, "operations": found}
    print(json.dumps(result, indent=1, ensure_ascii=False))
    if not found:
        print(f"no operation matches {args.query!r} in contract {lock['version']} — "
              "do not invent one; report it as missing", file=sys.stderr)
        return 1
    return 0


PATH_LITERAL = re.compile(r"""["'`](/?(?:api/)?[a-z][a-z0-9_\-]*(?:/[A-Za-z0-9_\-{}$:.]+)+)/?["'`]""")


def cmd_check(args) -> int:
    document = load_contract(pin_dir(args))
    templates = [(path_regex(p), p) for p in document.get("paths", {})]
    prefix = "/" + args.prefix.strip("/") if args.prefix else ""
    unknown, known = [], 0
    files = []
    for target in args.paths:
        root = Path(target)
        files += [root] if root.is_file() else sorted(
            p for p in root.rglob("*") if p.suffix in tuple(args.ext.split(",")))
    for file in files:
        text = file.read_text(encoding="utf-8", errors="replace")
        for number, line in enumerate(text.splitlines(), 1):
            for literal in PATH_LITERAL.findall(line):
                if literal.lstrip("/").startswith("api/"):
                    candidate = "/" + literal.lstrip("/")
                elif prefix:
                    candidate = f"{prefix}/{literal.lstrip('/')}"
                else:
                    continue  # not an API path (e.g. an asset); relative paths need --prefix
                # String interpolation ($id, ${id}, :id) stands in for a path parameter.
                candidate = re.sub(r"\$\{[^}]+\}|\$[A-Za-z_]\w*|:[A-Za-z_]\w*", "x", candidate)
                if any(rx.match(candidate) for rx, _ in templates):
                    known += 1
                else:
                    unknown.append(f"{file}:{number}: {literal}")
    print(f"{known} API path literal(s) match the pinned contract")
    for entry in unknown:
        print(f"NOT IN CONTRACT  {entry}")
    if unknown:
        print(f"{len(unknown)} path(s) are not in the pinned contract — they are undocumented "
              "or wrong; do not ship them without a contract change", file=sys.stderr)
        return 1
    return 0


# --------------------------------------------------------------------------- validation

JSON_TYPES = {"object": dict, "array": list, "string": str, "boolean": bool, "null": type(None)}


def type_ok(expected: str, value: Any) -> bool:
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return isinstance(value, JSON_TYPES.get(expected, object))


def validate_schema(document: dict, schema: Any, value: Any, where: str, depth: int = 0) -> list[str]:
    """A pragmatic JSON Schema (2020-12 subset) validator for OpenAPI 3.1 payloads."""
    if not isinstance(schema, dict) or depth > 64:
        return []
    if "$ref" in schema:
        return validate_schema(document, ref_target(document, schema["$ref"]), value, where, depth + 1)
    errors: list[str] = []
    for sub in schema.get("allOf", []):
        errors += validate_schema(document, sub, value, where, depth + 1)
    for keyword in ("anyOf", "oneOf"):
        if keyword in schema:
            branches = [validate_schema(document, sub, value, where, depth + 1) for sub in schema[keyword]]
            if all(branches):
                closest = min(branches, key=len)
                errors.append(f"{where}: matches none of the {keyword} alternatives; closest "
                              f"(#{branches.index(closest) + 1}) fails on: " + "; ".join(closest[:4]))
    expected = schema.get("type")
    if expected is not None:
        options = expected if isinstance(expected, list) else [expected]
        if not any(type_ok(t, value) for t in options):
            return errors + [f"{where}: expected {'|'.join(options)}, got {type(value).__name__}"]
    if "const" in schema and value != schema["const"]:
        errors.append(f"{where}: expected constant {schema['const']!r}, got {value!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{where}: {value!r} is not one of {schema['enum']}")
    if isinstance(value, str):
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(f"{where}: longer than {schema['maxLength']}")
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{where}: shorter than {schema['minLength']}")
        if "pattern" in schema:
            try:
                if not re.search(schema["pattern"], value):
                    errors.append(f"{where}: does not match pattern {schema['pattern']}")
            except re.error:
                pass
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{where}: below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{where}: above maximum {schema['maximum']}")
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for name in schema.get("required", []):
            if name not in value:
                errors.append(f"{where}: missing required property `{name}`")
        for name, item in value.items():
            if name in properties:
                errors += validate_schema(document, properties[name], item, f"{where}.{name}", depth + 1)
            elif schema.get("additionalProperties") is False:
                errors.append(f"{where}: property `{name}` is not allowed by the contract")
            elif isinstance(schema.get("additionalProperties"), dict):
                errors += validate_schema(document, schema["additionalProperties"], item,
                                          f"{where}.{name}", depth + 1)
    if isinstance(value, list) and "items" in schema:
        for i, item in enumerate(value):
            errors += validate_schema(document, schema["items"], item, f"{where}[{i}]", depth + 1)
    return errors


def find_operation(document: dict, method: str, concrete_path: str):
    path_only = concrete_path.split("?")[0]
    candidates = []
    for template, item in document.get("paths", {}).items():
        if method.lower() in item and path_regex(template).match(path_only):
            static = len(re.sub(r"\{[^}]+\}", "", template))
            candidates.append((static, template, item[method.lower()], item))
    if not candidates:
        return None
    _, template, op, item = max(candidates)
    return template, op, item


def json_body_schema(container: dict) -> Any:
    content = container.get("content", {})
    media = content.get("application/json") or next(iter(content.values()), None)
    return (media or {}).get("schema")


def validate_exchange(document: dict, entry: dict) -> list[str]:
    method = entry["method"].upper()
    found = find_operation(document, method, entry["path"])
    if not found:
        return [f"{method} {entry['path']}: no such operation in the contract"]
    template, op, item = found
    label = f"{method} {template} [{op.get('operationId')}]"
    errors = []
    params = [deref(document, p) for p in item.get("parameters", []) + op.get("parameters", [])]
    query = {p["name"]: p for p in params if p.get("in") == "query"}
    for name, value in (entry.get("query") or {}).items():
        if name not in query:
            errors.append(f"{label}: query parameter `{name}` is not in the contract")
            continue
        schema = deref(document, query[name].get("schema", {}))
        coerced = value
        types = schema.get("type") if isinstance(schema.get("type"), list) else [schema.get("type")]
        if "integer" in types and isinstance(value, str) and value.isdigit():
            coerced = int(value)
        errors += validate_schema(document, schema, coerced, f"{label} query.{name}")
    for name, param in query.items():
        if param.get("required") and name not in (entry.get("query") or {}):
            errors.append(f"{label}: required query parameter `{name}` was not sent")
    if "requestBody" in op:
        body_schema = json_body_schema(deref(document, op["requestBody"]))
        if entry.get("body") is None:
            if op["requestBody"].get("required"):
                errors.append(f"{label}: request body is required")
        elif body_schema:
            errors += validate_schema(document, body_schema, entry["body"], f"{label} body")
    elif entry.get("body") not in (None, {}):
        errors.append(f"{label}: the contract defines no request body")
    if "status" in entry:
        status = str(entry["status"])
        responses = op.get("responses", {})
        response = responses.get(status) or responses.get(status[0] + "XX") or responses.get("default")
        if response is None:
            errors.append(f"{label}: response status {status} is not in the contract "
                          f"(documented: {', '.join(responses)})")
        elif "response" in entry:
            schema = json_body_schema(deref(document, response))
            if schema:
                errors += validate_schema(document, schema, entry["response"], f"{label} {status} response")
    return errors


def cmd_validate(args) -> int:
    lock = verify_local(pin_dir(args))
    document = load_contract(pin_dir(args))
    traffic = json.loads(Path(args.traffic).read_text(encoding="utf-8"))
    entries = traffic if isinstance(traffic, list) else traffic.get("exchanges", [])
    failures = 0
    for entry in entries:
        errors = validate_exchange(document, entry)
        tag = f"{entry['method'].upper()} {entry['path']} -> {entry.get('status', '-')}"
        if errors:
            failures += 1
            print(f"FAIL  {tag}")
            for error in errors[: args.max_errors]:
                print(f"      {error}")
        else:
            print(f"ok    {tag}")
    print(f"{len(entries) - failures}/{len(entries)} exchange(s) conform to contract {lock['version']}")
    return 1 if failures else 0


def sample_value(document: dict, schema: Any, depth: int = 0) -> Any:
    if not isinstance(schema, dict) or depth > 12:
        return None
    if "$ref" in schema:
        return sample_value(document, ref_target(document, schema["$ref"]), depth + 1)
    if "const" in schema:
        return schema["const"]
    if schema.get("examples"):
        return schema["examples"][0]
    if "example" in schema:
        return schema["example"]
    if "enum" in schema:
        return next((v for v in schema["enum"] if v is not None), None)
    if "allOf" in schema:
        merged: dict = {}
        for sub in schema["allOf"]:
            part = sample_value(document, sub, depth + 1)
            if isinstance(part, dict):
                for key, value in part.items():
                    if isinstance(value, dict) and isinstance(merged.get(key), dict) and value == {}:
                        continue
                    merged[key] = value
        return merged
    for keyword in ("oneOf", "anyOf"):
        if keyword in schema:
            return sample_value(document, schema[keyword][0], depth + 1)
    kind = schema.get("type")
    if isinstance(kind, list):
        kind = next((t for t in kind if t != "null"), "null")
    if kind == "object" or "properties" in schema:
        return {name: sample_value(document, sub, depth + 1)
                for name, sub in schema.get("properties", {}).items()}
    if kind == "array":
        return [sample_value(document, schema.get("items", {}), depth + 1)]
    if kind == "integer":
        return max(1, schema.get("minimum", 1))
    if kind == "number":
        return 1.5
    if kind == "boolean":
        return True
    if kind == "string":
        return {"date-time": "2026-01-01T00:00:00Z", "date": "2026-01-01",
                "email": "user@example.com", "uuid": "00000000-0000-4000-8000-000000000000"}.get(
            schema.get("format"), "string")
    return None


def cmd_sample(args) -> int:
    document = load_contract(pin_dir(args))
    for method, path, op, _ in operations(document):
        if op.get("operationId") == args.operation_id:
            response = op.get("responses", {}).get(args.status)
            if response is None:
                print(f"{args.operation_id} documents no {args.status} response "
                      f"(documented: {', '.join(op.get('responses', {}))})", file=sys.stderr)
                return 1
            schema = json_body_schema(deref(document, response)) or {}
            print(json.dumps(sample_value(document, schema), indent=1, ensure_ascii=False))
            return 0
    print(f"operation {args.operation_id} is not in the pinned contract", file=sys.stderr)
    return 1


def cmd_sync(args) -> int:
    """Restore the pinned files (e.g. a fresh clone that does not commit openapi.json)."""
    directory = pin_dir(args)
    lock = read_lock(directory)
    try:
        verify_local(directory)
        print(f"pinned files already present and verified: {lock['version']}")
        return 0
    except CheckFailed:
        pass
    manifest, manifest_bytes, contract = resolve_version(lock["source"], lock["version"])
    if manifest["sha256"] != lock["sha256"] or sha256(manifest_bytes) != lock["manifest_sha256"]:
        raise CheckFailed("the published files for the pinned version do not match contract.lock")
    (directory / "openapi.json").write_bytes(contract)
    (directory / "manifest.json").write_bytes(manifest_bytes)
    verify_local(directory)
    print(f"restored pinned contract {lock['version']} (sha256 verified)")
    return 0


# --------------------------------------------------------------------------- gap report

ROW = re.compile(r"^\|(.+)\|\s*$")


def parse_requirements(text: str) -> list[dict]:
    """Parse markdown tables with Name / Method / path columns under '## N. Title'."""
    requirements, section, header = [], "", None
    for number, line in enumerate(text.splitlines(), 1):
        heading = re.match(r"^##\s+(\d+)\.\s+(.*)", line)
        if heading:
            section, header = f"{heading.group(1)}. {heading.group(2).strip()}", None
            continue
        row = ROW.match(line)
        if not row:
            header = None
            continue
        cells = [c.strip() for c in row.group(1).split("|")]
        lowered = [c.lower() for c in cells]
        if "method" in lowered and any("path" in c for c in lowered):
            header = {"name": next((i for i, c in enumerate(lowered) if c.startswith("name")), None),
                      "method": lowered.index("method"),
                      "path": next(i for i, c in enumerate(lowered) if "path" in c),
                      "params": next((i for i, c in enumerate(lowered) if "param" in c or "body" in c), None),
                      "response": next((i for i, c in enumerate(lowered) if "response" in c), None)}
            continue
        if header is None or set(line.replace("|", "").strip()) <= set("-: "):
            continue
        get = lambda key: cells[header[key]] if header[key] is not None and header[key] < len(cells) else ""
        method_cell = get("method").upper().split()
        requirements.append({
            "section": section,
            "line": number,
            "name": get("name").strip("`") or get("path").strip("`"),
            "method": method_cell[0] if method_cell else "",
            "path": get("path").strip("`").strip(),
            "params": get("params"),
            "response": get("response"),
        })
    return requirements


def field_names(text: str) -> set[str]:
    """Identifiers named inside backtick spans; parenthesised enum values are ignored."""
    names = set()
    for span in re.findall(r"`([^`]+)`", re.sub(r"\([^)]*\)", "", text)):
        names |= set(re.findall(r"\b([a-z][a-z0-9_]*)\b", span))
    return names - {"true", "false", "null"}


def contract_fields(document: dict, method: str, op: dict, item: dict) -> set[str]:
    names = {resolve(document, p, 1).get("name") for p in item.get("parameters", []) + op.get("parameters", [])}
    body = op.get("requestBody", {}).get("content", {})
    for media in body.values():
        schema = resolve(document, media.get("schema", {}), 2)
        names |= set(schema.get("properties", {}))
    return {n for n in names if n}


def contract_required(document: dict, op: dict, item: dict) -> set[str]:
    """Required query/body inputs (path parameters and headers excluded)."""
    names = set()
    for raw in item.get("parameters", []) + op.get("parameters", []):
        param = resolve(document, raw, 1)
        if param.get("required") and param.get("in") in ("query", "cookie"):
            names.add(param.get("name"))
    for media in op.get("requestBody", {}).get("content", {}).values():
        names |= set(resolve(document, media.get("schema", {}), 2).get("required", []))
    return {n for n in names if n}


def build_gap(document: dict, requirements: list[dict], mapping: dict,
              bindings: dict | None = None) -> list[dict]:
    index = {}
    by_id = {}
    for method, path, op, item in operations(document):
        index.setdefault(normalize_template(path), {})[method] = (path, op, item)
        if op.get("operationId"):
            by_id[op["operationId"]] = (method, path, op, item)
    results = []
    for req in requirements:
        out = {**req, "status": "", "operation": None, "notes": []}
        reviewed = mapping.get(req["name"])
        if reviewed:
            out["status"] = reviewed.get("status", "MAPPED_REVIEWED")
            op_id = reviewed.get("operationId")
            if op_id and op_id in by_id:
                method, path, _, _ = by_id[op_id]
                out["operation"] = f"{method} {path} [{op_id}]"
            elif op_id:
                out["status"] = "MAPPING_STALE"
                out["notes"].append(f"reviewed operation {op_id} is not in this contract")
            out["notes"] += reviewed.get("notes", [])
            results.append(out)
            continue
        if bindings is not None and req["name"] in bindings and bindings[req["name"]] is None:
            out["status"] = "NOT_BOUND_BY_BACKEND"
            out["notes"].append("the backend conformance bindings record no route for this endpoint")
            results.append(out)
            continue
        binding = (bindings or {}).get(req["name"])
        if binding:
            method, _, route = binding["route"].partition(" ")
            template = "/" + route.lstrip("/")
            found = index.get(normalize_template(template), {}).get(method.upper())
            if found:
                path, op, item = found
                out["status"] = "MAPPED_BY_BACKEND_BINDING"
                out["operation"] = f"{method.upper()} {path} [{op.get('operationId')}]"
                sent = set(binding.get("query") or {}) | set(binding.get("body") or {})
                unknown = sorted(sent - contract_fields(document, method.upper(), op, item))
                unsent = sorted(contract_required(document, op, item) - sent)
                if unsent:
                    out["notes"].append("contract marks required but the backend binding does not send: "
                                        + ", ".join(unsent) + " (the contract's required list is wrong, "
                                        "or the binding is incomplete)")
                if unknown:
                    out["notes"].append("backend binding sends fields this contract does not document: "
                                        + ", ".join(unknown) + " (undocumented aliases, or the binding "
                                        "targets newer development code — confirm with the backend)")
                if method.upper() != req["method"] or normalize_template(req["path"]) not in normalize_template(path):
                    out["notes"].append(f"the app must call {method.upper()} {path} "
                                        f"(requirement suggested {req['method']} {req['path']})")
            else:
                out["status"] = "BOUND_BUT_NOT_IN_CONTRACT"
                out["notes"].append(f"backend binding names {binding['route']}, which this contract "
                                    "does not contain (not implemented or not promoted to production)")
            results.append(out)
            continue
        if not req["path"] or req["path"] in ("–", "-") or not req["method"]:
            out["status"] = "NOT_MACHINE_MATCHABLE"
            results.append(out)
            continue
        wanted = normalize_template(req["path"])
        exact = None
        # Canonical routes first; /api/v1 holds deprecated aliases only.
        for prefix in ("/api", "/api/owner", "/api/v1"):
            key = normalize_template(prefix + wanted)
            if key in index:
                exact = index[key]
                break
        if exact and req["method"] in exact:
            path, op, item = exact[req["method"]]
            replacement = (op.get("x-canonical-replacement") or [None])[0]
            if replacement:
                r_method, _, r_path = replacement.partition(" ")
                canonical = index.get(normalize_template(r_path), {}).get(r_method)
                if canonical:
                    out["notes"].append(f"suggested path exists only as deprecated alias {path}; "
                                        "use the canonical route")
                    path, op, item = canonical
            out["operation"] = f"{req['method']} {path} [{op.get('operationId')}]"
            named = field_names(req["params"])
            missing = named - contract_fields(document, req["method"], op, item)
            no_params = req["params"].strip() in ("", "–", "-")
            unsent = contract_required(document, op, item) - named if (named or no_params) else set()
            if missing or unsent:
                out["status"] = "PARAMS_DIFFER"
                if missing:
                    out["notes"].append("not in contract: " + ", ".join(sorted(missing)))
                if unsent:
                    out["notes"].append("contract requires, requirement omits: "
                                        + ", ".join(sorted(unsent)))
            elif named or no_params:
                out["status"] = "PATH_AND_PARAMS_MATCH"
            else:
                out["status"] = "PATH_MATCH_FIELDS_UNVERIFIED"
                out["notes"].append(f"fields not machine-readable ({req['params'][:60]}) — review")
            if op.get("deprecated"):
                out["notes"].append("contract marks this route deprecated")
            out["notes"].append("response shape not compared automatically — review")
        elif exact:
            out["status"] = "METHOD_DIFFERS"
            out["notes"].append("contract methods: " + ", ".join(sorted(exact)))
        else:
            tail = [s for s in wanted.strip("/").split("/") if s]
            candidates = []
            for key, methods in index.items():
                segments = key.strip("/").split("/")
                if req["method"] in methods and segments[-len(tail):] == tail \
                        and not methods[req["method"]][1].get("deprecated"):
                    path, op, _ = methods[req["method"]]
                    candidates.append(f"{req['method']} {path} [{op.get('operationId')}]")
            other_methods = sorted({f"{m} {methods[m][0]}" for key, methods in index.items()
                                    if key.strip("/").split("/")[-len(tail):] == tail
                                    for m in methods if m != req["method"]
                                    and not methods[m][1].get("deprecated")})
            if candidates:
                out["status"] = "CANDIDATE_NEEDS_REVIEW"
                out["notes"].append("same method and path suffix (NOT proof of equivalence): "
                                    + "; ".join(sorted(candidates)[:3]))
            elif other_methods:
                out["status"] = "CANDIDATE_NEEDS_REVIEW"
                out["notes"].append(f"no {req['method']} at a similar path; other methods exist "
                                    "(NOT proof of equivalence): " + "; ".join(other_methods[:4]))
            else:
                out["status"] = "MISSING"
        results.append(out)
    return results


def render_gap(results: list[dict], lock: dict, requirements_name: str) -> str:
    counts: dict[str, int] = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    lines = [
        "# Requirements-to-contract gap report", "",
        f"- Requirements: `{requirements_name}` ({len(results)} endpoints)",
        f"- Contract: `{lock['version']}` (sha256 `{lock['sha256'][:16]}…`, "
        f"source `{lock['source_repository']}@{(lock['source_commit'] or '')[:12]}`)",
        f"- Generated by capitalix-contract {TOOL_VERSION}", "",
        "Statuses: `MAPPED_VERIFIED_LIVE` exercised against a running backend · "
        "`MAPPED_REVIEWED` a person confirmed the operation · `MAPPED_BY_BACKEND_BINDING` the backend "
        "conformance suite binds it · `BOUND_BUT_NOT_IN_CONTRACT` bound route absent from this contract · "
        "`NOT_BOUND_BY_BACKEND` the backend suite records no route · "
        "`PATH_AND_PARAMS_MATCH` method+path exist and every named param/field exists "
        "(response shape still needs review) · `PATH_MATCH_FIELDS_UNVERIFIED` method+path exist, "
        "fields could not be read · `PARAMS_DIFFER` · `METHOD_DIFFERS` · "
        "`CANDIDATE_NEEDS_REVIEW` similar path only, not proof · `MISSING` no candidate · "
        "`NOT_MACHINE_MATCHABLE`.", "",
        "| Status | Count |", "|---|---|",
        *[f"| {k} | {v} |" for k, v in sorted(counts.items())], "",
    ]
    section = None
    for r in results:
        if r["section"] != section:
            section = r["section"]
            lines += ["", f"## {section}", "", "| Requirement | Status | Contract operation | Notes |",
                      "|---|---|---|---|"]
        notes = "<br>".join(n.replace("|", "\\|") for n in r["notes"])
        lines.append(f"| `{r['name']}` {r['method']} `{r['path']}` (L{r['line']}) | {r['status']} | "
                     f"{('`' + r['operation'] + '`') if r['operation'] else '–'} | {notes} |")
    return "\n".join(lines) + "\n"


def cmd_gap(args) -> int:
    directory = pin_dir(args)
    lock = verify_local(directory)
    document = load_contract(directory)
    requirements = parse_requirements(Path(args.requirements).read_text(encoding="utf-8"))
    if not requirements:
        print("no requirement tables (Name | Method | path columns) found", file=sys.stderr)
        return 3
    mapping = json.loads(Path(args.map).read_text(encoding="utf-8")).get("requirements", {}) \
        if args.map else {}
    bindings = None
    if args.bindings:
        raw = json.loads(Path(args.bindings).read_text(encoding="utf-8"))
        bindings = raw.get("bindings", raw)
    results = build_gap(document, requirements, mapping, bindings)
    if args.json:
        output = json.dumps({"contract": lock, "results": results}, indent=1, ensure_ascii=False) + "\n"
    else:
        output = render_gap(results, lock, Path(args.requirements).name)
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        sys.stdout.write(output)
    return 0


# --------------------------------------------------------------------------- CLI

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="capitalix_contract.py",
                                     description=__doc__.split("\n\n")[0])
    parser.add_argument("--tool-version", action="version", version=TOOL_VERSION)
    parser.add_argument("--dir", default=DEFAULT_DIR, help="pin directory (default .capitalix-contract)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="pin an approved contract version")
    p.add_argument("--source", default=DEFAULT_SOURCE)
    p.add_argument("--version", dest="version", default="current")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("status", help="pinned version, integrity, and newer versions")
    p.add_argument("--fail-if-outdated", action="store_true")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("verify", help="verify the pinned files against contract.lock")
    p.add_argument("--remote", action="store_true", help="also check the published manifest")
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("verify-remote", help="verify a published version (used by the publisher)")
    p.add_argument("--source", default=DEFAULT_SOURCE)
    p.add_argument("--version", dest="version", default="current")
    p.add_argument("--expect-sha256")
    p.set_defaults(func=cmd_verify_remote)

    p = sub.add_parser("update", help="move the pin to another approved version")
    p.add_argument("--version", dest="version", default="current")
    p.set_defaults(func=cmd_update)

    p = sub.add_parser("list", help="compact index of operations")
    p.add_argument("filter", nargs="*")
    p.add_argument("--include-deprecated", action="store_true")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("inspect", help="operations + resolved schemas matching all query terms")
    p.add_argument("query", nargs="+")
    p.add_argument("--method")
    p.add_argument("--depth", type=int, default=4, help="$ref inlining depth (default 4)")
    p.add_argument("--limit", type=int, default=12)
    p.add_argument("--include-deprecated", action="store_true")
    p.set_defaults(func=cmd_inspect)

    p = sub.add_parser("check", help="API path literals in source exist in the pinned contract")
    p.add_argument("paths", nargs="+")
    p.add_argument("--prefix", default="",
                   help="also check relative literals (no api/ prefix) under this base, e.g. /api/owner")
    p.add_argument("--ext", default=".dart,.ts,.tsx,.js,.jsx,.php,.kt,.swift")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("sync", help="restore pinned files listed in contract.lock (fresh clones)")
    p.set_defaults(func=cmd_sync)

    p = sub.add_parser("validate", help="validate recorded request/response traffic against the contract")
    p.add_argument("traffic", help='JSON list of {"method","path","query","body","status","response"}')
    p.add_argument("--max-errors", type=int, default=8)
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("sample", help="example response body synthesized from the contract schema")
    p.add_argument("operation_id")
    p.add_argument("--status", default="200")
    p.set_defaults(func=cmd_sample)

    p = sub.add_parser("gap", help="requirements-to-contract gap report")
    p.add_argument("requirements")
    p.add_argument("--map", help="reviewed mappings JSON (highest precedence)")
    p.add_argument("--bindings", help="backend conformance bindings JSON (name -> route)")
    p.add_argument("--out")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_gap)

    # Allow query terms after options (e.g. `inspect customers --method POST owner`).
    args, extra = parser.parse_known_args(argv)
    if extra:
        field = {"inspect": "query", "list": "filter", "check": "paths"}.get(args.command)
        if field is None or any(token.startswith("-") for token in extra):
            parser.error(f"unrecognized arguments: {' '.join(extra)}")
        getattr(args, field).extend(extra)
    try:
        return args.func(args)
    except CheckFailed as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 1
    except SourceError as exc:
        print(f"SOURCE UNREACHABLE: {exc}", file=sys.stderr)
        return 2
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
