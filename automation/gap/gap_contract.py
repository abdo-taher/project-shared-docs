"""Read and verify the published contract; evaluate resolution checks against it.

The coordinator never runs code downloaded from shared-docs: it implements the
same integrity rules as the consumer tool (tools/capitalix_contract.py) here.

  current.json / index.json  ->  versions/<v>/manifest.json  ->  openapi.json
  digest == pointer/index == manifest; approval.json digest == manifest record,
  and approval.json approves exactly these bytes.

Resolution checks are a closed, declarative vocabulary (no expressions):

  {"check": "operation_exists",   "operation_id": "..."}  | {"method": "GET", "path": "/api/..."}
  {"check": "field_present",      "operation_id": "...", "in": "request"|"response", "field": "data.items[].name", "status": "200"}
  {"check": "field_required",     ... same ...}
  {"check": "field_type",         ... same ..., "type": "string"}
  {"check": "parameter_present",  "operation_id": "...", "name": "page", "in": "query"}
  {"check": "parameter_required", ... same ...}
  {"check": "operation_has_summary", "operation_id": "..."}
  {"check": "operation_description_contains", "operation_id": "...", "text": "Accept-Language"}  (literal, <= 120 chars)
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from gap_core import normalize_path
from gap_http import ApiError, Http

PUBLISHED_ROOT = "api/implemented"
METHODS = ("get", "post", "put", "patch", "delete")
CHECKS = {"operation_exists", "field_present", "field_required", "field_type",
          "parameter_present", "parameter_required", "operation_has_summary", "operation_description_contains"}


class IntegrityError(Exception):
    """Published files are inconsistent: never treat them as evidence."""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class PublishedContracts:
    """Published state of shared-docs: `github:OWNER/REPO` (anonymous HTTPS) or `file:PATH`."""

    def __init__(self, source: str, http: Http | None = None):
        self.source = source
        self.http = http
        self._documents: dict[str, dict] = {}
        self._index = None
        self._current = None

    def fetch(self, path: str) -> bytes:
        if self.source.startswith("file:"):
            try:
                return (Path(self.source[5:]) / path).read_bytes()
            except OSError as exc:
                raise ApiError(f"cannot read published file {path}: {exc.strerror}") from None
        if not self.source.startswith("github:"):
            raise ApiError(f"unsupported contract source [{self.source}]")
        repo, _, ref = self.source[7:].partition("@")
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
            raise ApiError("invalid contract source repository")
        http = self.http or Http("https://raw.githubusercontent.com", {})
        return http.request("GET", f"{repo}/{ref or 'HEAD'}/{path}", raw=True)[0]

    def _json(self, path: str) -> dict:
        try:
            value = json.loads(self.fetch(path))
        except json.JSONDecodeError:
            raise IntegrityError(f"{path} is not valid JSON") from None
        if not isinstance(value, dict):
            raise IntegrityError(f"{path} is not a JSON object")
        return value

    def index(self) -> list[dict]:
        if self._index is None:
            versions = self._json(f"{PUBLISHED_ROOT}/index.json").get("versions")
            if not isinstance(versions, list):
                raise IntegrityError("index.json has no versions list")
            self._index = versions
        return self._index

    def entry(self, version: str) -> dict | None:
        return next((v for v in self.index() if v.get("version") == version), None)

    def position(self, version: str) -> int:
        """Index position (oldest first); -1 when the version is not published."""
        return next((i for i, v in enumerate(self.index()) if v.get("version") == version), -1)

    def current(self) -> dict:
        if self._current is not None:
            return self._current
        pointer = self._json(f"{PUBLISHED_ROOT}/current.json")
        entry = self.entry(pointer.get("version", ""))
        if entry is None or entry.get("sha256") != pointer.get("sha256"):
            raise IntegrityError("current.json does not match index.json")
        self._current = pointer
        return pointer

    def manifest(self, version: str) -> dict:
        entry = self.entry(version)
        if entry is None:
            raise IntegrityError(f"version {version} is not published")
        manifest = self._json(f"{PUBLISHED_ROOT}/versions/{version}/manifest.json")
        if manifest.get("version") != version or manifest.get("sha256") != entry.get("sha256"):
            raise IntegrityError(f"manifest for {version} does not match the index")
        source = manifest.get("source") or {}
        if not source.get("repository") or not source.get("commit"):
            raise IntegrityError(f"manifest for {version} does not name its source")
        return manifest

    def document(self, version: str) -> dict:
        """The verified contract document of a published version."""
        if version in self._documents:
            return self._documents[version]
        manifest = self.manifest(version)
        base = f"{PUBLISHED_ROOT}/versions/{version}"
        contract = self.fetch(f"{base}/openapi.json")
        digest = sha256(contract)
        if digest != manifest["sha256"]:
            raise IntegrityError(f"contract digest for {version} does not match its manifest")
        approval_bytes = self.fetch(f"{base}/approval.json")
        recorded = (manifest.get("approval") or {}).get("approval_manifest_sha256")
        if not recorded or sha256(approval_bytes) != recorded \
                or (manifest.get("files") or {}).get("approval.json") != recorded:
            raise IntegrityError(f"approval evidence for {version} does not match its manifest")
        try:
            approval = json.loads(approval_bytes)
        except json.JSONDecodeError:
            raise IntegrityError(f"approval evidence for {version} is not JSON") from None
        if approval.get("decision") != "APPROVED" or approval.get("approved_artifact_sha256") != digest \
                or not approval.get("trusted_approval_signature"):
            raise IntegrityError(f"approval evidence for {version} does not approve these bytes")
        try:
            document = json.loads(contract)
        except json.JSONDecodeError:
            raise IntegrityError(f"contract {version} is not valid JSON") from None
        self._documents[version] = document
        return document


# --------------------------------------------------------------------------- contract queries

def operations(document: dict):
    for path, item in (document.get("paths") or {}).items():
        for method in METHODS:
            if isinstance(item, dict) and method in item:
                yield method.upper(), path, item[method], item


def find_operation(document: dict, operation: dict):
    """(method, path, op, item) for {operation_id} or {method, path}; None when absent."""
    wanted_id = operation.get("operation_id")
    wanted = (operation.get("method", "").upper(), normalize_path(operation.get("path", "")))
    for method, path, op, item in operations(document):
        if wanted_id and op.get("operationId") == wanted_id:
            return method, path, op, item
        if not wanted_id and (method, normalize_path(path)) == wanted:
            return method, path, op, item
    return None


def actor_of(path: str, op: dict) -> str | None:
    """Actor namespace of a canonical operation; None for deprecated /api/v1 aliases."""
    match = re.match(r"^/api/([a-z]+)/", path + "/")
    actor = match.group(1) if match else None
    return None if actor == "v1" else actor


def _deref(document: dict, node, depth: int = 0):
    while isinstance(node, dict) and "$ref" in node and depth < 32:
        ref = str(node["$ref"])
        if not ref.startswith("#/"):
            return {}
        target = document
        for part in ref[2:].split("/"):
            part = part.replace("~1", "/").replace("~0", "~")
            if not isinstance(target, dict) or part not in target:
                return {}
            target = target[part]
        node, depth = target, depth + 1
    return node if isinstance(node, dict) else {}


def _branches(document: dict, schema: dict) -> list[dict]:
    """A schema and its allOf/oneOf/anyOf members (dereferenced, flattened)."""
    out, queue, seen = [], [schema], 0
    while queue and seen < 64:
        node = _deref(document, queue.pop(0))
        seen += 1
        out.append(node)
        for key in ("allOf", "oneOf", "anyOf"):
            queue += [m for m in node.get(key, []) if isinstance(m, dict)]
    return out


def _walk(document: dict, schema: dict, field: str):
    """Follow a dotted field path ('data.items[].name'); returns (parent schemas, leaf schemas)."""
    current = [schema]
    parents: list[dict] = []
    for raw in [p for p in field.split(".") if p]:
        name, array = (raw[:-2], True) if raw.endswith("[]") else (raw, False)
        parents = [b for s in current for b in _branches(document, s)]
        current = [_deref(document, b["properties"][name]) for b in parents
                   if isinstance(b.get("properties"), dict) and name in b["properties"]]
        if not current:
            return parents, []
        if array:
            current = [_deref(document, b.get("items", {})) for s in current
                       for b in _branches(document, s) if b.get("items")]
            if not current:
                return parents, []
    return parents, current


def _target_schema(document: dict, op: dict, where: str, status: str | None) -> dict | None:
    if where == "request":
        content = _deref(document, op.get("requestBody", {})).get("content", {})
    else:
        responses = op.get("responses", {})
        code = status or next((c for c in sorted(responses) if str(c).startswith("2")), None)
        content = _deref(document, responses.get(str(code), {})).get("content", {}) if code else {}
    media = content.get("application/json") or next(iter(content.values()), None)
    return media.get("schema") if isinstance(media, dict) else None


def evaluate_check(document: dict, check: dict) -> str | None:
    """None when the check holds; otherwise a short reason."""
    if not isinstance(check, dict) or check.get("check") not in CHECKS:
        return "unsupported check"
    found = find_operation(document, check)
    label = check.get("operation_id") or f"{check.get('method')} {check.get('path')}"
    if found is None:
        return f"operation {label} is not in the contract"
    kind = check["check"]
    if kind == "operation_exists":
        return None
    _, _, op, item = found
    if kind == "operation_has_summary":
        return None if str(op.get("summary") or "").strip() else f"{label}: has no summary"
    if kind == "operation_description_contains":
        text = check.get("text")
        if not isinstance(text, str) or not 1 <= len(text) <= 120:
            return "unsupported check"
        return None if text in str(op.get("description") or "") else f"{label}: the description does not mention {text!r}"
    if kind.startswith("parameter_"):
        params = [_deref(document, p) for p in item.get("parameters", []) + op.get("parameters", [])]
        match = [p for p in params if p.get("name") == check.get("name")
                 and (not check.get("in") or p.get("in") == check.get("in"))]
        if not match:
            return f"{label}: parameter {check.get('name')} is not documented"
        if kind == "parameter_required" and not any(p.get("required") for p in match):
            return f"{label}: parameter {check.get('name')} is not required"
        return None
    schema = _target_schema(document, op, check.get("in", "response"), check.get("status"))
    if schema is None:
        return f"{label}: no {check.get('in', 'response')} schema"
    field = str(check.get("field", ""))
    parents, leaves = _walk(document, schema, field)
    if not leaves:
        return f"{label}: {check.get('in', 'response')} field {field} is not documented"
    if kind == "field_required":
        name = field.split(".")[-1].removesuffix("[]")
        if not any(name in (p.get("required") or []) for p in parents):
            return f"{label}: field {field} is not required"
    if kind == "field_type":
        types = set()
        for leaf in leaves:
            for b in _branches(document, leaf):
                value = b.get("type")
                types |= set(value) if isinstance(value, list) else {value} if value else set()
        if check.get("type") not in types:
            return f"{label}: field {field} is not of type {check.get('type')}"
    return None
