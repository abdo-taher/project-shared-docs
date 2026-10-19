#!/usr/bin/env python3
"""Validate the API gap credentials and activation prerequisites. Never prints a token.

  API_GAP_GITHUB_TOKEN=… API_GAP_BACKEND_TOKEN=… python3 automation/gap/gap_preflight.py [--json]

Checks (each PASS / WARN / FAIL / SKIP):
  GitHub token  — present; belongs to policy.coordinator_github_login; reads the intake repository;
                  is NOT able to read other private repositories (fine-grained, single-repository scope
                  expected: a token that can see the development repository is too broad); rate limit.
  Backend token — present; reads the backend repository (policy.backend_repository), its issues and pull
                  requests; fine-grained and not admin on that repository.
  Activation    — API_GAP_AUTOMATION_ENABLED must still be "false"/unset until the owner enables it
                  (reported as information when set).

Exit codes: 0 no FAIL; 1 at least one FAIL; 3 usage error. WARN never fails the run.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gap_coordinator import HERE, load_policy  # noqa: E402
from gap_http import ApiError, Http  # noqa: E402


class Report:
    def __init__(self):
        self.rows: list[tuple[str, str, str]] = []

    def add(self, status: str, check: str, detail: str = "") -> None:
        self.rows.append((status, check, detail))

    @property
    def failed(self) -> bool:
        return any(s == "FAIL" for s, _, _ in self.rows)


def github_checks(report: Report, policy: dict, token: str | None, http: Http | None = None,
                  base: str = "https://api.github.com") -> None:
    if not token:
        report.add("FAIL", "github token present", "API_GAP_GITHUB_TOKEN is not set")
        return
    kind = "fine-grained" if token.startswith("github_pat_") else ("classic" if token.startswith("ghp_") else "other")
    http = http or Http(base, {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {token}",
                               "X-GitHub-Api-Version": "2022-11-28"}, attempts=2)
    if kind == "classic":
        report.add("WARN", "github token type", "classic tokens cannot be limited to one repository; use a fine-grained "
                   "token (Issues: read & write, Metadata: read) or a GitHub App")
    elif kind == "fine-grained":
        report.add("PASS", "github token type", "fine-grained")
    repo = policy["github_repository"]
    if token.startswith("ghs_"):
        # An App installation token cannot call GET /user. Its identity is the bot account, and the repositories it
        # can reach are listed by the installation endpoint: exactly the intake repository is the least-privilege shape.
        report.add("PASS", "github token type", "app installation")
        app_login = os.environ.get("API_GAP_APP_LOGIN", "").strip()
        report.add("PASS" if app_login.endswith("[bot]") else "FAIL", "github identity",
                   f"app bot account {app_login}" if app_login.endswith("[bot]")
                   else "API_GAP_APP_LOGIN=<app-slug>[bot] is not set (state comments could not be recognised)")
        try:
            data, _ = http.request("GET", "installation/repositories")
            names = sorted(r["full_name"] for r in data.get("repositories", []))
            report.add("PASS" if names == [repo] else "FAIL", "github installation scope",
                       ", ".join(names) or "none" if names == [repo] else
                       f"token reaches {', '.join(names) or 'nothing'}; it must reach only {repo}")
        except ApiError as exc:
            report.add("FAIL", "github installation scope", str(exc))
    else:
        try:
            user, _ = http.request("GET", "user")
        except ApiError as exc:
            report.add("FAIL", "github token valid", str(exc))
            return
        login = user.get("login")
        expected = policy["coordinator_github_login"]
        report.add("PASS" if login == expected else "FAIL", "github identity",
                   f"token belongs to {login}" + ("" if login == expected else f", policy expects {expected}"))
    try:
        info, headers = http.request("GET", f"repos/{repo}")
        report.add("PASS", "github intake repository readable", repo)
        remaining = headers.get("X-RateLimit-Remaining")
        report.add("PASS" if remaining and int(remaining) > 200 else "WARN", "github rate limit remaining", str(remaining))
    except ApiError as exc:
        report.add("FAIL", "github intake repository readable", str(exc))
        return
    try:
        http.request("GET", f"repos/{repo}/issues", params={"per_page": 1})
        report.add("PASS", "github issues readable", "")
    except ApiError as exc:
        report.add("FAIL", "github issues readable", str(exc))
    other = (policy.get("development") or {}).get("repository")
    if other:
        try:
            http.request("GET", f"repos/{other}")
            report.add("FAIL", "github least privilege", f"the token can read {other}; it must be limited to {repo}")
        except ApiError as exc:
            if exc.status in (403, 404):
                report.add("PASS", "github least privilege", f"cannot read {other}")
            else:
                report.add("WARN", "github least privilege", f"could not verify ({exc})")
    login = policy["coordinator_github_login"]
    try:
        http.request("GET", f"repos/{repo}/collaborators/{login}/permission")
        report.add("PASS", "github can verify reporter trust", "collaborator permission lookup works")
    except ApiError as exc:
        report.add("FAIL", "github can verify reporter trust",
                   f"the collaborator permission lookup failed ({exc}); the coordinator would trust nobody. "
                   "Grant the token Metadata: read and make sure its owner has push access")
    report.add("SKIP", "github write permission", "verified only by the canary (labels/comment); not tested here "
               "because testing would write")


def backend_checks(report: Report, policy: dict, token: str | None, http: Http | None = None,
                   base: str = "https://api.github.com") -> None:
    if not token:
        report.add("FAIL", "backend token present", "API_GAP_BACKEND_TOKEN is not set")
        return
    kind = ("app installation" if token.startswith("ghs_") else "fine-grained" if token.startswith("github_pat_")
            else ("classic" if token.startswith(("ghp_", "gho_")) else "other"))
    http = http or Http(base, {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {token}",
                               "X-GitHub-Api-Version": "2022-11-28"}, attempts=2)
    scoped = kind in ("fine-grained", "app installation")
    report.add("PASS" if scoped else "WARN", "backend token type",
               kind + ("" if scoped else " (cannot be limited to one repository; use a fine-grained "
                       "token: Issues read/write, Pull requests read, Contents read, Metadata read)"))
    repo = policy["backend_repository"]
    try:
        info, _ = http.request("GET", f"repos/{repo}")
    except ApiError as exc:
        report.add("FAIL", "backend repository access", str(exc))
        return
    report.add("PASS", "backend repository access", f"{repo} (private={info.get('private')})")
    perms = info.get("permissions")
    if not perms:
        report.add("PASS", "backend repository role", "not reported for this token type (scoped by its permissions)")
    else:
        report.add("WARN" if perms.get("admin") else "PASS", "backend repository role",
                   "admin (broader than needed)" if perms.get("admin") else
                   ("write" if perms.get("push") else "read"))
    try:
        http.request("GET", f"repos/{repo}/issues", params={"labels": "api-gap", "per_page": 1})
        report.add("PASS", "backend issues readable", "")
    except ApiError as exc:
        report.add("FAIL", "backend issues readable", str(exc))
    try:
        http.request("GET", f"repos/{repo}/pulls", params={"per_page": 1})
        report.add("PASS", "backend pull requests readable", "")
    except ApiError as exc:
        report.add("FAIL", "backend pull requests readable", str(exc))


def activation_check(report: Report, env: dict) -> None:
    flag = (env.get("API_GAP_AUTOMATION_ENABLED") or "").lower()
    report.add("PASS" if flag != "true" else "WARN", "activation flag",
               "API_GAP_AUTOMATION_ENABLED is " + (flag or "unset") +
               ("" if flag != "true" else " — the scheduled job is ENABLED"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--policy", default=str(HERE / "policy.json"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        policy = load_policy(Path(args.policy))
    except (OSError, ValueError) as exc:
        print(f"ERROR: policy: {exc}", file=sys.stderr)
        return 3
    report = Report()
    github_checks(report, policy, os.environ.get("API_GAP_GITHUB_TOKEN"))
    backend_checks(report, policy, os.environ.get("API_GAP_BACKEND_TOKEN"))
    activation_check(report, dict(os.environ))
    if args.json:
        print(json.dumps([{"status": s, "check": c, "detail": d} for s, c, d in report.rows], indent=2))
    else:
        for status, check, detail in report.rows:
            print(f"{status:5} {check}" + (f" — {detail}" if detail else ""))
    return 1 if report.failed else 0


if __name__ == "__main__":
    sys.exit(main())
