"""Safe reservation and conflict detection against the Capitalix agent coordinator.

Why an adapter. The coordinator (`scripts/agent-wave-coordinator.py` in the development repository) owns
exclusive task claims and write-set reservations, but it only knows the registry's capability tasks
(`docs/final/AGENT_WAVE_TASK_REGISTRY.json`, which executors must not edit), so a gap fix cannot be claimed as a
task. Rather than write into its state (forbidden: "do not edit coordination state manually"), this module:

  1. READS the live coordination state and registry (never writes, never takes its lock, never runs a mutating
     subcommand) and mirrors its conflict rules: a task blocks others in the same default conflict root while its
     status is CLAIMED / IN_PROGRESS / HANDOFF_READY / BLOCKED / READY_FOR_REVIEW and its write set is not
     released; a declared write set blocks exact/prefix overlaps except the shared wiring paths the coordinator
     itself lets tasks share.
  2. Refuses to start a gap whose module root overlaps an active reservation (before any clone or agent).
  3. Holds its own lease per module root (`leases.json`, flock, TTL, owner pid) so two gap dispatches never work
     on the same module, and abandoned leases are reaped after a crash.
  4. After the agent finishes, refuses a diff that touches a path another active task has reserved.
  5. Checks that the gap workspace and branch collide with no coordinator worktree or branch.

Fail closed: if the coordination state cannot be read, a dispatch that requires coordination is refused.
Draft pull requests are the only output, so merge sequencing with the coordinator stays with the owner.
"""

from __future__ import annotations

import fcntl
import json
import os
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

ACTIVE_STATUSES = {"CLAIMED", "IN_PROGRESS", "HANDOFF_READY", "BLOCKED", "READY_FOR_REVIEW"}
# The hotfix lane (`capitalix-agent hotfix`, state in <checkout>/.state/hotfix/requests/HF-*.json) is a second source of
# live work. Its own terminal states (capitalix_agent/hotfix/model.py: TERMINAL) free everything; every other state,
# including BLOCKED, still owns a branch and a worktree.
HOTFIX_TERMINAL = {"COMPLETED", "FAILED", "CANCELLED"}
HOTFIX_DIR = ".state/hotfix/requests"
STATE_DIR_NAME = "capitalix-agent-coordination"
REGISTRY = "docs/final/AGENT_WAVE_TASK_REGISTRY.json"
# Mirrors DEFAULT_SHARED_WIRING_PATHS / GATE_GENERATED_PATHS of the coordinator (overlap there is by design).
SHARED_PATHS = ("bootstrap/providers.php", "bootstrap/app.php", "config/route-attributes.php", "routes/api.php",
                "routes/web.php", "routes/console.php", "tests/Feature/ApiContract/Owner/ledger.json",
                "tests/Feature/ApiContract/Owner/COVERAGE.md", "docs/architecture/access/ROUTE_ACCESS_INVENTORY.md",
                "docs/api/openapi.json")


class CoordinationUnavailable(Exception):
    """The coordination state could not be read."""


class CoordinationConflict(Exception):
    def __init__(self, message: str, conflicts: list[dict] | None = None):
        super().__init__(message)
        self.conflicts = conflicts or []


def path_overlap(a: str, b: str) -> bool:
    """Same rule as the coordinator's path_overlap (exact, or one is a directory prefix of the other)."""
    def shape(x: str) -> tuple[str, bool]:
        x = x.rstrip()
        wildcard = x.endswith("/**") or x.endswith("/")
        if x.endswith("/**"):
            x = x[:-3]
        return x.rstrip("/"), wildcard
    aa, adir = shape(a)
    bb, bdir = shape(b)
    return aa == bb or (adir and bb.startswith(aa + "/")) or (bdir and aa.startswith(bb + "/"))


def roots_overlap(a: str, b: str) -> bool:
    a, b = a.rstrip("/"), b.rstrip("/")
    return a == b or a.startswith(b + "/") or b.startswith(a + "/")


@dataclass
class Reservation:
    task: str
    status: str
    agent: str | None
    root: str
    write_set: list[str]
    branch: str | None
    worktree: str | None
    lease_until: str | None
    lease_expired: bool = False
    undeclared: bool = False        # active but declares no paths: its footprint is unknown


@dataclass
class Footprint:
    roots: list[str]
    sources: list[str] = field(default_factory=list)


def _parse(ts: str | None):
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


