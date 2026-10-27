import hashlib
import io
import json
import subprocess
import sys
import tempfile
import threading
import unittest
import zipfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools"))
sys.path.insert(0, str(REPO_ROOT / "tools" / "publish"))

import capitalix_contract as client  # noqa: E402
import capitalix_publish as pub  # noqa: E402

BACKEND = "abdo-taher/capitalix"
BRANCH = "integration/E01-FOUNDATION-SAAS"
SHA = "a" * 40
SHA2 = "b" * 40


def operation(op_id, summary=None, extra=None):
    op = {"operationId": op_id, "tags": ["T"], "security": [{"sanctumBearer": []}],
          "responses": {"200": {"description": "ok"}}}
    if summary:
        op["summary"] = summary
    op.update(extra or {})
    return op


def doc(paths):
    return {"openapi": "3.1.0", "info": {"title": "t", "version": "1"},
            "paths": paths, "components": {"securitySchemes": {"sanctumBearer": {"type": "http", "scheme": "bearer"}}}}


BASE = doc({"/api/public/a": {"get": operation("public.a")}})
DOC_ONLY = doc({"/api/public/a": {"get": operation("public.a", summary="List a")}})
ADDITIVE = doc({"/api/public/a": {"get": operation("public.a")}, "/api/public/b": {"get": operation("public.b")}})
BREAKING = doc({"/api/public/b": {"get": operation("public.b")}})
TWO = doc({"/api/public/a": {"get": operation("public.a")}, "/api/public/c": {"get": operation("public.c")}})


def raw(document):
    return (json.dumps(document, indent=1) + "\n").encode()


def record_for(document, commit=SHA, run_id=7):
    data = raw(document)
    return {"schema": pub.BUILD_SCHEMA, "repository": BACKEND, "commit": commit, "run_id": run_id,
            "run_url": f"https://github.com/{BACKEND}/actions/runs/{run_id}",
            "sha256": hashlib.sha256(data).hexdigest(), "size": len(data), "branch": BRANCH}


def zip_of(document, record):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("openapi.json", raw(document))
        archive.writestr("build-record.json", json.dumps(record))
    return buffer.getvalue()


class FakeApi:
    """Answers like GitHub for one backend run; every field can be overridden per test."""

    def __init__(self, document=BASE, **over):
        self.record = over.pop("record", record_for(document))
        self.blob = over.pop("blob", zip_of(document, self.record))
        self.run = {"repository": {"full_name": BACKEND}, "path": pub.BUILD_WORKFLOW, "status": "completed",
                    "conclusion": "success", "event": "workflow_dispatch", "head_branch": BRANCH, "head_sha": SHA,
                    "html_url": self.record["run_url"], "head_repository": {"full_name": BACKEND}}
        self.run.update(over.pop("run", {}))
        self.compare = over.pop("compare", "ahead")
        self.artifacts = over.pop("artifacts", [{"id": 5, "name": pub.BUILD_ARTIFACT, "expired": False}])
        self.date = over.pop("date", "2026-10-20T10:00:00Z")

    def get(self, path):
        if "/compare/" in path:
            return {"status": self.compare}
        if path.endswith("/artifacts"):
            return {"artifacts": self.artifacts}
        if "/commits/" in path:
            return {"commit": {"committer": {"date": self.date}}}
        return self.run

    def download(self, path):
        return self.blob


