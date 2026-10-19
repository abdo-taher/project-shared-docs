"""capitalix_gap.py: request creation, submission honesty, status and confirmation (no network)."""

import contextlib
import hashlib
import io
import json
import os
import re
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest import mock

TOOLS = Path(__file__).resolve().parents[1]
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))

import capitalix_contract as cc  # noqa: E402
import capitalix_gap as gap  # noqa: E402
import capitalix_gap_core as core  # noqa: E402

CONTRACT = {"openapi": "3.1.0", "info": {"version": "1"}, "paths": {
    "/api/owner/sales/customers": {"post": {"operationId": "owner.sales.customers.store", "responses": {}}},
    "/api/owner/sales/customers/{id}": {"get": {"operationId": "owner.sales.customers.show", "responses": {}}},
}}


def pin(directory: Path, version: str) -> dict:
    data = json.dumps(CONTRACT).encode()
    manifest = {"version": version, "sha256": hashlib.sha256(data).hexdigest(),
                "source": {"repository": "alalmiyalhura/capitalix", "commit": "a" * 40}}
    return cc.write_pin(directory, "github:o/r", manifest, json.dumps(manifest).encode(), data)


class FakeGitHub(ThreadingHTTPServer):
    def __init__(self):
        super().__init__(("127.0.0.1", 0), Handler)
        self.issues: list = []
        self.comments: dict = {}
        self.index: list = []
        self.posts: list = []
        self.fail_post: int | None = None
        self.auth_seen: list = []


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send(self, status, body):
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        s = self.server
        s.auth_seen.append(self.headers.get("Authorization"))
        path = self.path.split("?")[0]
        if path == "/repos/o/r/issues":
            return self.send(200, s.issues)
        match = re.fullmatch(r"/repos/o/r/issues/(\d+)(/comments)?", path)
        if match:
            number = int(match.group(1))
            if match.group(2):
                return self.send(200, s.comments.get(number, []))
            issue = next((i for i in s.issues if i["number"] == number), None)
            return self.send(200 if issue else 404, issue or {})
        if path.endswith("/api/implemented/index.json"):
            return self.send(200, {"versions": s.index})
        self.send(404, {})

    def do_POST(self):
        s = self.server
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        s.posts.append((self.path, body, self.headers.get("Authorization")))
        if s.fail_post:
            return self.send(s.fail_post, {"message": "nope"})
        if self.path == "/repos/o/r/issues":
            number = 40 + len(s.posts)
            s.issues.append({"number": number, "state": "open", "html_url": f"https://github.com/o/r/issues/{number}",
                             "title": body["title"], "body": body["body"], "created_at": "2026-10-19T10:00:00Z",
                             "labels": [{"name": n} for n in body.get("labels", [])]})
            return self.send(201, s.issues[-1])
        return self.send(201, {"id": 77})


