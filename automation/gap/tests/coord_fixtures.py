"""A development-repository fixture with the coordinator's real state shape (read-only adapter tests)."""

import json
import subprocess
from pathlib import Path

OWNER_API = "app/ERP/Capabilities/OwnerApi"
TASKS = {
    "CAP-OWN-180": {"conflict": "app/ERP/Modules/Expenses"},   # as in the real registry: not under OwnerApi
    "CAP-OWN-210": {"conflict": OWNER_API},
    "CAP-REG-005": {"conflict": "app/ERP/Capabilities/Onboarding"},
    "CAP-CUS-001": {"conflict": "app/ERP/Modules/Customers"},
}


def task_state(status="PENDING", agent=None, write_set=(), lease="2099-01-01T00:00:00Z", released=False,
               branch=None, worktree=None):
    return {"status": status, "agent": agent, "previous_agent": None, "write_set": list(write_set),
            "lease_until": lease, "write_set_released": released, "branch": branch, "worktree": worktree}


def make_dev_repo(root: Path, states: dict | None = None, shared=()) -> Path:
    repo = root / "dev"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "integration", str(repo)], check=True)
    (repo / "docs/final").mkdir(parents=True)
    registry = {"rules": {"shared_wiring_paths": list(shared)},
                "tasks": [{"task_id": tid, "default_conflict_key": v["conflict"], "code_root": v["conflict"]}
                          for tid, v in TASKS.items()]}
    (repo / "docs/final/AGENT_WAVE_TASK_REGISTRY.json").write_text(json.dumps(registry))
    write_state(repo, states or {})
    return repo


def write_state(repo: Path, states: dict) -> None:
    base = repo / ".git/capitalix-agent-coordination"
    base.mkdir(parents=True, exist_ok=True)
    tasks = {tid: task_state() for tid in TASKS}
    tasks.update(states)
    (base / "state.json").write_text(json.dumps({"version": 1, "tasks": tasks}))


def write_hotfix(repo: Path, hotfix_id: str, state: str, hints=(), changed=(), branch=None, worktree=None) -> None:
    directory = repo / ".state/hotfix/requests"
    directory.mkdir(parents=True, exist_ok=True)
    (directory / f"{hotfix_id}.json").write_text(json.dumps({
        "id": hotfix_id, "state": state, "paths_hint": list(hints), "changed_files": list(changed),
        "branch": branch or f"hotfix/{hotfix_id.lower()}", "worktree": worktree or f"/wt/hotfix-{hotfix_id}",
        "lease": {"at": "2026-10-19T13:00:00+00:00"}}))
