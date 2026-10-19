"""Transport behavior against a real local HTTP server (no network)."""

import json
import sys
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gap_http import ApiError, Http  # noqa: E402
from gap_platforms import GitHub  # noqa: E402

TOKEN = "glpat-SECRET-do-not-leak-0000"


class Server(ThreadingHTTPServer):
    def __init__(self):
        super().__init__(("127.0.0.1", 0), Handler)
        self.script: dict[str, list] = {}
        self.seen: list = []

    def handle_error(self, request, client_address):
        pass  # clients that time out on purpose close the socket early


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _reply(self):
        server = self.server
        server.seen.append((self.command, self.path, {k.lower(): v for k, v in self.headers.items()}))
        steps = server.script.get(self.path.split("?")[0], [])
        step = steps.pop(0) if len(steps) > 1 else (steps[0] if steps else (200, {}, []))
        status, headers, body = step
        if status == "sleep":
            time.sleep(headers)
            status, headers, body = 200, {}, []
        payload = json.dumps(body).encode()
        self.send_response(status)
        for k, v in headers.items():
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = _reply


class HttpTests(unittest.TestCase):

    def setUp(self):
        self.server = Server()
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.shutdown)
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"
        self.sleeps = []
        self.http = Http(self.base, {"PRIVATE-TOKEN": TOKEN}, timeout=0.5, attempts=3,
                         sleep=self.sleeps.append)

    def script(self, path, *steps):
        self.server.script[path] = list(steps)

    def test_client_errors_fail_at_once_without_leaking_the_token(self):
        for status, words in ((401, "unauthorized"), (403, "forbidden"), (404, "not found")):
            self.script("/x", (status, {}, {"message": TOKEN}))
            with self.assertRaises(ApiError) as ctx:
                self.http.get("x", private_token=TOKEN)
            self.assertEqual(ctx.exception.status, status)
            self.assertIn(words, str(ctx.exception))
            self.assertNotIn(TOKEN, str(ctx.exception))
            self.assertFalse(ctx.exception.transient)
        self.assertEqual(self.sleeps, [])

    def test_429_honours_retry_after(self):
        self.script("/x", (429, {"Retry-After": "7"}, {}), (200, {}, {"ok": 1}))
        self.assertEqual(self.http.get("x"), {"ok": 1})
        self.assertEqual(self.sleeps, [7.0])

    def test_rate_limit_403_is_retried_with_backoff(self):
        self.script("/x", (403, {"X-RateLimit-Remaining": "0"}, {}), (403, {"RateLimit-Remaining": "0"}, {}),
                    (200, {}, {"ok": 2}))
        self.assertEqual(self.http.get("x"), {"ok": 2})
        self.assertEqual(self.sleeps, [1.0, 2.0])

    def test_5xx_recovers(self):
        self.script("/x", (502, {}, {}), (200, {}, {"ok": 3}))
        self.assertEqual(self.http.get("x"), {"ok": 3})

    def test_5xx_permanent_is_transient_error(self):
        self.script("/x", (503, {}, {}))
        with self.assertRaises(ApiError) as ctx:
            self.http.get("x")
        self.assertTrue(ctx.exception.transient)
        self.assertEqual(len(self.sleeps), 2, "bounded retries")

    def test_timeout_retry_then_success(self):
        self.script("/x", ("sleep", 1.0, None), (200, {}, {"ok": 4}))
        self.assertEqual(self.http.get("x"), {"ok": 4})

    def test_timeouts_exhausted(self):
        self.script("/x", ("sleep", 1.0, None))
        with self.assertRaises(ApiError) as ctx:
            self.http.get("x")
        self.assertIn("timed out", str(ctx.exception))

    def test_backoff_is_capped(self):
        self.http.max_wait = 5
        self.script("/x", (429, {"Retry-After": "3600"}, {}), (200, {}, {}))
        self.http.get("x")
        self.assertEqual(self.sleeps, [5])

    def test_github_link_pagination(self):
        self.script("/list", (200, {"Link": f'<{self.base}/list2>; rel="next"'}, [1, 2]))
        self.script("/list2", (200, {}, [3]))
        self.assertEqual(self.http.paginate("list"), [1, 2, 3])

    def test_x_next_page_pagination(self):
        self.script("/list", (200, {"X-Next-Page": "2"}, [1]), (200, {}, [2]))
        self.assertEqual(self.http.paginate("list"), [1, 2])

    def test_pagination_never_sends_credentials_to_another_host(self):
        self.script("/list", (200, {"Link": '<https://evil.example/steal>; rel="next"'}, [1]))
        with self.assertRaises(ApiError):
            self.http.paginate("list")

    def test_adapters_send_credentials_only_as_headers(self):
        self.script("/repos/a/b/issues", (200, {}, []))
        GitHub("a/b", TOKEN, http=Http(self.base, {}, sleep=self.sleeps.append)).open_issues()
        method, path, headers = self.server.seen[-1]
        self.assertNotIn(TOKEN, path)
        self.assertEqual(headers.get("authorization"), f"Bearer {TOKEN}")

    def test_github_permission_maps_missing_access_to_none(self):
        self.script("/repos/o/r/collaborators/stranger/permission", (404, {}, {}))
        github = GitHub("o/r", "t", http=Http(self.base, {}, sleep=self.sleeps.append))
        self.assertEqual(github.permission("stranger"), "none")


if __name__ == "__main__":
    unittest.main()
