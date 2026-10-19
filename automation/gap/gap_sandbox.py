"""Run the coding-agent runner inside a Docker container.

What the agent can see:
  - its worktree (read-write) and the prompt file (read-only);
  - the agent image's own filesystem (read-only root) and a private tmpfs home and /tmp;
  - the agent executable (read-only);
  - a private configuration directory holding ONLY the agent's own login (the
    `claudeAiOauth` entry; never MCP/plugin tokens), or a dedicated token passed
    through the environment.

What it cannot see: the owner's home directory (SSH keys, glab/gh config, other
repositories and agent worktrees, session transcripts), /var/www, host processes,
the Docker socket. All capabilities are dropped, privilege escalation is off,
memory/CPU/process counts are capped, and the environment is rebuilt from an
allowlist (nothing is inherited from the dispatcher).

Network stays on (the agent talks to its model API and may fetch dependencies):
the sandbox limits what the agent can read and write, not where it can connect.

bubblewrap was evaluated and rejected for this host: Ubuntu's AppArmor blocks
unprivileged user namespaces (kernel.apparmor_restrict_unprivileged_userns=1)
and systemd user-service sandboxing silently falls back to no isolation.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import uuid
from pathlib import Path

AUTH_ENV = ("CLAUDE_CODE_OAUTH_TOKEN", "ANTHROPIC_API_KEY")
AGENT_BIN = "/opt/agent/bin"
LABEL = "capitalix-gap-agent"


class SandboxUnavailable(Exception):
    pass


def available(image: str) -> tuple[bool, str]:
    """(usable, reason). Usable = docker answers and the image exists locally."""
    if not shutil.which("docker"):
        return False, "docker is not installed"
    probe = subprocess.run(["docker", "image", "inspect", image, "--format", "{{.Id}}"], capture_output=True, text=True)
    if probe.returncode != 0:
        return False, (f"image {image} is missing or the docker daemon is unreachable "
                       f"(build it: docker build -f ci/gap-agent.Dockerfile -t {image} ci)")
    return True, "ok"


def agent_config(run_dir: Path, source_home: Path | None = None) -> tuple[Path, dict, dict]:
    """A private config dir with only the agent's own login.

    Returns (dir, public env, secret env). Secret env values are never put on a command line: the container gets
    only their names (`-e NAME`) and the values travel in the docker client's process environment.
    """
    cfg = run_dir / "agent-config"
    cfg.mkdir(parents=True, exist_ok=True)
    os.chmod(cfg, 0o700)
    env: dict = {"CLAUDE_CONFIG_DIR": "/agent-config"}
    secret_env: dict = {}
    for name in AUTH_ENV:
        value = os.environ.get(f"API_GAP_AGENT_{name}") or None
        if value:
            secret_env[name] = value
    if not secret_env:
        creds = (source_home or Path.home()) / ".claude" / ".credentials.json"
        try:
            login = {"claudeAiOauth": json.loads(creds.read_text())["claudeAiOauth"]}
        except (OSError, KeyError, json.JSONDecodeError):
            raise SandboxUnavailable("no agent login found: set API_GAP_AGENT_CLAUDE_CODE_OAUTH_TOKEN "
                                     "(from `claude setup-token`) or log in with `claude`") from None
        target = cfg / ".credentials.json"
        target.write_text(json.dumps(login))
        os.chmod(target, 0o600)
    return cfg, env, secret_env


def docker_command(argv: list[str], *, name: str, image: str, worktree: Path, readonly_files: list[Path],
                   config_dir: Path | None, extra_env: dict, memory: str = "4g", cpus: str = "2",
                   pids: int = 512, agent_executable: Path | None = None, max_seconds: int | None = None,
                   secret_env: dict | None = None, tools_dir: Path | None = None) -> list[str]:
    """The `docker run` command line that runs `argv` inside the sandbox."""
    uid, gid = os.getuid(), os.getgid()
    cmd = ["docker", "run", "--rm", "-i", "--name", name, "--label", f"{LABEL}=1", "--user", f"{uid}:{gid}", "--read-only",
           "--cap-drop", "ALL", "--security-opt", "no-new-privileges", "--pids-limit", str(pids),
           "--memory", memory, "--cpus", cpus, "--tmpfs", "/tmp:rw,exec,mode=1777,size=2g",
           "--tmpfs", "/home/agent:rw,exec,mode=1777,size=1g", "--hostname", "gap-agent",
           "-v", f"{worktree}:{worktree}:rw", "-w", str(worktree)]
    for path in readonly_files:
        cmd += ["-v", f"{path}:{path}:ro"]
    if tools_dir is not None:  # the repository's own gap tooling, read-only (e.g. the evidence checker)
        cmd += ["-v", f"{Path(tools_dir).resolve()}:/opt/gap-tools:ro"]
    if config_dir is not None:
        cmd += ["-v", f"{config_dir}:/agent-config:rw"]
    program = argv[0]
    if agent_executable is not None:
        target = f"{AGENT_BIN}/{Path(program).name}"
        cmd += ["-v", f"{agent_executable.resolve()}:{target}:ro"]
        program = target
    env = {"HOME": "/home/agent", "PATH": f"{AGENT_BIN}:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
           "LANG": "C.UTF-8", "CLAUDE_CODE_TMPDIR": "/home/agent/tmp", **extra_env}
    for key, value in env.items():
        cmd += ["-e", f"{key}={value}"]
    for key in (secret_env or {}):
        cmd += ["-e", key]  # name only: the value is taken from the docker client's environment, not from argv
    # hard limit inside the container: the agent cannot outlive a dispatcher that crashed or was SIGKILLed
    limit = ["timeout", "-s", "KILL", str(int(max_seconds) + 30)] if max_seconds else []
    return cmd + [image, *limit, program, *argv[1:]]


def kill(name: str) -> None:
    subprocess.run(["docker", "kill", name], capture_output=True)


def kill_orphans() -> list[str]:
    """Kill every agent container (one worker per host owns them all). Returns the container ids killed."""
    listed = subprocess.run(["docker", "ps", "-q", "--filter", f"label={LABEL}=1"], capture_output=True, text=True)
    ids = listed.stdout.split() if listed.returncode == 0 else []
    if ids:
        subprocess.run(["docker", "kill", *ids], capture_output=True)
    return ids


def new_name(prefix: str = "gap-agent") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:10]}"


def run_verification(image: str, worktree: Path, commands: list[str], *, tools_dir: Path | None, timeout: int,
                     memory: str = "4g", cpus: str = "2") -> list[dict]:
    """Re-run checks in ONE fresh container: no network, no agent login, no secrets, only the worktree writable.

    The commands share the container (so /tmp is shared between them) and run in order; the first failure stops the
    sequence. Returns one result per command that started: {command, exit, output_tail}. A hard time limit applies to
    the whole sequence.
    """
    uid, gid = os.getuid(), os.getgid()
    script = "\n".join(
        f'echo "::gapcmd:{i}:start"; ( {c}\n); rc=$?; echo "::gapcmd:{i}:exit:$rc"; [ "$rc" -eq 0 ] || exit "$rc"'
        for i, c in enumerate(commands))
    name = new_name("gap-verify")
    cmd = ["docker", "run", "--rm", "--name", name, "--label", f"{LABEL}=1", "--network", "none",
           "--user", f"{uid}:{gid}", "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
           "--pids-limit", "512", "--memory", memory, "--cpus", cpus,
           "--tmpfs", "/tmp:rw,exec,mode=1777,size=2g", "--tmpfs", "/home/agent:rw,exec,mode=1777,size=1g",
           "-v", f"{worktree}:{worktree}:rw", "-w", str(worktree), "-e", "HOME=/home/agent"]
    if tools_dir is not None:
        cmd += ["-v", f"{Path(tools_dir).resolve()}:/opt/gap-tools:ro"]
    cmd += [image, "timeout", "-s", "KILL", str(int(timeout)), "sh", "-c", script]
    timed_out, start_code = False, 0
    try:
        done = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 30)
        text, start_code = (done.stdout or "") + (done.stderr or ""), done.returncode
    except subprocess.TimeoutExpired as exc:
        kill(name)
        partial = exc.stdout or b""
        timed_out, text = True, (partial.decode(errors="replace") if isinstance(partial, bytes) else partial)
    results: list[dict] = []
    current: dict | None = None
    for line in text.splitlines():
        started = re.fullmatch(r"::gapcmd:(\d+):start", line)
        ended = re.fullmatch(r"::gapcmd:(\d+):exit:(\d+)", line)
        if started:
            current = {"command": commands[int(started.group(1))], "exit": None, "lines": []}
            results.append(current)
        elif ended and current is not None:
            current["exit"] = int(ended.group(2))
            current = None
        elif current is not None:
            current["lines"].append(line)
    for item in results:
        item["output_tail"] = "\n".join(item.pop("lines"))[-1500:]
        if item["exit"] is None:   # killed by the time limit, or the container died, mid-command
            item["exit"] = 124 if timed_out else 125
    if not results and (start_code != 0 or timed_out):   # the container never ran a command (e.g. image missing)
        results.append({"command": "(container start)", "exit": 124 if timed_out else start_code,
                        "output_tail": text[-1500:]})
    return results
