"""Coordinator + the real GitHubBackend adapter against a stateful stub of the GitHub REST API.

The full lifecycle with nothing mocked between the coordinator and the HTTP layer: intake -> backend issue ->
pull request -> merged (not published) -> published -> consumer confirmation -> resolved."""
import json
import re
import sys
import threading
import unittest
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gap_github_backend import GitHubBackend  # noqa: E402
from gap_http import Http  # noqa: E402
from test_gap_coordinator import DEV_BRANCH, RESOLUTION_SCHEMA, VERIFY_MARKER, Env, fp_of  # noqa: E402

REPO = "abdo-taher/capitalix"
MERGE_SHA = "c" * 40


class StubGitHub(ThreadingHTTPServer):
    def __init__(self):
        super().__init__(("127.0.0.1", 0), Handler)
        self.issues, self.comments, self.events, self.prs, self.files = {}, {}, {}, {}, {}
        self.timeline: dict[int, list] = {}
        self.calls: list[tuple[str, str]] = []

    @property
    def base(self):
        return f"http://127.0.0.1:{self.server_address[1]}"


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, status, body):
        raw = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def issue_json(self, i):
        return {"number": i["number"], "title": i["title"], "body": i["body"], "state": i["state"],
                "labels": [{"name": l} for l in i["labels"]], "html_url": f"u/{i['number']}",
                "created_at": "2026-10-19T00:00:00Z", "user": {"login": "abdo-taher"}}

    def handle_any(self, method):
        s = self.server
        length = int(self.headers.get("Content-Length") or 0)
        body = json.loads(self.rfile.read(length)) if length else None
        url = urllib.parse.urlsplit(self.path)
        path, query = url.path.lstrip("/"), urllib.parse.parse_qs(url.query)
        s.calls.append((method, path))
        prefix = f"repos/{REPO}/"
        if not path.startswith(prefix):
            return self.send(404, {})
        rest = path[len(prefix):]
        if rest == "issues" and method == "GET":
            wanted = query.get("state", ["open"])[0]
            items = [i for i in s.issues.values() if "api-gap" in i["labels"]
                     and (wanted == "all" or i["state"] == wanted)]
            return self.send(200, [self.issue_json(i) for i in items])
        if rest == "issues" and method == "POST":
            number = max(s.issues, default=0) + 1
            s.issues[number] = {"number": number, "title": body["title"], "body": body["body"], "state": "open",
                                "labels": list(body["labels"])}
            return self.send(201, self.issue_json(s.issues[number]))
        m = re.fullmatch(r"issues/(\d+)(?:/(\w+)(?:/(.+))?)?", rest)
        if m:
            n, sub, arg = int(m.group(1)), m.group(2), m.group(3)
            issue = s.issues.get(n)
            if issue is None:
                return self.send(404, {})
            if sub is None and method == "GET":
                return self.send(200, self.issue_json(issue))
            if sub is None and method == "PATCH":
                issue["state"] = body.get("state", issue["state"])
                return self.send(200, self.issue_json(issue))
            if sub == "labels" and method == "POST":
                issue["labels"] += [l for l in body["labels"] if l not in issue["labels"]]
                return self.send(200, [])
            if sub == "labels" and method == "DELETE":
                name = urllib.parse.unquote(arg)
                if name not in issue["labels"]:
                    return self.send(404, {})
                issue["labels"].remove(name)
                return self.send(200, [])
            if sub == "comments":
                if method == "POST":
                    s.comments.setdefault(n, []).append({"body": body["body"], "id": len(s.comments.get(n, [])) + 1})
                    return self.send(201, s.comments[n][-1])
                return self.send(200, s.comments.get(n, []))
            if sub == "events":
                return self.send(200, s.events.get(n, []))
            if sub == "timeline":
                return self.send(200, s.timeline.get(n, []))
        m = re.fullmatch(r"pulls/(\d+)", rest)
        if m and int(m.group(1)) in s.prs:
            return self.send(200, s.prs[int(m.group(1))])
        if rest.startswith("contents/"):
            key = (urllib.parse.unquote(rest[len("contents/"):]), query.get("ref", [""])[0])
            return self.send(200, s.files[key]) if key in s.files else self.send(404, {})
        return self.send(404, {})

    do_GET = lambda self: self.handle_any("GET")
    do_POST = lambda self: self.handle_any("POST")
    do_PATCH = lambda self: self.handle_any("PATCH")
    do_DELETE = lambda self: self.handle_any("DELETE")