class VerifyBuildTests(unittest.TestCase):

    def verify(self, **over):
        return pub.verify_build(FakeApi(**over), BACKEND, 7, BRANCH)

    def test_a_genuine_build_is_accepted(self):
        data, record, date = self.verify()
        self.assertEqual(data, raw(BASE))
        self.assertEqual((record["commit"], date), (SHA, "2026-10-20T10:00:00Z"))

    def test_every_run_property_is_checked_against_github_not_the_artifact(self):
        bad = [({"path": ".github/workflows/other.yml"}, "workflow"), ({"conclusion": "failure"}, "successfully"),
               ({"event": "push"}, "manually dispatched"), ({"head_branch": "feature/x"}, "not built from"),
               ({"head_repository": {"full_name": "evil/fork"}}, "fork"), ({"head_sha": "xyz"}, "no commit"),
               ({"repository": {"full_name": "other/repo"}}, "another repository")]
        for run, text in bad:
            with self.assertRaisesRegex(pub.Refused, text, msg=run):
                self.verify(run=run)

    def test_a_commit_that_is_not_on_the_development_branch_is_refused(self):
        with self.assertRaisesRegex(pub.Refused, "not on"):
            self.verify(compare="diverged")
        with self.assertRaisesRegex(pub.Refused, "not on"):
            self.verify(compare="behind")

    def test_a_record_that_disagrees_with_the_run_is_refused(self):
        for patch in ({"commit": SHA2}, {"run_id": 8}, {"repository": "evil/x"}):
            record = {**record_for(BASE), **patch}
            with self.assertRaisesRegex(pub.Refused, "does not match the GitHub run"):
                self.verify(record=record, blob=zip_of(BASE, record))

    def test_bytes_that_are_not_the_recorded_bytes_are_refused(self):
        record = record_for(BASE)
        with self.assertRaisesRegex(pub.Refused, "not the contract the build recorded"):
            self.verify(record=record, blob=zip_of(ADDITIVE, record))

    def test_artifact_shape_is_strict(self):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as archive:
            archive.writestr("openapi.json", raw(BASE))
            archive.writestr("../escape", "x")
        with self.assertRaisesRegex(pub.Refused, "exactly"):
            self.verify(blob=buffer.getvalue())
        with self.assertRaisesRegex(pub.Refused, "not a zip"):
            self.verify(blob=b"nope")
        for artifacts in ([], [{"id": 1, "name": pub.BUILD_ARTIFACT, "expired": True}],
                          [{"id": 1, "name": pub.BUILD_ARTIFACT}, {"id": 2, "name": pub.BUILD_ARTIFACT}]):
            with self.assertRaisesRegex(pub.Refused, "exactly one live"):
                self.verify(artifacts=artifacts)


