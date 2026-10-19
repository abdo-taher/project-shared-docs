#!/usr/bin/env python3
"""Supervised polling worker that dispatches approved API gap issues.

  python3 scripts/gap/gap_worker.py run [--once] [--dry-run]    poll and dispatch until stopped
  python3 scripts/gap/gap_worker.py health [--max-age 300]      0 healthy · 1 stale/blocked · 2 not running
  python3 scripts/gap/gap_worker.py status                      print the status file

Why a worker. The coordinator runs as a GitHub Actions job, which has no coding agent and
must not start one. Backend implementation happens on a host that has the agent
runtime (the owner's machine), so something there has to notice approved issues.
This is that something: a long-running process meant to be supervised by the
same mechanism that already supervises the Capitalix agents (systemd user
units; see deploy/capitalix-gap-worker.service). It is NOT autonomous unless
that unit is installed and running; `health` says whether it is.

Safety properties:
  - one worker per state directory (flock); a second one exits 4;
  - restart recovery first: dispatches left STARTED by a dead process are failed visibly;
  - the agent runtime (sandboxed) is probed at start and after any failure; while it is
    blocked nothing is dispatched and `health` reports it;
  - only issues that pass the dispatcher's gates are dispatched (Maintainer approval, owner
    approval for sensitive gaps, no open review, not failed/in progress), one at a time,
    at most --max-per-hour, and not while the host is busy (--max-load): it must never
    starve the running Capitalix agent pipelines;
  - a failed dispatch is labelled and is not retried until a Maintainer clears it;
  - SIGTERM/SIGINT: an idle worker exits at once; a running dispatch is aborted, the agent
    container killed, and the issue marked failed with its workspace kept.

Credentials come from the environment (a systemd EnvironmentFile, mode 600):
API_GAP_DISPATCH_TOKEN, CAPITALIX_GAP_EXECUTOR_CMD, optionally
API_GAP_AGENT_CLAUDE_CODE_OAUTH_TOKEN. Nothing is read from CI.

Exit codes: 0 stopped cleanly; 3 configuration error; 4 another worker holds the lock.
"""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import signal
import socket
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import gap_core as core  # noqa: E402
from gap_coordinator import HERE, load_policy  # noqa: E402
from gap_dispatch import (Dispatcher, Refused, Shutdown, build_coordination, make_forge, probe,  # noqa: E402
                          sandbox_config)
from gap_http import ApiError  # noqa: E402
from gap_github_backend import GitHubBackend  # noqa: E402

STATUS_FILE = "worker-status.json"
LOCK_FILE = "worker.lock"


def sd_notify(message: str) -> None:
    """systemd readiness/watchdog notification; a no-op outside systemd."""
    target = os.environ.get("NOTIFY_SOCKET")
    if not target:
        return
    if target.startswith("@"):
        target = "\0" + target[1:]
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as sock:
            sock.connect(target)
            sock.sendall(message.encode())
    except OSError:
        pass


