"""Remote transport: anonymous public access, authenticated fallback, failure handling.

A local HTTP server emulates raw.githubusercontent.com (/raw/OWNER/REPO/REF/PATH)
and the GitHub contents API (/api/repos/OWNER/REPO/contents/PATH, which
requires `Authorization: Bearer good-token`). The tool runs in-process with its
endpoints pointed at the server; failures are injected per path.
"""

import contextlib
import io
import json
import os
import stat
import sys
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import capitalix_contract as tool  # noqa: E402
from test_capitalix_contract import CONTRACT_V1, publish  # noqa: E402

REPO = "abdo-taher/project-shared-docs"
SOURCE = f"github:{REPO}"
CURRENT = "api/implemented/versions/2026.10.19-aaaa"


class FakeGitHub(BaseHTTPRequestHandler):
    root: Path
    overrides: dict
    hits: list

    def log_message(self, *args):  # keep test output clean
        pass

    def do_GET(self):
        self.hits.append((self.path, self.headers.get("Authorization")))
        if self.path.startswith("/raw/"):
            owner, repo, _ref, rel = self.path[5:].split("/", 3)
            if f"{owner}/{repo}" != REPO or getattr(self.server, "private", False):
                return self.reply(404, b"404: Not Found")
        elif self.path.startswith("/api/repos/"):
            if self.headers.get("Authorization") != "Bearer good-token":
                return self.reply(401, b'{"message":"Bad credentials"}')
            rel = self.path.split("/contents/", 1)[1].split("?")[0]
        else:
            return self.reply(404, b"")
        override = self.overrides.get(rel)
        if override:
            action = override.pop(0) if isinstance(override, list) else override
            if action == "timeout":
                time.sleep(1.5)
                return self.reply(200, b"late")
            status, headers, body = action
            return self.reply(status, body, headers)
        target = self.root / rel
        if not target.is_file():
            return self.reply(404, b"404: Not Found")
        self.reply(200, target.read_bytes())

    def reply(self, status, body, headers=None):
        self.send_response(status)
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass


class RemoteAccessTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.shared = base / "shared"
        self.project = base / "project"
        self.project.mkdir()
        self.bin = base / "bin"
        self.bin.mkdir()
        publish(self.shared, "2026.10.19-aaaa", CONTRACT_V1, "2026-10-19T00:00:00Z", "c1")
        handler = type("Handler", (FakeGitHub,), {"root": self.shared, "overrides": {}, "hits": []})
        self.handler = handler
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        url = f"http://127.0.0.1:{self.server.server_address[1]}"
        self.patches = [
            mock.patch.object(tool, "RAW_BASE", f"{url}/raw"),
            mock.patch.object(tool, "API_BASE", f"{url}/api"),
            mock.patch.object(tool, "HTTP_TIMEOUT", 0.5),
            mock.patch.object(tool, "MAX_RETRY_WAIT", 0),
            # No credentials and no gh unless a test says otherwise.
            mock.patch.dict(os.environ, {"PATH": str(self.bin)}, clear=True),
        ]
        for patch in self.patches:
            patch.start()
        self.cwd = os.getcwd()
        os.chdir(self.project)

    def tearDown(self):
        os.chdir(self.cwd)
        for patch in reversed(self.patches):
            patch.stop()
        self.server.shutdown()
        self.server.server_close()
        self.tmp.cleanup()

    def run_tool(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = tool.main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def fake_gh(self, logged_in: bool, serve: Path | None = None):
        """A stand-in `gh`: `auth status` reflects logged_in; `api` serves files from serve."""
        script = self.bin / "gh"
        body = "#!/bin/sh\nPATH=/usr/bin:/bin\n"
        body += f'if [ "$1" = auth ]; then exit {0 if logged_in else 1}; fi\n'
        if serve:
            body += 'for a; do last="$a"; done\n'
            body += f'cat "{serve}/${{last#*/contents/}}" || exit 1\n'
        else:
            body += "echo 'not logged in' >&2; exit 1\n"
        script.write_text(body)
        script.chmod(script.stat().st_mode | stat.S_IEXEC)

    def lock(self):
        return json.loads((self.project / ".capitalix-contract/contract.lock").read_text())

    def raw_hits(self):
        return [path for path, _ in self.handler.hits if path.startswith("/raw/")]

    # ---------------------------------------------------------- anonymous access

    def test_anonymous_init_without_gh_or_tokens(self):
        self.assertIsNone(tool.shutil.which("gh"))
        self.assertNotIn("GITHUB_TOKEN", os.environ)
        self.assertNotIn("GH_TOKEN", os.environ)
        code, out, err = self.run_tool("init", "--source", SOURCE)
        self.assertEqual(code, 0, err)
        self.assertEqual(self.lock()["version"], "2026.10.19-aaaa")
        self.assertTrue(all(auth is None for _, auth in self.handler.hits), "no credentials sent")
        self.assertTrue(all(p.startswith(f"/raw/{REPO}/HEAD/") for p in self.raw_hits()))

    def test_anonymous_init_with_gh_installed_but_logged_out(self):
        self.fake_gh(logged_in=False)
        code, _, err = self.run_tool("init", "--source", SOURCE)
        self.assertEqual(code, 0, err)

    def test_anonymous_remote_verification(self):
        self.assertEqual(self.run_tool("init", "--source", SOURCE)[0], 0)
        code, out, err = self.run_tool("verify", "--remote")
        self.assertEqual(code, 0, err)
        self.assertIn("published manifest OK", out)

    def test_anonymous_status_and_inspection(self):
        self.assertEqual(self.run_tool("init", "--source", SOURCE)[0], 0)
        code, out, _ = self.run_tool("status")
        self.assertEqual(code, 0)
        self.assertIn("up to date", out)
        code, out, _ = self.run_tool("inspect", "customers", "--method", "POST", "owner")
        self.assertEqual(code, 0)
        self.assertEqual([op["operationId"] for op in json.loads(out)["operations"]],
                         ["owner.sales.customers.store"])

    def test_anonymous_update_is_explicit(self):
        self.assertEqual(self.run_tool("init", "--source", SOURCE)[0], 0)
        newer = json.loads(json.dumps(CONTRACT_V1))
        newer["paths"]["/api/owner/new"] = {"get": {"operationId": "new", "responses": {"200": {"description": "ok"}}}}
        publish(self.shared, "2026.10.20-bbbb", newer, "2026-10-20T00:00:00Z", "c2")
        # Nothing but `update` may move the pin.
        for command in (["status"], ["verify", "--remote"], ["inspect", "new"], ["sync"]):
            self.run_tool(*command)
            self.assertEqual(self.lock()["version"], "2026.10.19-aaaa", command)
        code, _, _ = self.run_tool("init", "--source", SOURCE)
        self.assertEqual(code, 3, "init must refuse to replace an existing pin")
        code, out, err = self.run_tool("update")
        self.assertEqual(code, 0, err)
        self.assertEqual(self.lock()["version"], "2026.10.20-bbbb")
        self.assertIn("added   GET /api/owner/new", out)

    def test_pinned_version_not_published(self):
        code, _, err = self.run_tool("init", "--source", SOURCE, "--version", "2020.01.01-ffff")
        self.assertEqual(code, 1)
        self.assertIn("is not published", err)
        self.assertFalse((self.project / ".capitalix-contract").exists())

    # ---------------------------------------------------------- authenticated / private

    def test_token_uses_authenticated_api(self):
        with mock.patch.dict(os.environ, {"GITHUB_TOKEN": "good-token"}):
            code, _, err = self.run_tool("init", "--source", SOURCE)
        self.assertEqual(code, 0, err)
        self.assertTrue(self.handler.hits)
        self.assertTrue(all(path.startswith("/api/") and auth == "Bearer good-token"
                            for path, auth in self.handler.hits))

    def test_gh_token_alias_is_honoured(self):
        with mock.patch.dict(os.environ, {"GH_TOKEN": "good-token"}):
            self.assertEqual(self.run_tool("init", "--source", SOURCE)[0], 0)

    def test_rejected_token_fails_without_leaking_it(self):
        with mock.patch.dict(os.environ, {"GITHUB_TOKEN": "s3cr3t-bad-token"}):
            code, out, err = self.run_tool("init", "--source", SOURCE)
        self.assertEqual(code, 2)
        self.assertIn("HTTP 401", err)
        self.assertNotIn("s3cr3t-bad-token", out + err)

    def test_private_repository_falls_back_to_logged_in_gh(self):
        self.server.private = True
        self.fake_gh(logged_in=True, serve=self.shared)
        code, _, err = self.run_tool("init", "--source", SOURCE)
        self.assertEqual(code, 0, err)
        self.assertEqual(self.lock()["sha256"], json.loads(
            (self.shared / "api/implemented/current.json").read_text())["sha256"])

    def test_private_repository_without_credentials_explains_how_to_authenticate(self):
        self.server.private = True
        code, _, err = self.run_tool("init", "--source", SOURCE)
        self.assertEqual(code, 2)
        self.assertIn("GITHUB_TOKEN", err)
        self.assertIn("gh auth login", err)

    # ---------------------------------------------------------- integrity failures

    def tamper(self, rel, transform):
        target = self.shared / rel
        target.write_bytes(transform(target.read_bytes()))

    def test_invalid_manifest_json(self):
        self.tamper(f"{CURRENT}/manifest.json", lambda b: b"{not json")
        code, _, err = self.run_tool("init", "--source", SOURCE)
        self.assertEqual(code, 1)
        self.assertIn("not valid JSON", err)

    def test_missing_manifest(self):
        (self.shared / f"{CURRENT}/manifest.json").unlink()
        code, _, err = self.run_tool("init", "--source", SOURCE)
        self.assertEqual(code, 2)
        self.assertIn("manifest.json: not found", err)

    def test_tampered_approval_evidence(self):
        self.tamper(f"{CURRENT}/approval.json", lambda b: b.replace(b"MR-!1", b"MR-!9"))
        code, _, err = self.run_tool("init", "--source", SOURCE)
        self.assertEqual(code, 1)
        self.assertIn("approval evidence does not match", err)

    def test_approval_for_other_bytes(self):
        manifest_path = self.shared / f"{CURRENT}/manifest.json"
        approval_path = self.shared / f"{CURRENT}/approval.json"
        approval = json.loads(approval_path.read_text())
        approval["approved_artifact_sha256"] = "0" * 64
        approval_path.write_text(json.dumps(approval))
        manifest = json.loads(manifest_path.read_text())
        digest = tool.sha256(approval_path.read_bytes())
        manifest["approval"]["approval_manifest_sha256"] = digest
        manifest["files"]["approval.json"] = digest
        manifest_path.write_text(json.dumps(manifest))
        code, _, err = self.run_tool("init", "--source", SOURCE)
        self.assertEqual(code, 1)
        self.assertIn("does not approve this exact contract", err)

    def test_contract_hash_mismatch(self):
        self.tamper(f"{CURRENT}/openapi.json", lambda b: b.replace(b"customers", b"clients"))
        code, _, err = self.run_tool("init", "--source", SOURCE)
        self.assertEqual(code, 1)
        self.assertIn("does not match the published digest", err)
        self.assertFalse((self.project / ".capitalix-contract/contract.lock").exists(),
                         "an unverified contract is never pinned")

    def test_remote_verify_detects_changed_published_source(self):
        self.assertEqual(self.run_tool("init", "--source", SOURCE)[0], 0)
        manifest_path = self.shared / f"{CURRENT}/manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["source"]["commit"] = "other"
        manifest_path.write_text(json.dumps(manifest))
        code, _, err = self.run_tool("verify", "--remote")
        self.assertEqual(code, 1)
        self.assertIn("different source", err)

    # ---------------------------------------------------------- transport failures

    def test_network_timeout(self):
        self.handler.overrides["api/implemented/current.json"] = ["timeout"] * 3
        code, _, err = self.run_tool("init", "--source", SOURCE)
        self.assertEqual(code, 2)
        self.assertIn("timed out", err)

    def test_timeout_then_success_is_retried(self):
        self.handler.overrides["api/implemented/current.json"] = ["timeout"]
        code, _, err = self.run_tool("init", "--source", SOURCE)
        self.assertEqual(code, 0, err)

    def test_http_404(self):
        code, _, err = self.run_tool("init", "--source", "github:abdo-taher/no-such-repo")
        self.assertEqual(code, 2)
        self.assertIn("not found", err)

    def test_http_403_rate_limit_is_retried_then_reported(self):
        limited = (403, {"X-RateLimit-Remaining": "0"}, b"rate limited")
        self.handler.overrides["api/implemented/current.json"] = [limited] * 3
        code, _, err = self.run_tool("init", "--source", SOURCE)
        self.assertEqual(code, 2)
        self.assertIn("rate limited (HTTP 403) after 3 attempts", err)

    def test_http_429_with_retry_after_recovers(self):
        self.handler.overrides["api/implemented/current.json"] = [(429, {"Retry-After": "0"}, b"slow down")]
        code, _, err = self.run_tool("init", "--source", SOURCE)
        self.assertEqual(code, 0, err)

    def test_plain_http_403_is_not_retried(self):
        self.handler.overrides["api/implemented/current.json"] = [(403, {}, b"forbidden")]
        code, _, err = self.run_tool("init", "--source", SOURCE)
        self.assertEqual(code, 2)
        self.assertIn("HTTP 403", err)
        self.assertEqual(len([p for p in self.raw_hits() if p.endswith("current.json")]), 1)

    def test_invalid_pointer_json(self):
        self.handler.overrides["api/implemented/current.json"] = [(200, {}, b"<html>")]
        code, _, err = self.run_tool("init", "--source", SOURCE)
        self.assertEqual(code, 2)
        self.assertIn("not valid JSON", err)

    def test_rejects_malformed_repository(self):
        code, _, err = self.run_tool("init", "--source", "github:../../etc")
        self.assertEqual(code, 2)
        self.assertIn("invalid repository", err)


if __name__ == "__main__":
    unittest.main()
