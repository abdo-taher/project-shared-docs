import contextlib
import io
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import check_resolutions  # noqa: E402
from fakes import LIST_OPERATION, contract, merge_paths  # noqa: E402
from gap_coordinator import RESOLUTION_SCHEMA, load_policy  # noqa: E402
from gap_http import Http  # noqa: E402
from gap_preflight import Report, activation_check, backend_checks, github_checks  # noqa: E402

POLICY = load_policy(HERE.parent / "policy.json")
GH_TOKEN = "github_pat_" + "A" * 40
BE_TOKEN = "github_pat_" + "B" * 40
FP = "a" * 64


class Stub(ThreadingHTTPServer):
    def __init__(self, routes):
        super().__init__(("127.0.0.1", 0), StubHandler)
        self.routes = routes
        self.seen = []

    @property
    def base(self):
        return f"http://127.0.0.1:{self.server_address[1]}"


class StubHandler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        path = self.path.split("?")[0].lstrip("/")
        self.server.seen.append(dict(self.headers))
        status, body, headers = self.server.routes.get(path, (404, {}, {}))
        payload = json.dumps(body).encode()
        self.send_response(status)
        for k, v in headers.items():
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def serve(routes):
    server = Stub(routes)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


class PreflightTests(unittest.TestCase):

    def run_github(self, routes, token=GH_TOKEN):
        server = serve(routes)
        self.addCleanup(server.shutdown)
        report = Report()
        github_checks(report, POLICY, token, http=Http(server.base, {"Authorization": f"Bearer {token}"}, attempts=1))
        return report, server

    def statuses(self, report):
        return {check: status for status, check, _ in report.rows}

    def good_github(self):
        return {"user": (200, {"login": "abdo-taher"}, {}),
                "repos/abdo-taher/project-shared-docs": (200, {}, {"X-RateLimit-Remaining": "4999"}),
                "repos/abdo-taher/project-shared-docs/issues": (200, [], {}),
                "repos/abdo-taher/project-shared-docs/collaborators/abdo-taher/permission": (200, {"role_name": "admin"}, {})}

    def test_github_token_that_cannot_verify_trust_fails_the_preflight(self):
        routes = self.good_github()
        del routes["repos/abdo-taher/project-shared-docs/collaborators/abdo-taher/permission"]
        report, _ = self.run_github(routes)
        self.assertEqual(self.statuses(report)["github can verify reporter trust"], "FAIL")

    def test_github_least_privilege_token_passes(self):
        report, server = self.run_github(self.good_github())
        s = self.statuses(report)
        self.assertFalse(report.failed, report.rows)
        self.assertEqual(s["github least privilege"], "PASS")
        self.assertEqual(s["github write permission"], "SKIP")

    def test_github_token_that_can_read_the_development_repository_is_too_broad(self):
        routes = {**self.good_github(), "repos/abdo-taher/capitalix": (200, {}, {})}
        report, _ = self.run_github(routes)
        self.assertEqual(self.statuses(report)["github least privilege"], "FAIL")

    def test_github_wrong_identity_and_invalid_token(self):
        report, _ = self.run_github({**self.good_github(), "user": (200, {"login": "someone-else"}, {})})
        self.assertEqual(self.statuses(report)["github identity"], "FAIL")
        report, _ = self.run_github({"user": (401, {}, {})})
        self.assertTrue(report.failed)

    def test_github_classic_token_warns_and_missing_token_fails(self):
        report, _ = self.run_github(self.good_github(), token="ghp_" + "C" * 36)
        self.assertEqual(self.statuses(report)["github token type"], "WARN")
        missing = Report()
        github_checks(missing, POLICY, None)
        self.assertTrue(missing.failed)

    def backend_routes(self, push=True, admin=False, issues=200, pulls=200):
        repo = "repos/abdo-taher/capitalix"
        return {repo: (200, {"private": True, "permissions": {"admin": admin, "push": push, "pull": True}}, {}),
                repo + "/issues": (issues, [], {}), repo + "/pulls": (pulls, [], {})}

    def run_backend(self, routes, token=BE_TOKEN):
        server = serve(routes)
        self.addCleanup(server.shutdown)
        report = Report()
        backend_checks(report, POLICY, token, http=Http(server.base, {"Authorization": f"Bearer {token}"}, attempts=1))
        return report

    def test_backend_fine_grained_token_passes(self):
        report = self.run_backend(self.backend_routes())
        self.assertFalse(report.failed, report.rows)
        s = self.statuses(report)
        self.assertEqual((s["backend token type"], s["backend repository role"]), ("PASS", "PASS"))

    def test_backend_problems(self):
        self.assertEqual(self.statuses(self.run_backend(self.backend_routes(admin=True)))["backend repository role"], "WARN")
        self.assertEqual(self.statuses(self.run_backend(self.backend_routes(issues=403)))["backend issues readable"], "FAIL")
        self.assertEqual(self.statuses(self.run_backend(self.backend_routes(pulls=404)))["backend pull requests readable"], "FAIL")
        self.assertEqual(self.statuses(self.run_backend(self.backend_routes(), token="gho_" + "C" * 36))["backend token type"], "WARN")
        self.assertTrue(self.run_backend({"repos/abdo-taher/capitalix": (404, {}, {})}).failed)
        missing = Report()
        backend_checks(missing, POLICY, None)
        self.assertTrue(missing.failed)

    def test_no_token_value_ever_appears_in_the_report(self):
        for report in (self.run_github({**self.good_github(), "repos/abdo-taher/capitalix": (200, {}, {})})[0],
                       self.run_github({"user": (401, {"message": GH_TOKEN}, {})})[0],
                       self.run_backend({"repos/abdo-taher/capitalix": (403, {"message": BE_TOKEN}, {})})):
            text = json.dumps(report.rows)
            self.assertNotIn(GH_TOKEN, text)
            self.assertNotIn(BE_TOKEN, text)

    def test_activation_flag(self):
        report = Report()
        activation_check(report, {})
        self.assertEqual(report.rows[0][0], "PASS")
        activation_check(report, {"API_GAP_AUTOMATION_ENABLED": "true"})
        self.assertEqual(report.rows[1][0], "WARN")


