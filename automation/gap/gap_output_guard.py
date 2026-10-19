"""Scan what an agent produced before any of it leaves the host (push, pull request, notes).

An agent runs with its own login inside the container and an open network, so it could try (or be tricked by
untrusted request text into) writing a secret into the code, a commit message or a summary that the dispatcher
would then push or post. The dispatcher therefore scans, in this order, before anything is pushed:

  1. exact values of every secret that was reachable by or around the agent: its own login tokens, the dispatcher's
     environment secrets (GitLab/GitHub/CI tokens) -- found anywhere, in any text;
  2. high-confidence credential formats (private keys, GitHub / GitLab / Slack / AWS tokens, API secret keys).

Only secret *kinds* and locations are reported; values are never echoed. Generic patterns such as `password = ...`
are deliberately not used here: ordinary Laravel code and tests contain them, and blocking them would make every
change fail. They are still applied to anything that becomes public (request text, public summaries).
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

import gap_core as core

HARD_KINDS = {"private key", "GitHub token", "GitLab token", "AWS access key", "Slack token", "API secret key"}
MIN_SECRET_LENGTH = 12
SECRET_ENV_NAME = re.compile(r"^(API_GAP_.*|GITLAB_.*|GL_.*|GITHUB_.*|GH_.*|CI_JOB_TOKEN|.*_TOKEN|.*_SECRET|.*_PASSWORD"
                             r"|.*_API_KEY|ANTHROPIC_.*)$")
MAX_SCAN_BYTES = 40 * 1024 * 1024


def hard_findings(text: str) -> list[str]:
    return sorted({name for name, pattern in core.SENSITIVE_PATTERNS if name in HARD_KINDS and pattern.search(text)})


def secret_values_in(path: Path) -> list[str]:
    """Token-like string values of a login file (keys are ignored; nothing is returned for unreadable files)."""
    try:
        data = json.loads(Path(path).read_text())
    except (OSError, json.JSONDecodeError):
        return []
    found: list[str] = []

    def walk(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if isinstance(value, str) and re.search(r"(?i)token|secret|key|password", key):
                    found.append(value)
                else:
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(data)
    return [v for v in found if len(v) >= MIN_SECRET_LENGTH]


def environment_secrets(env: dict | None = None) -> list[str]:
    source = os.environ if env is None else env
    return [v for k, v in source.items() if SECRET_ENV_NAME.match(k) and len(v) >= MIN_SECRET_LENGTH]


def scan(texts: dict[str, str], known_secrets: list[str]) -> list[str]:
    """Findings like 'added code: GitHub token' or 'commit message: contains a secret the agent could reach'."""
    problems = []
    known = [s for s in set(known_secrets) if len(s) >= MIN_SECRET_LENGTH]
    for where, text in texts.items():
        text = text[:MAX_SCAN_BYTES]
        if any(secret in text for secret in known):
            problems.append(f"{where}: contains a secret value the agent could reach")
        for kind in hard_findings(text):
            problems.append(f"{where}: looks like a {kind}")
    return problems