class Coordination:
    """Read-only view of the coordinator's live state for the repository at `repo`."""

    def __init__(self, repo: Path, *, now=lambda: datetime.now(timezone.utc), shared_paths=SHARED_PATHS):
        self.repo = Path(repo).expanduser()
        self.now = now
        self.shared = set(shared_paths)

    def _common_dir(self) -> Path:
        result = subprocess.run(["git", "-C", str(self.repo), "rev-parse", "--git-common-dir"],
                                capture_output=True, text=True)
        if result.returncode != 0 or not result.stdout.strip():
            raise CoordinationUnavailable(f"{self.repo} is not a git repository")
        path = Path(result.stdout.strip())
        return path if path.is_absolute() else (self.repo / path).resolve()

    def state_path(self) -> Path:
        explicit = os.environ.get("CAPITALIX_COORDINATION_DIR")
        base = Path(explicit).expanduser() if explicit else self._common_dir() / STATE_DIR_NAME
        return base / "state.json"

    def _load(self, path: Path, what: str) -> dict:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise CoordinationUnavailable(f"cannot read the coordinator's {what} ({type(exc).__name__})") from None
        if not isinstance(data, dict):
            raise CoordinationUnavailable(f"the coordinator's {what} is malformed")
        return data

    def state(self) -> dict:
        state = self._load(self.state_path(), "state")
        if not isinstance(state.get("tasks"), dict):
            raise CoordinationUnavailable("the coordinator's state has no task table")
        return state

    def registry(self) -> dict[str, dict]:
        data = self._load(self.repo / REGISTRY, "registry")
        tasks = data.get("tasks", data)
        items = tasks if isinstance(tasks, list) else list(tasks.values())
        extra = ((data.get("rules") or {}).get("shared_wiring_paths")) or []
        self.shared |= {str(p).strip().strip("/") for p in extra}
        return {t["task_id"]: t for t in items if isinstance(t, dict) and "task_id" in t}

    def hotfix_reservations(self) -> list[Reservation]:
        """Active hotfix-lane requests as reservations (read-only; unreadable request files fail closed)."""
        directory = self.repo / HOTFIX_DIR
        if not directory.is_dir():
            return []
        out = []
        for path in sorted(directory.glob("HF-*.json")):
            request = self._load(path, f"hotfix request {path.name}")
            state = request.get("state")
            if not isinstance(state, str):
                raise CoordinationUnavailable(f"hotfix request {path.name} has no state")
            if state in HOTFIX_TERMINAL:
                continue
            hints = [str(h).strip("/") for h in (request.get("paths_hint") or []) if str(h).strip("/")]
            changed = [str(c) for c in (request.get("changed_files") or [])]
            declared = [h + "/**" for h in hints] + changed
            out.append(Reservation(
                task=f"hotfix:{request.get('id', path.stem)}", status=state, agent="hotfix-lane", root="",
                write_set=declared, branch=request.get("branch"), worktree=request.get("worktree"),
                lease_until=(request.get("lease") or {}).get("at"),
                # a running hotfix that declares nothing could be touching anything; a BLOCKED one is idle
                undeclared=not declared and state != "BLOCKED"))
        return out

    def reservations(self) -> list[Reservation]:
        return self.coordinator_reservations() + self.hotfix_reservations()

    def coordinator_reservations(self) -> list[Reservation]:
        state, registry = self.state(), self.registry()
        out = []
        for task_id, ts in state["tasks"].items():
            if ts.get("status") not in ACTIVE_STATUSES or ts.get("write_set_released"):
                continue
            until = _parse(ts.get("lease_until"))
            out.append(Reservation(
                task=task_id, status=ts["status"], agent=ts.get("agent") or ts.get("previous_agent"),
                root=(registry.get(task_id) or {}).get("default_conflict_key", ""),
                write_set=list(ts.get("write_set") or []), branch=ts.get("branch"), worktree=ts.get("worktree"),
                lease_until=ts.get("lease_until"), lease_expired=bool(until and until < self.now())))
        return out

    # -- footprint -----------------------------------------------------------
    def footprint(self, request: dict, policy: dict, explicit_roots: list[str]) -> Footprint:
        cfg = policy.get("coordination") or {}
        roots, sources = [], []
        capability = request.get("capability_id")
        if capability:
            entry = self.registry().get(capability)
            if entry and entry.get("default_conflict_key"):
                roots.append(entry["default_conflict_key"])
                sources.append(f"capability {capability}")
        # The consumer's capability id is a weak signal (it may be registered under a different module than the
        # one that serves the API), so the actor namespace and the operation namespace always widen the footprint.
        for actor, mapped in (cfg.get("actor_roots") or {}).items():
            if request.get("actor") == actor:
                roots += mapped
                sources.append(f"actor {actor}")
        operation_id = (request.get("operation") or {}).get("operation_id") or ""
        for prefix, mapped in (cfg.get("operation_roots") or {}).items():
            if operation_id.startswith(prefix):
                roots += mapped
                sources.append(f"operation namespace {prefix}")
        for root in explicit_roots:
            roots.append(root)
            sources.append("maintainer-declared root")
        roots = sorted(set(r.rstrip("/") for r in roots))
        if not roots:
            raise CoordinationConflict("cannot determine which module this gap touches: give the issue a "
                                       "capability that exists in the registry, or a Maintainer adds a "
                                       "`gap-root::<path>` label (e.g. gap-root::app/ERP/Capabilities/OwnerApi)")
        return Footprint(roots, sources)

    # -- checks ----------------------------------------------------------------
    def conflicts(self, footprint: Footprint) -> list[dict]:
        found = []
        for resv in self.reservations():
            reasons = []
            if resv.undeclared:
                reasons.append(f"{resv.task} is {resv.status} and declares no paths, so it may touch any module")
            for root in footprint.roots:
                if resv.root and roots_overlap(root, resv.root):
                    reasons.append(f"module root {resv.root} is reserved")
                for path in resv.write_set:
                    if path_overlap(root + "/**", path) and path not in self.shared:
                        reasons.append(f"write set path {path} is inside {root}")
                        break
            if reasons:
                found.append({"task": resv.task, "status": resv.status, "agent": resv.agent,
                              "lease_until": resv.lease_until, "lease_expired": resv.lease_expired,
                              "reason": reasons[0]})
        return found

    def check_changed_paths(self, changed: list[str]) -> list[dict]:
        """Paths of a finished gap change that another active task has reserved."""
        found = []
        for resv in self.reservations():
            for path in changed:
                if path in self.shared or any(path.startswith(s.rstrip("/") + "/") for s in self.shared if s.endswith("/")):
                    continue
                hit = next((w for w in resv.write_set if path_overlap(path, w)), None)
                if hit is None and not resv.write_set and resv.root and roots_overlap(path, resv.root):
                    hit = f"{resv.root} (undeclared reservation)"
                if hit:
                    found.append({"task": resv.task, "agent": resv.agent, "path": path, "reserved": hit})
        return found

    def collisions(self, worktree: Path, branch: str) -> list[str]:
        """Worktree/branch names that collide with anything the coordinator knows about."""
        problems = []
        state = self.state()
        wt = str(Path(worktree).resolve())
        repo = str(self.repo.resolve())
        if wt == repo or wt.startswith(repo + "/"):
            problems.append("the gap workspace is inside the development checkout")
        for task_id, ts in state["tasks"].items():
            other = ts.get("worktree")
            if other and (wt == str(Path(other)) or wt.startswith(str(Path(other)) + "/")
                          or str(Path(other)).startswith(wt + "/")):
                problems.append(f"workspace collides with {task_id}'s worktree {other}")
            if ts.get("branch") and ts["branch"] == branch:
                problems.append(f"branch {branch} is {task_id}'s branch")
        for resv in self.hotfix_reservations():
            other = resv.worktree
            if other and (wt == str(Path(other)) or wt.startswith(str(Path(other)) + "/")
                          or str(Path(other)).startswith(wt + "/")):
                problems.append(f"workspace collides with {resv.task}'s worktree {other}")
            if resv.branch and resv.branch == branch:
                problems.append(f"branch {branch} is {resv.task}'s branch")
        if not branch.startswith("gap/"):
            problems.append("gap branches must live in the gap/ namespace")
        return problems