class PrepareTests(unittest.TestCase):

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.shared = Path(tmp.name) / "shared"
        self.work = Path(tmp.name) / "work"
        self.work.mkdir()
        self.shared.mkdir()

    def prepare(self, document, commit=SHA, run_id=7, date="2026-10-20T10:00:00Z", **kw):
        artifact = self.work / "openapi.json"
        artifact.write_bytes(raw(document))
        return pub.prepare(artifact, record_for(document, commit, run_id), date, self.shared, repo=BACKEND, **kw)

    def current(self):
        return json.loads((self.shared / "api/implemented/current.json").read_text())

    def test_initial_publication_is_sound_and_accepted_by_the_consumer_client(self):
        version = self.prepare(BASE)
        self.assertEqual(self.current()["version"], version)
        self.assertEqual(pub.verify_tree(self.shared), [])
        manifest, _, contract = client.resolve_version(f"file:{self.shared}", "current")
        self.assertEqual(manifest["source"]["repository"], BACKEND)
        self.assertEqual(manifest["approval"]["approval_method"], pub.APPROVAL_METHOD)
        self.assertEqual(contract, raw(BASE))

    def test_next_versions_chain_and_classify(self):
        first = self.prepare(BASE)
        second = self.prepare(DOC_ONLY, commit=SHA2, run_id=8, date="2026-10-21T10:00:00Z")
        third = self.prepare(ADDITIVE, commit="c" * 40, run_id=9, date="2026-10-22T10:00:00Z")
        index = json.loads((self.shared / "api/implemented/index.json").read_text())
        self.assertEqual([v["version"] for v in index["versions"]], [first, second, third])
        self.assertEqual(index["versions"][1]["compatibility"]["DOCUMENTATION_ONLY"], 1)
        self.assertEqual(index["versions"][2]["compatibility"]["NON_BREAKING"], 1)
        self.assertEqual(pub.verify_tree(self.shared), [])
        self.assertIn(third, (self.shared / "api/implemented/CHANGELOG.md").read_text())

    def test_breaking_and_unclassified_changes_fail_closed_unless_explicitly_allowed(self):
        self.prepare(BASE)
        with self.assertRaisesRegex(pub.Refused, "breaking"):
            self.prepare(BREAKING, commit=SHA2, run_id=8, date="2026-10-21T10:00:00Z")
        version = self.prepare(BREAKING, commit=SHA2, run_id=8, date="2026-10-21T10:00:00Z", allow_breaking=True,
                               approved_scope=["public.a removed"])
        approval = json.loads((self.shared / f"api/implemented/versions/{version}/approval.json").read_text())
        self.assertTrue(approval["allow_breaking"])
        self.assertEqual(approval["approved_scope"], ["public.a removed"])
        self.assertEqual(pub.verify_tree(self.shared), [])

    def test_refusal_lists_every_blocker_with_its_location(self):
        self.prepare(TWO)
        both = doc({"/api/public/c": {"get": operation("public.c", extra={"vendorFlag": 1})}})
        with self.assertRaises(pub.Refused) as caught:
            self.prepare(both, commit=SHA2, run_id=8, date="2026-10-21T10:00:00Z")
        message = str(caught.exception)
        self.assertIn("unclassified change(s)", message)
        self.assertIn("breaking change(s)", message)
        self.assertIn("publish:   BREAKING operation_removed at paths./api/public/a.get", message)
        self.assertIn("publish:   UNKNOWN operation_keyword_changed at paths./api/public/c.get.vendorFlag", message)
        self.assertEqual(pub.verify_tree(self.shared), [])

    def test_refusal_names_only_the_blockers_that_were_not_allowed(self):
        self.prepare(TWO)
        both = doc({"/api/public/c": {"get": operation("public.c", extra={"vendorFlag": 1})}})
        with self.assertRaises(pub.Refused) as caught:
            self.prepare(both, commit=SHA2, run_id=8, date="2026-10-21T10:00:00Z", allow_breaking=True)
        self.assertIn("unclassified change(s)", str(caught.exception))
        self.assertNotIn("breaking change(s)", str(caught.exception))

    def test_long_refusals_are_truncated_with_a_count(self):
        many = doc({f"/api/public/n{i}": {"get": operation(f"public.n{i}")} for i in range(15)})
        self.prepare(many)
        with self.assertRaises(pub.Refused) as caught:
            self.prepare(BASE, commit=SHA2, run_id=8, date="2026-10-21T10:00:00Z")
        self.assertIn("... and 3 more BREAKING change(s)", str(caught.exception))

    def test_narrowed_response_const_in_a_tuple_publishes_without_any_allow_flag(self):
        def with_usage(position_schema):
            schema = {"type": "array", "minItems": 1, "maxItems": 1, "prefixItems": [position_schema]}
            return doc({"/api/public/a": {"get": operation("public.a", extra={"responses": {"200": {
                "description": "ok", "content": {"application/json": {"schema": schema}}}}})}})
        self.prepare(with_usage({"type": "object", "properties": {"limit": {"type": "integer"}}}))
        version = self.prepare(
            with_usage({"type": "object", "properties": {"limit": {"type": "integer", "const": 0}}}),
            commit=SHA2, run_id=8, date="2026-10-21T10:00:00Z")
        approval = json.loads((self.shared / f"api/implemented/versions/{version}/approval.json").read_text())
        self.assertFalse(approval["allow_breaking"])
        self.assertFalse(approval["allow_unknown"])
        self.assertEqual(pub.verify_tree(self.shared), [])

    def test_same_bytes_are_refused_as_already_published_and_rollback_and_stale_are_refused(self):
        first = self.prepare(BASE)
        with self.assertRaisesRegex(pub.Refused, "already published"):
            self.prepare(BASE)
        second = self.prepare(ADDITIVE, commit=SHA2, run_id=8, date="2026-10-21T10:00:00Z")
        self.assertNotEqual(first, second)
        with self.assertRaisesRegex(pub.Refused, "roll back"):
            self.prepare(BASE)
        with self.assertRaisesRegex(pub.Refused, "stale"):
            self.prepare(DOC_ONLY, commit="c" * 40, run_id=9, date="2026-10-19T10:00:00Z")

    def test_a_build_from_another_repository_or_for_other_bytes_is_refused(self):
        artifact = self.work / "openapi.json"
        artifact.write_bytes(raw(BASE))
        with self.assertRaisesRegex(pub.Refused, "accepts only"):
            pub.prepare(artifact, {**record_for(BASE), "repository": "evil/x"}, "2026-10-20T10:00:00Z",
                        self.shared, repo=BACKEND)
        with self.assertRaisesRegex(pub.Refused, "not the contract"):
            pub.prepare(artifact, record_for(ADDITIVE), "2026-10-20T10:00:00Z", self.shared, repo=BACKEND)

    def test_existing_versions_are_never_rewritten(self):
        first = self.prepare(BASE)
        before = (self.shared / f"api/implemented/versions/{first}/openapi.json").read_bytes()
        self.prepare(ADDITIVE, commit=SHA2, run_id=8, date="2026-10-21T10:00:00Z")
        self.assertEqual((self.shared / f"api/implemented/versions/{first}/openapi.json").read_bytes(), before)