class GapCliTests(unittest.TestCase):

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)
        self.pin = self.dir / ".capitalix-contract"
        self.lock = pin(self.pin, "2026.10.18-aaaaaaaaaaaa")
        self.server = FakeGitHub()
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.shutdown)
        base = f"http://127.0.0.1:{self.server.server_address[1]}"
        for patch in (mock.patch.object(cc, "API_BASE", base), mock.patch.object(cc, "RAW_BASE", base),
                      mock.patch.object(cc, "HTTP_TIMEOUT", 2), mock.patch.object(cc, "MAX_RETRY_WAIT", 0),
                      mock.patch.dict(os.environ, {"PATH": str(self.dir / "nobin")}, clear=True)):
            patch.start()
            self.addCleanup(patch.stop)
        self.server.index = [{"version": self.lock["version"], "sha256": self.lock["sha256"]}]

    def cli(self, *args) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = gap.main(["--dir", str(self.pin), "--repo", "o/r", *args])
        return code, out.getvalue(), err.getvalue()

    def new(self, *extra, out="gap.json", project="owner-app") -> tuple[int, str, str]:
        return self.cli("new", "--type", "MISSING_OPERATION", "--actor", "owner", "--capability", "CAP-OWN-180",
                        "--location", "customers.list", "--feature", "Customers list", "--project", project,
                        "--platform", "flutter", "--expected", "A paginated customers list.",
                        "--actual", "No list operation.", "--criterion", "returns items",
                        "--out", str(self.dir / out), *extra)

    def lock_digest(self) -> str:
        return hashlib.sha256((self.pin / "contract.lock").read_bytes()).hexdigest()

    # ----------------------------------------------------------------- new / validate

    def test_new_fills_the_pinned_contract(self):
        code, out, _ = self.new()
        self.assertEqual(code, 0, out)
        request = json.loads((self.dir / "gap.json").read_text())
        self.assertEqual(request["contract"], {"version": self.lock["version"], "sha256": self.lock["sha256"]})
        self.assertEqual(core.validate(request), [])
        self.assertEqual(self.cli("validate", str(self.dir / "gap.json"))[0], 0)

    def test_new_canonicalizes_existing_operations(self):
        code, _, err = self.cli("new", "--type", "RESPONSE_MISMATCH", "--actor", "owner", "--method", "get",
                                "--path", "/api/owner/sales/customers/{customer}", "--location", "data.phone",
                                "--feature", "Customer details", "--project", "web", "--platform", "react",
                                "--expected", "phone is documented", "--actual", "missing",
                                "--criterion", "c", "--out", str(self.dir / "m.json"))
        self.assertEqual(code, 0, err)
        operation = json.loads((self.dir / "m.json").read_text())["operation"]
        self.assertEqual(operation["operation_id"], "owner.sales.customers.show")

    def test_new_refuses_unknown_operation_and_existing_missing_operation(self):
        code, _, err = self.cli("new", "--type", "RESPONSE_MISMATCH", "--actor", "owner", "--operation", "owner.nope",
                                "--location", "x", "--feature", "Feature x", "--project", "p", "--platform", "web",
                                "--expected", "expected text", "--actual", "actual", "--criterion", "c")
        self.assertEqual(code, 1)
        code, _, err = self.new("--method", "POST", "--path", "/api/owner/sales/customers")
        self.assertEqual(code, 1)
        self.assertIn("exists in your pinned contract", err)

    def test_new_rejects_secrets_without_echoing_them(self):
        evidence = self.dir / "e.txt"
        evidence.write_text('{"password": "Sup3rSecret!"}')
        code, out, err = self.new("--evidence", str(evidence))
        self.assertEqual(code, 1)
        self.assertIn("sensitive", err)
        self.assertNotIn("Sup3rSecret", out + err)
        self.assertFalse((self.dir / "gap.json").exists())

    def test_tampered_pin_is_refused(self):
        (self.pin / "openapi.json").write_text("{}")
        self.assertEqual(self.new()[0], 1)

    # ----------------------------------------------------------------- submit

    def test_submit_without_credentials_never_claims_success(self):
        self.new()
        code, out, _ = self.cli("submit", str(self.dir / "gap.json"))
        self.assertEqual(code, gap.NOT_SUBMITTED)
        self.assertIn("NOT_SUBMITTED", out)
        self.assertNotIn("SUBMITTED #", out)
        self.assertTrue((self.dir / "gap.issue.md").exists())
        self.assertFalse((self.dir / "gap.submission.json").exists())
        self.assertTrue((self.dir / "gap.json").exists())
        self.assertEqual(self.server.posts, [])
        self.assertEqual(set(self.server.auth_seen), {None}, "reads stay anonymous")

    def test_submit_with_token(self):
        self.new()
        with mock.patch.dict(os.environ, {"GITHUB_TOKEN": "tkn"}):
            code, out, _ = self.cli("submit", str(self.dir / "gap.json"))
        self.assertEqual(code, 0)
        self.assertIn("SUBMITTED #41", out)
        record = json.loads((self.dir / "gap.submission.json").read_text())
        self.assertEqual(record["issue"], 41)
        path, body, auth = self.server.posts[0]
        self.assertEqual(auth, "Bearer tkn")
        self.assertIn(core.BODY_MARKER, body["body"])
        self.assertEqual(body["labels"], ["api-gap", "gap:submitted"])

    def test_failed_post_is_not_retried_or_recorded(self):
        self.new()
        self.server.fail_post = 502
        with mock.patch.dict(os.environ, {"GITHUB_TOKEN": "tkn"}):
            code, _, err = self.cli("submit", str(self.dir / "gap.json"))
        self.assertEqual(code, 2)
        self.assertEqual(len(self.server.posts), 1, "a POST is never retried automatically")
        self.assertNotIn("tkn", err)
        self.assertFalse((self.dir / "gap.submission.json").exists())

    def test_same_project_duplicate_is_refused_other_consumers_are_linked(self):
        self.new()
        with mock.patch.dict(os.environ, {"GITHUB_TOKEN": "tkn"}):
            self.assertEqual(self.cli("submit", str(self.dir / "gap.json"))[0], 0)
            self.new(out="again.json")
            code, _, err = self.cli("submit", str(self.dir / "again.json"))
            self.assertEqual(code, 1)
            self.assertIn("already reported", err)
            self.new(out="web.json", project="capitalix-web")
            code, out, _ = self.cli("submit", str(self.dir / "web.json"))
            self.assertEqual(code, 0)
            self.assertIn("same backend work", out)

    def test_search_is_anonymous(self):
        self.new()
        code, out, _ = self.cli("search", str(self.dir / "gap.json"))
        self.assertEqual(code, 0)
        self.assertIn("no reported gap", out)
        self.assertEqual(set(self.server.auth_seen), {None})

    # ----------------------------------------------------------------- status / confirm

    def published_issue(self, version: str, digest: str, association: str = "OWNER") -> None:
        request = json.loads((self.dir / "gap.json").read_text())
        _, body = core.render_issue(request)
        self.server.issues.append({"number": 9, "state": "open", "title": "t", "body": body,
                                   "html_url": "https://github.com/o/r/issues/9", "created_at": "2026-10-19T10:00:00Z",
                                   "labels": [{"name": "api-gap"}, {"name": "gap:contract-published"}]})
        state = {"fingerprint": core.fingerprint(request), "state": "CONTRACT_PUBLISHED", "reason": "x",
                 "backend": 3, "resolution": {"version": version, "sha256": digest}}
        self.server.comments[9] = [{"author_association": association,
                                    "body": f"<!-- capitalix-gap-coordinator:v1 {json.dumps(state)} -->\nstate"}]

    def test_status_reports_an_older_pin_and_never_upgrades(self):
        self.new()
        newer = {"version": "2026.10.20-bbbbbbbbbbbb", "sha256": "b" * 64}
        self.server.index.append(newer)
        self.published_issue(newer["version"], newer["sha256"])
        before = self.lock_digest()
        code, out, _ = self.cli("status", "9")
        self.assertEqual(code, 0)
        self.assertIn("is older than the resolution", out)
        self.assertIn(f"update --version {newer['version']}", out)
        self.assertEqual(self.lock_digest(), before, "status never changes the pin")
        code, _, err = self.cli("confirm", "9", "--tests-passed")
        self.assertEqual(code, 1)
        self.assertIn("does not include", err)
        self.assertEqual(self.lock_digest(), before)

    def test_status_ignores_state_comments_from_non_members(self):
        self.new()
        self.published_issue(self.lock["version"], self.lock["sha256"], association="NONE")
        code, out, _ = self.cli("status", "9")
        self.assertIn("not processed yet", out)

    def test_confirm_after_upgrade(self):
        self.new()
        self.published_issue(self.lock["version"], self.lock["sha256"])
        self.assertEqual(self.cli("confirm", "9")[0], 1, "--tests-passed is required")
        code, out, _ = self.cli("confirm", "9", "--tests-passed")
        self.assertEqual(code, gap.NOT_SUBMITTED)
        self.assertIn("capitalix-gap-verification:v1", out)
        with mock.patch.dict(os.environ, {"GITHUB_TOKEN": "tkn"}):
            code, out, _ = self.cli("confirm", "9", "--tests-passed")
        self.assertEqual(code, 0)
        path, body, _ = self.server.posts[-1]
        self.assertEqual(path, "/repos/o/r/issues/9/comments")
        payload = json.loads(re.search(r"verification:v1 (\{.*\}) -->", body["body"]).group(1))
        self.assertEqual(payload["version"], self.lock["version"])
        self.assertTrue(payload["tests_passed"])