class LifecycleTests(unittest.TestCase):

    def setUp(self):
        self.server = StubGitHub()
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.env = Env(self)
        self.env.gl = GitHubBackend(REPO, "t", http=Http(self.server.base, {}, attempts=1))

    def labels(self, n=1):
        return set(self.server.issues[n]["labels"])

    def merge_pr(self, fingerprint, checks=None, evidence=True):
        self.server.timeline[1] = [{"event": "cross-referenced", "source": {"issue": {
            "number": 21, "pull_request": {"url": "x"}, "repository": {"full_name": REPO}}}}]
        self.server.prs[21] = {"state": "closed", "merged": True, "base": {"ref": DEV_BRANCH}, "head": {"sha": "d" * 40},
                               "merge_commit_sha": MERGE_SHA, "merged_at": "2026-10-20T10:00:00Z", "html_url": "u"}
        if evidence:
            doc = {"schema": RESOLUTION_SCHEMA, "fingerprint": fingerprint, "backend_issue": 1, "root_cause": "A",
                   "summary": "Adds the customers list.", "tests": ["tests/X.php"],
                   "checks": checks or [{"check": "operation_exists", "operation_id": "owner.sales.customers.index"}]}
            self.server.files[(f"docs/api-gap/resolutions/{fingerprint[:16]}.json", MERGE_SHA)] = json.dumps(doc).encode()

    def test_full_lifecycle_never_reports_resolved_before_publication_and_confirmation(self):
        env = self.env
        request = env.submit(1)
        fp = fp_of(request)
        env.run()
        self.assertEqual(len(self.server.issues), 1, "one backend issue")
        self.assertIn("gap::accepted", self.labels())
        self.assertIn("gap:accepted", env.gh.labels(1))

        env.run()
        self.assertEqual(len(self.server.issues), 1, "idempotent: rerun creates nothing")

        self.server.prs[21] = {"state": "open", "merged": False, "base": {"ref": DEV_BRANCH}, "head": {"sha": "d" * 40}}
        self.server.timeline[1] = [{"event": "cross-referenced", "source": {"issue": {
            "number": 21, "pull_request": {"url": "x"}, "repository": {"full_name": REPO}}}}]
        env.run()
        self.assertIn("gap:in-progress", env.gh.labels(1), "a draft/open PR is progress, not resolution")

        self.merge_pr(fp)
        env.run()
        self.assertEqual(env.gh.state_of(1)["reason"], "MERGED_NOT_PUBLISHED")
        self.assertNotIn("gap:contract-published", env.gh.labels(1))
        self.assertNotIn("gap:resolved", env.gh.labels(1))

        version, digest = env.publish_fix()
        env.run()
        self.assertIn("gap:contract-published", env.gh.labels(1))
        self.assertIn("gap::contract-published", self.labels())
        self.assertEqual(env.gh.state_of(1)["resolution"]["merge_request"], 21)

        payload = {"fingerprint": fp, "version": version, "sha256": digest, "tests_passed": True}
        env.gh.user_comment(1, "alice", f"<!-- {VERIFY_MARKER} {json.dumps(payload)} -->\nverified")
        env.run()
        self.assertIn("gap:consumer-verified", env.gh.labels(1), "backend issue still open: not resolved yet")
        self.assertNotIn("gap:resolved", env.gh.labels(1))

        self.server.issues[1]["state"] = "closed"
        env.run()
        self.assertIn("gap:resolved", env.gh.labels(1))
        self.assertIn("gap::resolved", self.labels())

    def test_a_merged_pull_request_without_evidence_fails_closed(self):
        env = self.env
        fp = fp_of(env.submit(1))
        env.run()
        self.merge_pr(fp, evidence=False)
        env.publish_fix()
        env.run()
        self.assertEqual(env.gh.state_of(1)["reason"], "RESOLUTION_EVIDENCE_MISSING")
        self.assertNotIn("gap:contract-published", env.gh.labels(1))

    def test_the_coordinator_never_writes_outside_the_issue_and_label_apis(self):
        env = self.env
        env.submit(1)
        env.run()
        writes = {(m, re.sub(r"\d+", "N", p.split(REPO + "/")[1])) for m, p in self.server.calls if m != "GET"}
        allowed = {("POST", "issues"), ("POST", "issues/N/labels"), ("POST", "issues/N/comments"),
                   ("DELETE", "issues/N/labels/gap%3A%3Aaccepted"), ("PATCH", "issues/N")}
        self.assertLessEqual(writes, allowed)
        self.assertFalse([c for c in self.server.calls if c[0] != "GET" and "pulls" in c[1]], "never touches pull requests")
        self.assertFalse([c for c in self.server.calls if c[0] != "GET" and "contents" in c[1]], "never writes content")


if __name__ == "__main__":
    unittest.main()
