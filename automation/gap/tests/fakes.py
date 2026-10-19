"""Isolated fixtures: in-memory GitHub intake/backend and a published shared-docs layout on disk."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gap_http import ApiError  # noqa: E402

COORDINATOR = "capitalix-bot"
SHA_A = "a" * 40


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def contract(extra_paths: dict | None = None) -> dict:
    paths = {
        "/api/owner/sales/customers": {
            "post": {"operationId": "owner.sales.customers.store",
                     "requestBody": {"content": {"application/json": {"schema": {
                         "type": "object", "required": ["name"],
                         "properties": {"name": {"type": "string"}, "phone": {"type": "string"}}}}}},
                     "responses": {"201": {"content": {"application/json": {"schema": {
                         "$ref": "#/components/schemas/CustomerEnvelope"}}}}}}},
        "/api/owner/sales/customers/{id}": {
            "get": {"operationId": "owner.sales.customers.show",
                    "responses": {"200": {"content": {"application/json": {"schema": {
                        "$ref": "#/components/schemas/CustomerEnvelope"}}}}}}},
        "/api/accountant/ledger": {"get": {"operationId": "accountant.ledger.index", "responses": {}}},
        "/api/v1/customers": {"get": {"operationId": "alias.customers.index", "deprecated": True, "responses": {}}},
    }
    paths.update(extra_paths or {})
    return {"openapi": "3.1.0", "info": {"version": "1.0.0"}, "paths": paths,
            "components": {"schemas": {
                "Customer": {"type": "object", "properties": {"id": {"type": "integer"},
                                                              "name": {"type": "string"}}},
                "CustomerEnvelope": {"type": "object", "properties": {
                    "data": {"$ref": "#/components/schemas/Customer"}}}}}}


_LIST_SCHEMA = {"type": "object", "properties": {"data": {"type": "object", "properties": {
    "items": {"type": "array", "items": {"$ref": "#/components/schemas/Customer"}},
    "meta": {"type": "object", "properties": {"total": {"type": "integer"}}}}}}}
LIST_OPERATION = {"/api/owner/sales/customers": {"get": {
    "operationId": "owner.sales.customers.index",
    "parameters": [{"name": "page", "in": "query", "schema": {"type": "integer"}}],
    "responses": {"200": {"content": {"application/json": {"schema": _LIST_SCHEMA}}}}}}}


def merge_paths(base: dict, extra: dict) -> dict:
    out = copy.deepcopy(base)
    for path, item in extra.items():
        out["paths"].setdefault(path, {}).update(item)
    return out


def publish(root: Path, version_date: str, document: dict, commit: str = SHA_A,
            repository: str = "example/published-contract-source") -> tuple[str, str]:
    """Write one published version exactly like openapi_publish.py lays it out."""
    data = (json.dumps(document, indent=2) + "\n").encode()
    digest = sha(data)
    version = f"{version_date}-{digest[:12]}"
    base = root / "api/implemented"
    vdir = base / "versions" / version
    vdir.mkdir(parents=True, exist_ok=True)
    (vdir / "openapi.json").write_bytes(data)
    approval = json.dumps({"decision": "APPROVED", "approved_artifact_sha256": digest,
                           "trusted_approval_signature": "f" * 64}).encode()
    (vdir / "approval.json").write_bytes(approval)
    manifest = {"schema": "capitalix-contract-manifest/1", "version": version, "sha256": digest,
                "source": {"repository": repository, "commit": commit, "ref": "main"},
                "approval": {"approval_manifest_sha256": sha(approval)},
                "files": {"openapi.json": digest, "approval.json": sha(approval)}}
    (vdir / "manifest.json").write_text(json.dumps(manifest))
    index_path = base / "index.json"
    index = json.loads(index_path.read_text()) if index_path.exists() else {"versions": []}
    index["versions"].append({"version": version, "sha256": digest, "source_commit": commit})
    index_path.write_text(json.dumps(index))
    (base / "current.json").write_text(json.dumps({"version": version, "sha256": digest, "source_commit": commit}))
    return version, digest


def gap_request(version: str, digest: str, **overrides) -> dict:
    request = {
        "schema_version": "capitalix.api-gap.v1",
        "request_id": "gap-0000000000000001",
        "consumer": {"project": "capitalix-owner-app", "platform": "flutter"},
        "feature": "Customers list screen",
        "actor": "owner",
        "capability_id": "CAP-OWN-180",
        "gap_type": "MISSING_OPERATION",
        "location": "customers.list",
        "contract": {"version": version, "sha256": digest},
        "expected": "A paginated list of the owner's customers with name and id.",
        "actual": "The contract has no list operation for owner customers.",
        "evidence": [{"kind": "note", "content": "inspect customers --method GET owner returns nothing"}],
        "requirements": ["BACKEND_API.md#7 Customers"],
        "acceptance_criteria": ["GET list returns data.items[] with id and name", "data.meta.total present"],
        "severity": "high",
        "submitted_at": "2026-10-19T10:00:00Z",
    }
    for key, value in overrides.items():
        if value is None:
            request.pop(key, None)
        else:
            request[key] = value
    return request


class Failing:
    """Inject failures: fail[method] = [exc, exc, ...] raised on successive calls."""

    def _maybe_fail(self, method: str) -> None:
        queue = self.fail.get(method)
        if queue:
            raise queue.pop(0)


class FakeGitHub(Failing):
    def __init__(self):
        self.can_write = True
        self.issues: dict[int, dict] = {}
        self._comments: dict[int, list] = {}
        self.events: dict[int, list] = {}
        self.permissions: dict[str, str] = {}
        self.fail: dict[str, list] = {}
        self.writes = 0
        self._next_comment = 1000

    def add_issue(self, number: int, body: str, author: str = "alice", labels=("api-gap", "gap:submitted"),
                  created_at: str = "2026-10-19T10:00:00Z") -> dict:
        issue = {"number": number, "user": {"login": author}, "body": body, "state": "open",
                 "labels": [{"name": n} for n in labels], "created_at": created_at}
        self.issues[number] = issue
        self._comments.setdefault(number, [])
        return issue

    def add_label_by(self, number: int, label: str, actor: str) -> None:
        self.issues[number]["labels"].append({"name": label})
        self.events.setdefault(number, []).append({"event": "labeled", "label": {"name": label},
                                                   "actor": {"login": actor}})

    def user_comment(self, number: int, login: str, body: str) -> None:
        self._next_comment += 1
        self._comments[number].append({"id": self._next_comment, "user": {"login": login}, "body": body})

    def labels(self, number: int) -> set[str]:
        return {l["name"] for l in self.issues[number]["labels"]}

    def state_of(self, number: int) -> dict | None:
        from gap_coordinator import STATE_MARKER, marker_json
        for c in reversed(self._comments[number]):
            if c["user"]["login"] == COORDINATOR:
                value = marker_json(c["body"], STATE_MARKER)
                if value:
                    return value
        return None

    # adapter interface
    def viewer(self):
        return COORDINATOR

    def open_issues(self):
        self._maybe_fail("open_issues")
        return [copy.deepcopy(i) for i in self.issues.values() if i["state"] == "open"]

    def issue(self, number):
        return copy.deepcopy(self.issues[number])

    def comments(self, number):
        self._maybe_fail("comments")
        return copy.deepcopy(self._comments.get(number, []))

    def label_events(self, number):
        return copy.deepcopy(self.events.get(number, []))

    def permission(self, login):
        self._maybe_fail("permission")
        return self.permissions.get(login, "none")

    def ensure_labels(self):
        pass

    def set_labels(self, number, add, remove):
        self._maybe_fail("set_labels")
        self.writes += 1
        issue = self.issues[number]
        issue["labels"] = [l for l in issue["labels"] if l["name"] not in remove] + [{"name": n} for n in add]

    def comment(self, number, body):
        self._maybe_fail("comment")
        self.writes += 1
        self.user_comment(number, COORDINATOR, body)
        return self._comments[number][-1]

    def edit_comment(self, comment_id, body):
        self.writes += 1
        for comments in self._comments.values():
            for c in comments:
                if c["id"] == comment_id:
                    c["body"] = body

    def close(self, number, reason="completed"):
        self.writes += 1
        self.issues[number]["state"] = "closed"
        self.issues[number]["state_reason"] = reason


class FakeBackend(Failing):
    def __init__(self):
        self.issues: dict[int, dict] = {}
        self._notes: dict[int, list] = {}
        self.events: dict[int, list] = {}
        self.mrs: dict[int, list] = {}
        self.pipeline_by_sha: dict[str, list] = {}
        self.jobs: dict[int, list] = {}
        self.files: dict[tuple[str, str], bytes] = {}
        self.ancestors: set[tuple[str, str]] = set()
        self.access: dict[int, int] = {}
        self.fail: dict[str, list] = {}
        self.hide_on_find = 0
        self.created_mrs: list = []
        self.writes = 0

    def add_label_by(self, iid: int, label: str, user_id: int, username: str = "maint") -> None:
        self.issues[iid]["labels"].append(label)
        self.events.setdefault(iid, []).append({"action": "add", "label": {"name": label},
                                                "user": {"id": user_id, "username": username}})

    # adapter interface
    def find_by_fingerprint(self, fingerprint):
        self._maybe_fail("find_by_fingerprint")
        if self.hide_on_find:
            self.hide_on_find -= 1
            return []
        marker = f"capitalix-gap fingerprint={fingerprint}"
        return [copy.deepcopy(i) for i in sorted(self.issues.values(), key=lambda i: i["iid"])
                if marker in i["description"]]

    def issue(self, iid):
        return copy.deepcopy(self.issues[iid])

    def gap_issues(self, state="opened"):
        return [copy.deepcopy(i) for i in self.issues.values() if "api-gap" in i["labels"] and i["state"] == state]

    def create_issue(self, title, description, labels):
        self._maybe_fail("create_issue")
        self.writes += 1
        iid = max(self.issues, default=0) + 1
        self.issues[iid] = {"iid": iid, "title": title, "description": description, "labels": list(labels),
                            "state": "opened"}
        self._notes[iid] = []
        return copy.deepcopy(self.issues[iid])

    def update_issue(self, iid, **fields):
        self._maybe_fail("update_issue")
        self.writes += 1
        issue = self.issues[iid]
        for name in filter(None, (fields.get("remove_labels") or "").split(",")):
            if name in issue["labels"]:
                issue["labels"].remove(name)
        for name in filter(None, (fields.get("add_labels") or "").split(",")):
            if name not in issue["labels"]:
                issue["labels"].append(name)
        if fields.get("state_event") == "close":
            issue["state"] = "closed"
        return copy.deepcopy(issue)

    def notes(self, iid):
        return copy.deepcopy(self._notes.get(iid, []))

    def add_note(self, iid, body):
        self.writes += 1
        self._notes.setdefault(iid, []).append({"body": body})
        return {"body": body}

    def label_events(self, iid):
        return copy.deepcopy(self.events.get(iid, []))

    def access_level(self, user_id):
        return self.access.get(user_id, 0)

    def related_merge_requests(self, iid):
        self._maybe_fail("related_merge_requests")
        return copy.deepcopy(self.mrs.get(iid, []))

    def pipelines(self, sha_):
        return copy.deepcopy(self.pipeline_by_sha.get(sha_, []))

    def pipeline_jobs(self, pipeline_id):
        return copy.deepcopy(self.jobs.get(pipeline_id, []))

    def is_ancestor(self, ancestor, descendant):
        return ancestor == descendant or (ancestor, descendant) in self.ancestors

    def file_at(self, path, ref):
        return self.files.get((path, ref))

    def ensure_labels(self):
        pass

    def create_merge_request(self, source, title, description, target="main"):
        self.writes += 1
        mr = {"iid": 100 + len(self.created_mrs), "source_branch": source, "target_branch": target, "title": title,
              "description": description, "state": "opened"}
        self.created_mrs.append(mr)
        return mr


def api_error(status: int, transient: bool = False) -> ApiError:
    return ApiError(f"GET /x: HTTP {status}", status, transient=transient)