class SharedContractTests(unittest.TestCase):

    def test_core_matches_the_shared_corpus(self):
        corpus = json.loads((TOOLS / "tests/gap-conformance.json").read_text())
        source = (TOOLS / "capitalix_gap_core.py").read_bytes()
        self.assertEqual(hashlib.sha256(source).hexdigest(), corpus["core_sha256"],
                         "after editing the core, update core_sha256 in tools/tests/gap-conformance.json")
        for case in corpus["cases"]:
            with self.subTest(case["name"]):
                errors = core.validate(case["request"])
                self.assertEqual(not errors, case["valid"])
                if case["valid"]:
                    self.assertEqual(core.fingerprint(case["request"]), case["fingerprint"])

    def test_issue_form_labels_match_the_parser(self):
        form = (ROOT / ".github/ISSUE_TEMPLATE/api-gap.yml").read_text()
        labels = re.findall(r"^\s+label: (.+)$", form, re.M)
        self.assertEqual(sorted(labels), sorted(core.ISSUE_FORM_FIELDS))
        options = dict(re.findall(r"label: (Gap type|Actor)\n\s+options: \[([^\]]+)\]", form.replace("\n                ", " ")))
        self.assertEqual([o.strip() for o in options["Gap type"].split(",")], list(core.GAP_TYPES))
        self.assertEqual([o.strip() for o in options["Actor"].split(",")], list(core.ACTORS))

    def test_json_schema_matches_the_core(self):
        schema = json.loads((ROOT / "api/gaps/capitalix.api-gap.v1.schema.json").read_text())
        self.assertEqual(set(schema["properties"]), core.TOP_LEVEL)
        self.assertEqual(schema["required"], list(core.REQUIRED))
        self.assertEqual(schema["properties"]["gap_type"]["enum"], list(core.GAP_TYPES))
        self.assertEqual(schema["properties"]["schema_version"]["const"], core.SCHEMA_VERSION)


if __name__ == "__main__":
    unittest.main()
