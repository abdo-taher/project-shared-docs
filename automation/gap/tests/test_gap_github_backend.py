import json
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gap_github_backend import GitHubBackend  # noqa: E402
from gap_http import Http  # noqa: E402

REPO = "abdo-taher/capitalix"


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _serve(self, method):
        length = int(self.headers.get("Content-Length") or 0)
        body = json.loads(self.rfile.read(length)) if length else None
        path = self.path.split("?")[0].lstrip("/")
        self.server.seen.append((method, path, body, dict(self.headers)))
        status, payload = self.server.routes.get((method, path), (404, {}))
        raw = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    do_GET = lambda self: self._serve("GET")
    do_POST = lambda self: self._serve("POST")
    do_PATCH = lambda self: self._serve("PATCH")
    do_DELETE = lambda self: self._serve("DELETE")


class BackendTests(unittest.TestCase):

    def backend(self, routes):
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        server.routes, server.seen = routes, []
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.shutdown)
        self.server = server
        return GitHubBackend(REPO, "t", http=Http(f"http://127.0.0.1:{server.server_address[1]}", {}, attempts=1))

    def issue(self, number, body="", labels=(), state="open", pr=False):
        raw = {"number": number, "title": f"t{number}", "body": body, "state": state, "html_url": f"u/{number}",
               "labels": [{"name": l} for l in labels], "created_at": "2026-10-19T00:00:00Z", "user": {"login": "x"}}
        if pr:
            raw["pull_request"] = {}
        return raw

    def test_issues_are_normalized_and_pull_requests_excluded(self):
        be = self.backend({("GET", f"repos/{REPO}/issues"): (200, [self.issue(3, "b", ["api-gap"]),
                                                                    self.issue(4, pr=True)])})
        issues = be.gap_issues()
        self.assertEqual([(i["iid"], i["state"], i["labels"], i["description"]) for i in issues],
                         [(3, "opened", ["api-gap"], "b")])

    def test_find_by_fingerprint_matches_the_marker_and_orders_oldest_first(self):
        fp = "a" * 64
        marker = f"<!-- capitalix-gap fingerprint={fp} -->"
        be = self.backend({("GET", f"repos/{REPO}/issues"): (200, [
            self.issue(9, marker), self.issue(2, marker, state="closed"), self.issue(5, "other")])})
        self.assertEqual([i["iid"] for i in be.find_by_fingerprint(fp)], [2, 9])

    def test_update_issue_adds_removes_and_closes(self):
        be = self.backend({("DELETE", f"repos/{REPO}/issues/7/labels/gap%3A%3Aaccepted"): (200, []),
                           ("POST", f"repos/{REPO}/issues/7/labels"): (200, []),
                           ("PATCH", f"repos/{REPO}/issues/7"): (200, self.issue(7, state="closed")),
                           ("GET", f"repos/{REPO}/issues/7"): (200, self.issue(7, state="closed"))})
        result = be.update_issue(7, add_labels="gap::blocked", remove_labels="gap::accepted", state_event="close")
        seen = [(m, p) for m, p, _, _ in self.server.seen]
        self.assertIn(("POST", f"repos/{REPO}/issues/7/labels"), seen)
        self.assertEqual(result["state"], "closed")
        close = next(b for m, p, b, _ in self.server.seen if m == "PATCH")
        self.assertEqual(close["state"], "closed")

    def test_removing_a_label_that_is_not_there_is_not_an_error(self):
        be = self.backend({("POST", f"repos/{REPO}/issues/7/labels"): (200, []),
                           ("GET", f"repos/{REPO}/issues/7"): (200, self.issue(7))})
        be.update_issue(7, add_labels="gap::accepted", remove_labels="gap::blocked")

    def test_label_events_and_access_levels_come_from_github_identities(self):
        events = [{"event": "labeled", "label": {"name": "gap-dispatch::approved"}, "actor": {"id": 11, "login": "w"}},
                  {"event": "assigned"},
                  {"event": "unlabeled", "label": {"name": "x"}, "actor": {"id": 12, "login": "r"}}]
        be = self.backend({("GET", f"repos/{REPO}/issues/7/events"): (200, events),
                           ("GET", f"repos/{REPO}/collaborators/w/permission"): (200, {"role_name": "write"}),
                           ("GET", f"repos/{REPO}/collaborators/r/permission"): (404, {}),
                           ("GET", "user/13"): (200, {"login": "m"}),
                           ("GET", f"repos/{REPO}/collaborators/m/permission"): (200, {"role_name": "maintain"})})
        normalized = be.label_events(7)
        self.assertEqual(normalized[0], {"action": "add", "label": {"name": "gap-dispatch::approved"},
                                         "user": {"id": 11, "username": "w"}})
        self.assertEqual(normalized[1]["action"], "remove")
        self.assertEqual((be.access_level(11), be.access_level(12), be.access_level(13)), (30, 0, 40))
        self.assertEqual(be.access_level(11), 30)
        self.assertEqual(sum(1 for m, p, *_ in self.server.seen if p.endswith("w/permission")), 1, "cached")

    def test_related_pull_requests_are_normalized_from_the_timeline(self):
        timeline = [{"event": "cross-referenced", "source": {"issue": {"number": 21, "pull_request": {},
                                                                         "repository": {"full_name": REPO}}}},
                    {"event": "cross-referenced", "source": {"issue": {"number": 22, "pull_request": {},
                                                                         "repository": {"full_name": "other/repo"}}}},
                    {"event": "cross-referenced", "source": {"issue": {"number": 23, "repository": {"full_name": REPO}}}},
                    {"event": "labeled"}]
        pr = {"state": "closed", "merged": True, "base": {"ref": "integration/E01-FOUNDATION-SAAS"},
              "head": {"sha": "h" * 40}, "merge_commit_sha": "m" * 40, "merged_at": "2026-10-20T00:00:00Z",
              "html_url": "u", "draft": False}
        be = self.backend({("GET", f"repos/{REPO}/issues/7/timeline"): (200, timeline),
                           ("GET", f"repos/{REPO}/pulls/21"): (200, pr)})
        related = be.related_merge_requests(7)
        self.assertEqual([(r["iid"], r["state"], r["target_branch"], r["merge_commit_sha"]) for r in related],
                         [(21, "merged", "integration/E01-FOUNDATION-SAAS", "m" * 40)])

    def test_open_and_closed_unmerged_pull_requests(self):
        be = self.backend({("GET", f"repos/{REPO}/issues/7/timeline"): (200, [
            {"event": "cross-referenced", "source": {"issue": {"number": 1, "pull_request": {}}}},
            {"event": "cross-referenced", "source": {"issue": {"number": 2, "pull_request": {}}}}]),
            ("GET", f"repos/{REPO}/pulls/1"): (200, {"state": "open", "merged": False, "base": {"ref": "b"}, "head": {}}),
            ("GET", f"repos/{REPO}/pulls/2"): (200, {"state": "closed", "merged": False, "base": {"ref": "b"}, "head": {}})})
        self.assertEqual([r["state"] for r in be.related_merge_requests(7)], ["opened", "closed"])

    def test_file_at_reads_raw_content_at_a_commit_and_maps_404_to_none(self):
        be = self.backend({("GET", f"repos/{REPO}/contents/docs/api-gap/resolutions/a.json"): (200, b'{"x":1}')})
        self.assertEqual(be.file_at("docs/api-gap/resolutions/a.json", "c" * 40), b'{"x":1}')
        accept = [h["Accept"] for _, _, _, h in self.server.seen][0]
        self.assertIn("raw", accept)
        self.assertIsNone(be.file_at("docs/missing.json", "c" * 40))

    def test_is_ancestor_uses_the_compare_api_and_fails_closed(self):
        be = self.backend({("GET", f"repos/{REPO}/compare/aaa...bbb"): (200, {"status": "ahead"}),
                           ("GET", f"repos/{REPO}/compare/ccc...bbb"): (200, {"status": "diverged"}),
                           ("GET", f"repos/{REPO}/compare/ddd...bbb"): (200, {"status": "behind"})})
        self.assertTrue(be.is_ancestor("aaa", "bbb"))
        self.assertTrue(be.is_ancestor("x", "x"))
        self.assertFalse(be.is_ancestor("ccc", "bbb"))
        self.assertFalse(be.is_ancestor("ddd", "bbb"))
        self.assertFalse(be.is_ancestor("zzz", "bbb"), "unknown commit (404) is not an ancestor")

    def test_create_issue_sends_labels_and_body_and_returns_normalized(self):
        be = self.backend({("POST", f"repos/{REPO}/issues"): (201, self.issue(8, "desc", ["api-gap"]))})
        created = be.create_issue("T", "desc", ["api-gap", "gap::accepted"])
        self.assertEqual(created["iid"], 8)
        sent = self.server.seen[0][2]
        self.assertEqual(sent, {"title": "T", "body": "desc", "labels": ["api-gap", "gap::accepted"]})

    def test_ensure_labels_creates_only_the_missing_ones(self):
        be = self.backend({("GET", f"repos/{REPO}/labels"): (200, [{"name": "api-gap"}]),
                           ("POST", f"repos/{REPO}/labels"): (201, {})})
        be.ensure_labels()
        created = [b["name"] for m, p, b, _ in self.server.seen if m == "POST"]
        self.assertNotIn("api-gap", created)
        self.assertIn("gap::resolved", created)


if __name__ == "__main__":
    unittest.main()