class ResolutionGuardTests(unittest.TestCase):

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.dir = self.root / "resolutions"
        self.dir.mkdir()
        self.contract = self.root / "openapi.json"
        self.contract.write_text(json.dumps(merge_paths(contract(), LIST_OPERATION)))

    def write(self, **overrides):
        evidence = {"schema": RESOLUTION_SCHEMA, "fingerprint": FP, "backend_issue": 4, "root_cause": "A",
                    "summary": "s", "tests": ["t"],
                    "checks": [{"check": "operation_exists", "operation_id": "owner.sales.customers.index"}],
                    **overrides}
        (self.dir / f"{FP[:16]}.json").write_text(json.dumps(evidence))

    def test_holding_resolutions_pass(self):
        self.write()
        self.assertEqual(check_resolutions.check_tree(self.dir, self.contract), [])

    def test_a_dropped_fix_fails_the_guard(self):
        self.write()
        self.contract.write_text(json.dumps(contract()))  # a later promotion without the list operation
        problems = check_resolutions.check_tree(self.dir, self.contract)
        self.assertEqual(len(problems), 1)
        self.assertIn("owner.sales.customers.index", problems[0])
        buffer = io.StringIO()
        with contextlib.redirect_stderr(buffer), contextlib.redirect_stdout(io.StringIO()):
            code = check_resolutions.main(["--dir", str(self.dir), "--contract", str(self.contract)])
        self.assertEqual(code, 1)
        self.assertIn("REGRESSION", buffer.getvalue())

    def test_invalid_files(self):
        self.write()
        (self.dir / f"{FP[:16]}.json").rename(self.dir / "wrongname.json")
        self.assertIn("file name", check_resolutions.check_tree(self.dir, self.contract)[0])
        (self.dir / "wrongname.json").write_text("not json")
        self.assertIn("not a JSON object", check_resolutions.check_tree(self.dir, self.contract)[0])

    def test_no_directory_or_files_is_fine(self):
        self.assertEqual(check_resolutions.check_tree(self.dir, self.contract), [])
        self.assertEqual(check_resolutions.main(["--dir", str(self.root / "missing")]), 0)


if __name__ == "__main__":
    unittest.main()