class VerifyTreeTests(unittest.TestCase):

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.shared = Path(tmp.name)
        artifact = self.shared / "o.json"
        artifact.write_bytes(raw(BASE))
        self.first = pub.prepare(artifact, record_for(BASE), "2026-10-20T10:00:00Z", self.shared, repo=BACKEND)
        artifact.unlink()
        for cmd in (["init", "-q"], ["config", "user.email", "t@t"], ["config", "user.name", "t"],
                    ["add", "-A"], ["commit", "-qm", "base"]):
            subprocess.run(["git", "-C", str(self.shared), *cmd], check=True, capture_output=True)

    def vdir(self, v=None):
        return self.shared / "api/implemented/versions" / (v or self.first)

    def test_the_real_published_tree_of_this_repository_is_sound(self):
        self.assertEqual(pub.verify_tree(REPO_ROOT), [])

    def test_tampering_is_detected(self):
        (self.vdir() / "openapi.json").write_bytes(raw(ADDITIVE))
        self.assertTrue(any("digest" in p for p in pub.verify_tree(self.shared)))

    def test_approval_rules_are_enforced(self):
        path = self.vdir() / "approval.json"
        approval = json.loads(path.read_text())
        approval["approval_method"] = "email"
        path.write_text(json.dumps(approval))
        self.assertTrue(pub.verify_tree(self.shared))

    def test_immutability_against_the_base_ref(self):
        self.assertEqual(pub.verify_tree(self.shared, "HEAD", max_new_versions=1), [])
        (self.vdir() / "compatibility.md").write_text("changed")
        problems = pub.verify_tree(self.shared, "HEAD")
        self.assertTrue(any("modified" in p for p in problems), problems)

    def test_deleting_a_published_file_is_detected(self):
        (self.vdir() / "compatibility.md").unlink()
        self.assertTrue(any("deleted" in p or "unreadable" in p for p in pub.verify_tree(self.shared, "HEAD")))

    def test_more_than_one_new_version_in_a_change_is_refused(self):
        artifact = self.shared / "o.json"
        for i, document in enumerate((ADDITIVE, doc({"/api/public/a": {"get": operation("public.a")},
                                                      "/api/public/b": {"get": operation("public.b")},
                                                      "/api/public/c": {"get": operation("public.c")}}))):
            artifact.write_bytes(raw(document))
            pub.prepare(artifact, record_for(document, "c" * 39 + str(i), 20 + i), f"2026-10-2{1 + i}T10:00:00Z",
                        self.shared, repo=BACKEND)
        artifact.unlink()
        self.assertTrue(any("new versions" in p for p in pub.verify_tree(self.shared, "HEAD", max_new_versions=1)))


