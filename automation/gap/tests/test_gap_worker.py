import json
import os
import signal
import subprocess
import sys
import time
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import gap_core as core  # noqa: E402
from fakes import gap_request  # noqa: E402
from gap_coordinator import Coordinator, Intake  # noqa: E402
from gap_worker import Worker, acquire_lock, health  # noqa: E402
from test_gap_dispatch import DispatchBase, MAINTAINER, POLICY, V, D  # noqa: E402


class Clock:
    def __init__(self):
        self.now = 1_000_000.0

    def __call__(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds


class WorkerTests(DispatchBase):

    def worker(self, **kwargs) -> Worker:
        self.clock = Clock()
        dispatcher = self.dispatcher()
        return Worker(dispatcher, self.tmp / "work/state", template=self.template, sandbox_cfg=None,
                      probe_timeout=30, clock=self.clock, sleep=self.clock.sleep, loadavg=lambda: 0.5,
                      log=lambda m: None, **kwargs)

    def add_second_issue(self, iid=2, **overrides):
        request = gap_request(V, D, location="orders.list", capability_id="CAP-OWN-181", **overrides)
        coordinator = Coordinator({**POLICY, "coordinator_github_login": "bot"}, None, self.gl, None)
        intake = Intake(number=2, author="alice", request=request, fingerprint=core.fingerprint(request))
        self.gl.create_issue(coordinator.backend_title(intake), coordinator.backend_description(intake),
                             ["api-gap", "gap::accepted"])
        self.gl.add_label_by(iid, "gap-dispatch::approved", MAINTAINER)

    def test_idle_when_nothing_is_approved(self):
        w = self.worker()
        w.check_runtime(force=True)
        self.assertEqual(w.poll(), "IDLE")
        self.assertEqual(self.gl.writes, 1)  # only the issue created in setUp; the worker wrote nothing
        self.assertEqual(w.status["state"], "idle")

    def test_dispatches_the_oldest_approved_issue_once(self):
        self.approve()
        self.add_second_issue()
        w = self.worker()
        w.check_runtime(force=True)
        self.assertEqual(w.poll(), "DISPATCHED")
        self.assertEqual(self.forge.opened[0]["branch"].split("-")[0], "gap/1")
        self.assertEqual(w.poll(), "DISPATCHED")  # now issue 2
        self.assertEqual(len(self.forge.opened), 2)
        self.assertEqual(w.poll(), "IDLE")
        self.assertEqual(len(self.forge.opened), 2, "no duplicate execution")

    def test_rate_limit(self):
        self.approve()
        self.add_second_issue()
        w = self.worker(max_per_hour=1)
        w.check_runtime(force=True)
        self.assertEqual(w.poll(), "DISPATCHED")
        self.assertEqual(w.poll(), "RATE_LIMITED")
        self.clock.now += 3601
        self.assertEqual(w.poll(), "DISPATCHED")

    def test_does_not_start_agents_while_the_host_is_busy(self):
        self.approve()
        w = self.worker(max_load=2.0)
        w.loadavg = lambda: 9.0
        w.check_runtime(force=True)
        self.assertEqual(w.poll(), "WAITING_LOAD")
        self.assertEqual(self.forge.opened, [])
        w.loadavg = lambda: 1.0
        self.assertEqual(w.poll(), "DISPATCHED")

    def test_blocked_runtime_blocks_dispatch_and_is_reported(self):
        self.approve()
        w = self.worker()
        w.template = None
        w.check_runtime(force=True)
        self.assertEqual(w.runtime["status"], "BLOCKED_AGENT_RUNTIME")
        self.assertEqual(w.poll(), "BLOCKED_RUNTIME")
        self.assertEqual(self.forge.opened, [])
        self.assertEqual(health(self.tmp / "work/state", 300, now=self.clock, alive=lambda p: True)[0], 1)

    def test_failed_dispatch_is_not_retried_in_a_loop(self):
        self.approve()
        self.mode.write_text("fail")
        w = self.worker()
        w.check_runtime(force=True)
        self.assertEqual(w.poll(), "FAILED")
        self.assertEqual(w.poll(), "IDLE", "the failed label keeps it out until a maintainer clears it")
        self.assertEqual(w.poll(), "IDLE")
        self.assertEqual(w.status["failed"], 1)
        self.assertIn("exited 9", w.status["last_error"])

    def test_sensitive_issue_is_not_dispatched_without_the_owner(self):
        sensitive = gap_request(V, D, capability_id="CAP-PAY-001", location="payroll.list")
        self.gl.issues[1]["description"] = self.gl.issues[1]["description"].replace(
            json.dumps(self.request, indent=2, ensure_ascii=False), json.dumps(sensitive, indent=2, ensure_ascii=False)
        ).replace(self.fp, core.fingerprint(sensitive))
        self.approve()
        w = self.worker()
        w.check_runtime(force=True)
        self.assertEqual(w.poll(), "IDLE")
        self.gl.add_label_by(1, "gap-owner::approved", 9, username="abdo-taher")
        self.assertEqual(w.poll(), "DISPATCHED")

    def test_gitlab_outage_is_reported_and_the_worker_keeps_running(self):
        self.approve()
        w = self.worker()
        w.check_runtime(force=True)
        self.gl.fail["related_merge_requests"] = [__import__("fakes").api_error(503, transient=True)]
        self.assertEqual(w.poll(), "ERROR")
        self.assertEqual(w.status["state"], "error")
        self.assertEqual(w.poll(), "DISPATCHED")

    def test_start_up_recovers_interrupted_dispatches_before_polling(self):
        self.approve()
        d = self.dispatcher()
        self.gl.update_issue(1, add_labels="gap::in-progress", remove_labels="gap::accepted")
        d._write_record(1, status="STARTED", pid=999999, worktree="/x", branch="b")
        w = self.worker()
        w.run(once=True)
        self.assertEqual(w.status["recovered"], [1])
        self.assertIn("gap-dispatch::failed", self.gl.issues[1]["labels"])
        self.assertEqual(w.status["state"], "stopped")

    def test_single_instance_lock(self):
        state = self.tmp / "lockstate"
        first = acquire_lock(state)
        self.assertIsNotNone(first)
        self.assertIsNone(acquire_lock(state))
        first.close()
        self.assertIsNotNone(acquire_lock(state))

    def test_health_states(self):
        state = self.tmp / "work/state"
        w = self.worker()
        w.check_runtime(force=True)
        w.write_status(state="idle")
        self.assertEqual(health(state, 300, now=self.clock, alive=lambda p: True)[0], 0)
        self.clock.now += 1000
        code, message = health(state, 300, now=self.clock, alive=lambda p: True)
        self.assertEqual((code, "stale" in message), (1, True))
        self.assertEqual(health(state, 300, now=self.clock, alive=lambda p: False)[0], 2)
        w.write_status(state="dispatching", current_issue=1, dispatch_deadline_epoch=self.clock.now + 600)
        self.clock.now += 400  # older than max-age, but still inside the run's time limit
        self.assertEqual(health(state, 300, now=self.clock, alive=lambda p: True)[0], 0, "long runs are not 'stale'")
        self.clock.now += 400  # past the limit: a hung dispatch is reported
        self.assertEqual(health(state, 300, now=self.clock, alive=lambda p: True)[0], 1, "but only within their limit")
        self.assertEqual(health(self.tmp / "nothing", 300)[0], 2)


class WorkerProcessTests(unittest.TestCase):
    """The real worker process: signals, lock, status file (no network: gitlab is a local stub server)."""

    def test_sigterm_stops_an_idle_worker_cleanly_and_a_second_instance_is_refused(self):
        import tempfile, threading
        from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

        class Stub(BaseHTTPRequestHandler):
            def log_message(self, *a): pass
            def do_GET(self):
                body = b"[]"
                self.send_response(200); self.send_header("Content-Length", "2"); self.end_headers(); self.wfile.write(body)

        server = ThreadingHTTPServer(("127.0.0.1", 0), Stub)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.shutdown)
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        work = Path(tmp.name) / "work"
        runner = Path(tmp.name) / "agent.py"
        runner.write_text("import re,sys\nm=re.search(r'GAP-PROBE-[0-9a-f]+', sys.stdin.read())\nprint(m.group(0) if m else '')\n")
        policy = json.loads((HERE.parent / "policy.json").read_text())
        policy_path = Path(tmp.name) / "policy.json"
        policy_path.write_text(json.dumps(policy))
        env = {"PATH": os.environ["PATH"], "HOME": tmp.name, "API_GAP_DISPATCH_TOKEN": "t",
               "CAPITALIX_GAP_EXECUTOR_CMD": f"{sys.executable} {runner}",
               "API_GAP_DEV_REMOTE": str(Path(tmp.name) / "none.git")}
        base = [sys.executable, str(HERE.parent / "gap_worker.py"), "--policy", str(policy_path), "--workdir", str(work)]
        # point the GitLab client at the stub by patching the base URL through a tiny wrapper script
        wrapper = Path(tmp.name) / "run.py"
        wrapper.write_text(f"import sys, runpy\nsys.path.insert(0, {str(HERE.parent)!r})\n"
                           f"import gap_platforms\n"
                           f"orig = gap_platforms.GitLab.__init__\n"
                           f"gap_platforms.GitLab.__init__ = lambda self, project, token, http=None, base='http://127.0.0.1:{server.server_address[1]}': orig(self, project, token, http, base)\n"
                           f"sys.argv = ['gap_worker.py'] + sys.argv[1:]\n"
                           f"runpy.run_path({str(HERE.parent / 'gap_worker.py')!r}, run_name='__main__')\n")
        cmd = [sys.executable, str(wrapper), "--policy", str(policy_path), "--workdir", str(work), "run",
               "--no-sandbox", "--poll-interval", "1"]
        first = subprocess.Popen(cmd, env=env, stderr=subprocess.PIPE, text=True)
        self.addCleanup(lambda: first.poll() is None and first.kill())
        state = work / "state"
        for _ in range(100):
            if (state / "worker-status.json").exists() and json.loads((state / "worker-status.json").read_text()).get("state") in ("idle", "polling"):
                break
            time.sleep(0.1)
        second = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=30)
        self.assertEqual(second.returncode, 4, second.stderr)
        self.assertEqual(health(state, 30)[0], 0, health(state, 30))
        first.send_signal(signal.SIGTERM)
        self.assertEqual(first.wait(timeout=20), 0)
        self.assertEqual(json.loads((state / "worker-status.json").read_text())["state"], "stopped")
        self.assertEqual(health(state, 30)[0], 2)


if __name__ == "__main__":
    unittest.main()