class Worker:
    def __init__(self, dispatcher: Dispatcher, state_dir: Path, *, template: str | None, sandbox_cfg: dict | None,
                 poll_interval: float = 60, probe_interval: float = 6 * 3600, probe_timeout: int = 180,
                 max_per_hour: int = 4, max_load: float = 6.0, dry_run: bool = False, clock=time.time,
                 sleep=time.sleep, loadavg=lambda: os.getloadavg()[0], log=print):
        self.d = dispatcher
        self.state_dir = state_dir
        self.template = template
        self.sandbox_cfg = sandbox_cfg
        self.poll_interval = poll_interval
        self.probe_interval = probe_interval
        self.probe_timeout = probe_timeout
        self.max_per_hour = max_per_hour
        self.max_load = max_load
        self.dry_run = dry_run
        self.clock = clock
        self.sleep = sleep
        self.loadavg = loadavg
        self.log = log
        self.stop = False
        self.dispatching = False
        self.dispatch_deadline = 0.0
        self.dispatched_at: list[float] = []
        self.runtime = {"status": "UNKNOWN", "detail": "", "checked_at": 0.0}
        self.status = {"pid": os.getpid(), "started_at": core.utc_now(), "state": "starting", "polls": 0,
                       "dispatched": 0, "failed": 0, "refused": 0, "current_issue": None, "last_error": None,
                       "last_poll_at": None, "runtime": None, "recovered": []}

    # -- status / health -----------------------------------------------------
    def write_status(self, **fields) -> None:
        self.status.update(fields)
        self.status["updated_at_epoch"] = self.clock()
        self.status["updated_at"] = core.utc_now()
        self.status["runtime"] = {"status": self.runtime["status"], "detail": self.runtime["detail"]}
        path = self.state_dir / STATUS_FILE
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.status, indent=1))
        os.replace(tmp, path)

    # -- signals ---------------------------------------------------------------
    def request_stop(self, signum, frame) -> None:
        self.stop = True
        self.write_status(state="stopping")
        if self.dispatching:
            raise Shutdown()

    # -- one polling cycle -------------------------------------------------------
    def check_runtime(self, force: bool = False) -> bool:
        now = self.clock()
        if not force and self.runtime["status"] == "RUNTIME_OK" and now - self.runtime["checked_at"] < self.probe_interval:
            return True
        if not force and self.runtime["status"] != "RUNTIME_OK" and now - self.runtime["checked_at"] < min(
                self.probe_interval, max(self.poll_interval * 5, 300)):
            return False  # blocked: re-probe at a calm cadence, not every poll
        status, detail = probe(self.template, self.probe_timeout, self.sandbox_cfg)
        self.runtime = {"status": status, "detail": detail, "checked_at": now}
        self.log(f"agent runtime: {status} — {detail}")
        return status == "RUNTIME_OK"

    def poll(self) -> str:
        """One cycle. Returns what happened: IDLE, DISPATCHED, FAILED, BLOCKED_RUNTIME, WAITING_LOAD, RATE_LIMITED, ERROR."""
        self.status["polls"] += 1
        self.write_status(last_poll_at=core.utc_now(), state="polling")
        try:
            candidates = [iid for iid, st in self.d.eligible() if st == "ELIGIBLE"]
        except ApiError as exc:
            self.write_status(state="error", last_error=str(exc)[:200])
            return "ERROR"
        if not candidates:
            self.write_status(state="idle")
            return "IDLE"
        if not self.check_runtime():
            self.write_status(state="blocked-runtime", last_error=self.runtime["detail"][:200])
            return "BLOCKED_RUNTIME"
        load = self.loadavg()
        if load > self.max_load:
            self.write_status(state="waiting-load", last_error=f"load average {load:.1f} > {self.max_load}")
            return "WAITING_LOAD"
        now = self.clock()
        self.dispatched_at = [t for t in self.dispatched_at if now - t < 3600]
        if len(self.dispatched_at) >= self.max_per_hour:
            self.write_status(state="rate-limited")
            return "RATE_LIMITED"
        iid = min(candidates)
        if self.dry_run:
            self.log(f"DRY-RUN would dispatch #{iid}")
            self.write_status(state="idle", current_issue=None)
            return "DRY_RUN"
        # a long agent run must not look hung: heartbeats are allowed until the run's own timeout expires
        self.dispatch_deadline = now + self.d.timeout + 120
        self.write_status(state="dispatching", current_issue=iid, dispatch_deadline_epoch=self.dispatch_deadline)
        sd_notify(f"STATUS=dispatching #{iid}")
        self.dispatching = True
        try:
            outcome = self.d.run(iid)
        except Refused as exc:
            self.status["failed"] += 1
            self.write_status(state="idle", current_issue=None, last_error=f"#{iid}: {str(exc)[:180]}")
            self.check_runtime(force=True)  # a failure may mean the runtime broke: say so promptly
            return "FAILED"
        except ApiError as exc:
            self.write_status(state="error", current_issue=None, last_error=f"#{iid}: {str(exc)[:180]}")
            return "ERROR"
        finally:
            self.dispatching = False
        self.dispatched_at.append(now)
        self.status["dispatched"] += 1
        self.write_status(state="idle", current_issue=None, last_error=None, last_result=outcome.get("status"))
        return "DISPATCHED"

    def _heartbeat(self) -> None:
        while not self.stop_heartbeat.wait(20):
            if self.dispatching and self.clock() < self.dispatch_deadline:
                sd_notify("WATCHDOG=1")

    # -- main loop -----------------------------------------------------------------
    def run(self, once: bool = False) -> int:
        self.stop_heartbeat = threading.Event()
        threading.Thread(target=self._heartbeat, daemon=True).start()
        signal.signal(signal.SIGTERM, self.request_stop)
        signal.signal(signal.SIGINT, self.request_stop)
        try:
            recovered = self.d.recover()
        except ApiError as exc:
            self.log(f"restart recovery could not reach GitHub: {exc}")
            recovered = []
        self.status["recovered"] = recovered
        if recovered:
            self.log(f"restart recovery settled interrupted dispatches: {recovered}")
        self.check_runtime(force=True)
        self.write_status(state="idle")
        sd_notify("READY=1")
        try:
            while not self.stop:
                try:
                    self.poll()
                except Exception as exc:  # keep supervising: report it, the next cycle retries
                    self.dispatching = False
                    self.write_status(state="error", current_issue=None,
                                      last_error=f"{type(exc).__name__}: {str(exc)[:160]}")
                sd_notify("WATCHDOG=1")
                if once:
                    break
                deadline = self.clock() + self.poll_interval
                while not self.stop and self.clock() < deadline:
                    self.sleep(min(1.0, self.poll_interval))
                    sd_notify("WATCHDOG=1")
        except Shutdown:
            self.log("stopped during a dispatch; the issue was marked failed and its workspace kept")
        finally:
            self.stop_heartbeat.set()
            self.write_status(state="stopped")
            sd_notify("STOPPING=1")
        return 0