class VerifyMergeTests(unittest.TestCase):

    class Api:
        def __init__(self, pulls, reviews):
            self.pulls, self.reviews = pulls, reviews

        def get(self, path):
            return self.reviews if path.endswith("/reviews") else self.pulls

    PULL = {"number": 9, "merged_at": "2026-10-20T10:00:00Z", "head": {"ref": "publish/2026.10.20-abc"},
            "user": {"login": "api-gap-automation[bot]"}}
    REVIEW = {"user": {"login": "abdo-taher"}, "state": "APPROVED", "author_association": "OWNER"}

    def check(self, pulls, reviews=None):
        return pub.verify_merge(self.Api(pulls, reviews or []), BACKEND, SHA)

    def test_a_publisher_pull_request_passes(self):
        self.assertEqual(self.check([self.PULL]), [])

    def test_a_direct_push_is_reported(self):
        self.assertTrue(any("direct push" in p for p in self.check([])))
        self.assertTrue(any("direct push" in p for p in self.check([{**self.PULL, "merged_at": None}])))

    def test_other_branches_are_reported(self):
        self.assertTrue(self.check([{**self.PULL, "head": {"ref": "feature/x"}}]))


class RedirectTests(unittest.TestCase):

    def test_the_token_is_not_forwarded_to_the_storage_host_after_a_redirect(self):
        seen = {}

        class Storage(BaseHTTPRequestHandler):
            def log_message(self, *a): pass
            def do_GET(self):
                seen["storage_auth"] = self.headers.get("Authorization")
                self.send_response(200); self.send_header("Content-Length", "2"); self.end_headers(); self.wfile.write(b"ok")

        storage = ThreadingHTTPServer(("127.0.0.1", 0), Storage)
        threading.Thread(target=storage.serve_forever, daemon=True).start()
        target = f"http://127.0.0.1:{storage.server_address[1]}/blob"

        class Api(BaseHTTPRequestHandler):
            def log_message(self, *a): pass
            def do_GET(self):
                seen["api_auth"] = self.headers.get("Authorization")
                self.send_response(302); self.send_header("Location", target); self.end_headers()

        api = ThreadingHTTPServer(("127.0.0.1", 0), Api)
        threading.Thread(target=api.serve_forever, daemon=True).start()
        self.addCleanup(storage.shutdown); self.addCleanup(api.shutdown)
        self.addCleanup(storage.server_close); self.addCleanup(api.server_close)
        data = pub.GitHubApi("SECRET-TOKEN", base=f"http://127.0.0.1:{api.server_address[1]}").download("x/zip")
        self.assertEqual(data, b"ok")
        self.assertEqual(seen["api_auth"], "Bearer SECRET-TOKEN")
        self.assertIsNone(seen["storage_auth"])


class ClientAcceptanceTests(unittest.TestCase):

    def test_the_client_rejects_a_v2_approval_without_the_github_method_or_build(self):
        approval = {"schema": pub.APPROVAL_SCHEMA, "decision": "APPROVED", "approved_artifact_sha256": "d",
                    "approval_method": "email", "build": {}}
        data = json.dumps(approval).encode()
        manifest = {"approval": {"approval_manifest_sha256": hashlib.sha256(data).hexdigest()},
                    "files": {"approval.json": hashlib.sha256(data).hexdigest()}}
        with self.assertRaises(client.CheckFailed):
            client.verify_approval_evidence(manifest, data, "d")

    def test_v1_still_needs_its_signature(self):
        approval = {"decision": "APPROVED", "approved_artifact_sha256": "d"}
        data = json.dumps(approval).encode()
        manifest = {"approval": {"approval_manifest_sha256": hashlib.sha256(data).hexdigest()},
                    "files": {"approval.json": hashlib.sha256(data).hexdigest()}}
        with self.assertRaises(client.CheckFailed):
            client.verify_approval_evidence(manifest, data, "d")


if __name__ == "__main__":
    unittest.main()