class LeaseStore:
    """Gap-side exclusive leases per module root (the coordinator cannot hold them for us)."""

    def __init__(self, state_dir: Path, *, now=lambda: datetime.now(timezone.utc),
                 alive=lambda pid: Path(f"/proc/{pid}").exists()):
        self.dir = Path(state_dir)
        self.path = self.dir / "leases.json"
        self.lock_path = self.dir / "leases.lock"
        self.now = now
        self.alive = alive

    def _locked(self):
        self.dir.mkdir(parents=True, exist_ok=True)
        handle = open(self.lock_path, "a+")
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        return handle

    def _read(self) -> dict:
        try:
            return json.loads(self.path.read_text())
        except (OSError, json.JSONDecodeError):
            return {}

    def _write(self, leases: dict) -> None:
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(leases, indent=1))
        os.replace(tmp, self.path)

    def _live(self, lease: dict) -> bool:
        until = _parse(lease.get("until"))
        return bool(until and until > self.now() and self.alive(lease.get("pid", 0)))

    def acquire(self, issue: int, roots: list[str], ttl_seconds: int, pid: int | None = None) -> None:
        handle = self._locked()
        try:
            leases = {k: v for k, v in self._read().items() if self._live(v)}  # abandoned ones are dropped here
            for key, lease in leases.items():
                if key != str(issue) and any(roots_overlap(a, b) for a in roots for b in lease["roots"]):
                    raise CoordinationConflict(f"another gap dispatch (#{key}) already holds a lease on "
                                               f"{lease['roots']}")
            until = self.now().timestamp() + ttl_seconds
            leases[str(issue)] = {"roots": roots, "pid": pid or os.getpid(),
                                  "until": datetime.fromtimestamp(until, timezone.utc).isoformat()}
            self._write(leases)
        finally:
            handle.close()

    def release(self, issue: int) -> None:
        handle = self._locked()
        try:
            leases = self._read()
            if leases.pop(str(issue), None) is not None:
                self._write(leases)
        finally:
            handle.close()

    def reap(self) -> list[str]:
        """Drop leases whose owner died or whose TTL passed. Returns the issue numbers released."""
        handle = self._locked()
        try:
            leases = self._read()
            dead = [k for k, v in leases.items() if not self._live(v)]
            for key in dead:
                del leases[key]
            if dead:
                self._write(leases)
            return dead
        finally:
            handle.close()

    def held(self) -> dict:
        return {k: v for k, v in self._read().items() if self._live(v)}