def acquire_lock(state_dir: Path):
    state_dir.mkdir(parents=True, exist_ok=True)
    handle = open(state_dir / LOCK_FILE, "w")
    try:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        handle.close()
        return None
    handle.write(str(os.getpid()))
    handle.flush()
    return handle


def health(state_dir: Path, max_age: float, now=time.time, alive=lambda pid: Path(f"/proc/{pid}").exists()) -> tuple[int, str]:
    path = state_dir / STATUS_FILE
    if not path.exists():
        return 2, "not running: no status file"
    status = json.loads(path.read_text())
    if status.get("state") != "stopped" and not alive(status.get("pid", 0)):
        return 2, f"not running: process {status.get('pid')} is gone (last state {status.get('state')})"
    if status.get("state") == "stopped":
        return 2, "not running: stopped"
    age = now() - status.get("updated_at_epoch", 0)
    if status.get("state") == "dispatching" and now() < status.get("dispatch_deadline_epoch", 0):
        return 0, f"healthy: dispatching #{status.get('current_issue')} (within its time limit)"
    if age > max_age:
        return 1, f"stale: last update {age:.0f}s ago (state {status.get('state')})"
    if (status.get("runtime") or {}).get("status") != "RUNTIME_OK":
        return 1, f"agent runtime {status['runtime']['status']}: {status['runtime']['detail']}"
    if status.get("state") == "error":
        return 1, f"error: {status.get('last_error')}"
    return 0, f"healthy: {status['state']}, {status['dispatched']} dispatched, {status['failed']} failed"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Supervised API gap dispatch worker")
    parser.add_argument("--policy", default=str(HERE / "policy.json"))
    parser.add_argument("--workdir", default=str(Path.home() / ".capitalix-gap-work"))
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run")
    run.add_argument("--once", action="store_true")
    run.add_argument("--dry-run", action="store_true")
    run.add_argument("--poll-interval", type=float, default=60)
    run.add_argument("--max-per-hour", type=int, default=4)
    run.add_argument("--max-load", type=float, default=6.0)
    run.add_argument("--timeout", type=int, default=3600, help="seconds one agent run may take")
    run.add_argument("--no-sandbox", action="store_true")
    run.add_argument("--image")
    run.add_argument("--remote", default=os.environ.get("API_GAP_DEV_REMOTE"))
    run.add_argument("--base")
    run.add_argument("--forge", choices=("github", "bundle"))
    run.add_argument("--coordination-repo", help="development checkout whose coordinator state is read")
    h = sub.add_parser("health")
    h.add_argument("--max-age", type=float, default=300)
    sub.add_parser("status")
    args = parser.parse_args(argv)
    state_dir = Path(args.workdir) / "state"
    if args.command == "status":
        path = state_dir / STATUS_FILE
        print(path.read_text() if path.exists() else "no status file")
        return 0
    if args.command == "health":
        code, message = health(state_dir, args.max_age)
        print(message)
        return code
    try:
        policy = load_policy(Path(args.policy))
    except (OSError, ValueError) as exc:
        print(f"ERROR: policy: {exc}", file=sys.stderr)
        return 3
    token = os.environ.get("API_GAP_DISPATCH_TOKEN")
    template = os.environ.get("CAPITALIX_GAP_EXECUTOR_CMD") or None
    if not token or not template:
        print("ERROR: API_GAP_DISPATCH_TOKEN and CAPITALIX_GAP_EXECUTOR_CMD are required", file=sys.stderr)
        return 3
    lock = acquire_lock(state_dir)
    if lock is None:
        print("another worker holds the lock; nothing done", file=sys.stderr)
        return 4
    backend = GitHubBackend(os.environ.get("API_GAP_BACKEND_REPOSITORY", policy["backend_repository"]), token)
    cfg = sandbox_config(policy, args)
    dev = {**(policy.get("development") or {}), **({"forge": args.forge} if args.forge else {})}
    try:
        forge = make_forge(dev, Path(args.workdir))
    except Refused as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 3
    dispatcher = Dispatcher(policy, backend, workdir=Path(args.workdir), template=template, timeout=args.timeout,
                            forge=forge, remote=args.remote, base_branch=args.base, sandbox_cfg=cfg,
                            state_dir=state_dir, coordination=build_coordination(policy, args.coordination_repo),
                            log=lambda m: print(m, file=sys.stderr))
    worker = Worker(dispatcher, state_dir, template=template, sandbox_cfg=cfg, poll_interval=args.poll_interval,
                    max_per_hour=args.max_per_hour, max_load=args.max_load, dry_run=args.dry_run,
                    log=lambda m: print(m, file=sys.stderr))
    return worker.run(once=args.once)


if __name__ == "__main__":
    sys.exit(main())
