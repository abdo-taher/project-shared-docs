#!/usr/bin/env python3
"""capitalix-gap: report an API gap against your pinned Capitalix contract, and follow it.

Stdlib only (Python >= 3.9). Copy it next to capitalix_contract.py and
capitalix_gap_core.py (the same tool/ directory), then:

  python3 tool/capitalix_gap.py new --type MISSING_OPERATION --actor owner --capability CAP-OWN-180 \\
      --location customers.list --feature "Customers list" --project my-app --platform flutter \\
      --expected "..." --actual "..." --criterion "..."          create .capitalix-gaps/<id>.json
  python3 tool/capitalix_gap.py validate FILE        check a request offline (and against the pin)
  python3 tool/capitalix_gap.py search FILE          already reported? (anonymous)
  python3 tool/capitalix_gap.py submit FILE          create the GitHub issue (needs write credentials)
  python3 tool/capitalix_gap.py status ISSUE         coordinator state, backend status, resolution, your pin
  python3 tool/capitalix_gap.py confirm ISSUE --tests-passed   after you upgraded and tested

Reading is anonymous for the public repository. Submitting and confirming need a
GitHub identity: $GITHUB_TOKEN / $GH_TOKEN, else a logged-in `gh`. Without one,
`submit` keeps the request, writes the issue text next to it and prints a
prefilled "new issue" link; it never claims a submission that did not happen.

This tool never changes contract.lock: upgrading is always your explicit
`capitalix_contract.py update --version V`.

Exit codes: 0 ok; 1 check failed or refused; 2 source unreachable; 3 usage or
input error; 5 not submitted (no write credentials) — the request is kept.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import capitalix_contract as cc  # noqa: E402
import capitalix_gap_core as core  # noqa: E402

DEFAULT_REPO = "abdo-taher/project-shared-docs"
DEFAULT_GAPS = ".capitalix-gaps"
STATE_MARKER = "capitalix-gap-coordinator:v1"
VERIFY_MARKER = "capitalix-gap-verification:v1"
TRUSTED_ASSOCIATIONS = {"OWNER", "MEMBER", "COLLABORATOR"}
NOT_SUBMITTED = 5


class Refused(Exception):
    pass


# --------------------------------------------------------------------------- GitHub access

def _token() -> str | None:
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or None


def _headers() -> dict:
    headers = {"User-Agent": f"capitalix-gap/{core.CORE_VERSION}", "Accept": "application/vnd.github+json"}
    token = _token()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def api_get(path: str) -> object:
    try:
        return json.loads(cc.http_get(f"{cc.API_BASE}/{path}", _headers(), path))
    except cc.HttpStatusError as exc:
        hint = {401: " — the token in GITHUB_TOKEN/GH_TOKEN was rejected",
                403: " — rate limited or forbidden; set GITHUB_TOKEN for a higher limit",
                404: " — not found"}.get(exc.code, "")
        raise cc.SourceError(f"{path}: HTTP {exc.code}{hint}") from None
    except json.JSONDecodeError:
        raise cc.SourceError(f"{path}: response is not JSON") from None


def gap_issues(repo: str) -> list[dict]:
    issues, page = [], 1
    while page <= 20:
        batch = api_get(f"repos/{repo}/issues?state=all&labels=api-gap&per_page=100&page={page}")
        issues += [i for i in batch if "pull_request" not in i]
        if len(batch) < 100:
            break
        page += 1
    return issues


def write_credentials() -> str | None:
    if _token():
        return "token"
    if shutil.which("gh") and subprocess.run(["gh", "auth", "status"], stdout=subprocess.DEVNULL,
                                             stderr=subprocess.DEVNULL).returncode == 0:
        return "gh"
    return None


def api_post(path: str, payload: dict) -> dict:
    """POST once (never retried: a retry after an ambiguous failure could duplicate the issue)."""
    method = write_credentials()
    data = json.dumps(payload).encode()
    if method == "token":
        request = urllib.request.Request(f"{cc.API_BASE}/{path}", data=data, method="POST",
                                         headers={**_headers(), "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(request, timeout=cc.HTTP_TIMEOUT) as response:
                return json.loads(response.read())
        except urllib.error.HTTPError as exc:
            hint = {401: "the token was rejected", 403: "the token cannot create issues here",
                    404: "repository not found, or the token cannot see it",
                    410: "issues are disabled", 422: "GitHub refused the content"}.get(exc.code, "")
            raise cc.SourceError(f"POST {path}: HTTP {exc.code} {hint}".strip()) from None
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise cc.SourceError(f"POST {path}: no confirmed response ({type(exc).__name__}); run `search` "
                                 "before retrying so the request is not filed twice") from None
    if method == "gh":
        result = subprocess.run(["gh", "api", "-X", "POST", path, "--input", "-"], input=data,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise cc.SourceError(f"POST {path} via gh failed (exit {result.returncode}); run `search` before "
                                 "retrying")
        return json.loads(result.stdout)
    raise LookupError("no write credentials")


# --------------------------------------------------------------------------- request building

def read_text(value: str) -> str:
    return Path(value[1:]).read_text(encoding="utf-8") if value.startswith("@") else value


def pinned(args) -> tuple[dict, dict]:
    directory = Path(args.dir)
    lock = cc.verify_local(directory)
    return lock, cc.load_contract(directory)


def find(document: dict, operation_id: str | None, method: str | None, path: str | None):
    for m, p, op, item in cc.operations(document):
        if operation_id and op.get("operationId") == operation_id:
            return m, p, op
        if not operation_id and method and path and m == method.upper() \
                and core.normalize_path(p) == core.normalize_path(path):
            return m, p, op
    return None


def check_against_pin(request: dict, document: dict, lock: dict) -> list[str]:
    """Consistency of a request with the pinned contract (the coordinator re-checks all of it)."""
    problems = []
    if request["contract"] != {"version": lock["version"], "sha256": lock["sha256"]}:
        problems.append(f"contract: the request names {request['contract'].get('version')}, the pin is "
                        f"{lock['version']}")
    if request["gap_type"] == "MISSING_OPERATION":
        proposed = request.get("proposed") or {}
        if proposed.get("method") and proposed.get("path") and find(document, None, proposed["method"],
                                                                     proposed["path"]):
            problems.append("proposed: that operation exists in your pinned contract — report a mismatch type")
    elif request.get("operation"):
        op = request["operation"]
        found = find(document, op.get("operation_id"), op.get("method"), op.get("path"))
        if not found:
            problems.append("operation: not in your pinned contract (use MISSING_OPERATION, or `inspect` to find it)")
        elif not found[1].startswith(f"/api/{request['actor']}/"):
            problems.append(f"actor: the operation is not in the /api/{request['actor']}/ namespace")
    return problems


def cmd_new(args) -> int:
    lock, document = pinned(args)
    request = {
        "schema_version": core.SCHEMA_VERSION,
        "request_id": "gap-" + uuid.uuid4().hex[:20],
        "consumer": {"project": args.project, "platform": args.platform},
        "feature": args.feature,
        "actor": args.actor,
        "gap_type": args.type,
        "contract": {"version": lock["version"], "sha256": lock["sha256"]},
        "expected": read_text(args.expected),
        "actual": read_text(args.actual),
        "acceptance_criteria": args.criterion,
        "submitted_at": core.utc_now(),
    }
    if args.capability:
        request["capability_id"] = args.capability
    if args.location:
        request["location"] = args.location
    if args.requirement:
        request["requirements"] = args.requirement
    if args.severity:
        request["severity"] = args.severity
    if args.evidence:
        kinds = args.evidence_kind or []
        request["evidence"] = [{"kind": kinds[i] if i < len(kinds) else "note",
                                "content": Path(f).read_text(encoding="utf-8")} for i, f in enumerate(args.evidence)]
    if args.type == "MISSING_OPERATION":
        if args.operation:
            print("ERROR: --operation names an existing operation; MISSING_OPERATION uses --capability "
                  "and --location (optionally --method/--path as a suggestion)", file=sys.stderr)
            return 3
        if args.method or args.path:
            request["proposed"] = {k: v for k, v in (("method", (args.method or "").upper()), ("path", args.path)) if v}
    elif args.operation or args.method or args.path:
        found = find(document, args.operation, args.method, args.path)
        if found is None:
            print("FAILED: that operation is not in your pinned contract — check with `capitalix_contract.py "
                  "inspect`, or report MISSING_OPERATION", file=sys.stderr)
            return 1
        method, path, op = found
        request["operation"] = {"operation_id": op["operationId"], "method": method, "path": path} \
            if op.get("operationId") else {"method": method, "path": path}
    errors = core.validate(request) + (check_against_pin(request, document, lock) if not core.validate(request) else [])
    if errors:
        for error in errors:
            print(f"INVALID: {error}", file=sys.stderr)
        return 1
    out = Path(args.out) if args.out else Path(args.gaps) / f"{request['request_id']}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(request, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    print(f"fingerprint {core.fingerprint(request)[:16]} — next: `search {out}`, then `submit {out}`")
    return 0


def load_request(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def cmd_validate(args) -> int:
    request = load_request(args.file)
    errors = core.validate(request)
    if not errors and (Path(args.dir) / "contract.lock").is_file():
        lock, document = pinned(args)
        errors = check_against_pin(request, document, lock)
    for error in errors:
        print(f"INVALID: {error}", file=sys.stderr)
    if errors:
        return 1
    print(f"valid {core.SCHEMA_VERSION} request; fingerprint {core.fingerprint(request)[:16]}")
    return 0


# --------------------------------------------------------------------------- search / submit

def canonical_fingerprint(request: dict, document: dict | None) -> str:
    operation = request.get("operation") or {}
    if document and operation and not operation.get("operation_id"):
        found = find(document, None, operation.get("method"), operation.get("path"))
        if found and found[2].get("operationId"):
            request = {**request, "operation": {**operation, "operation_id": found[2]["operationId"]}}
    return core.fingerprint(request)


def matches(repo: str, fingerprint: str, document: dict | None) -> list[dict]:
    """Reported gaps whose recomputed fingerprint starts with `fingerprint` (full or prefix)."""
    found = []
    for issue in gap_issues(repo):
        request, problems = core.parse_issue_body(issue.get("body") or "", issue["number"],
                                                  issue.get("created_at", ""))
        if problems or core.validate(request):
            continue
        if canonical_fingerprint(request, document).startswith(fingerprint):
            found.append({"number": issue["number"], "state": issue["state"], "url": issue["html_url"],
                          "project": request["consumer"]["project"],
                          "labels": sorted(l["name"] for l in issue.get("labels", []) if l["name"].startswith("gap:"))})
    return found


def optional_document(args) -> dict | None:
    try:
        return pinned(args)[1]
    except (cc.CheckFailed, OSError):
        return None


def cmd_search(args) -> int:
    document = optional_document(args)
    if args.fingerprint:
        fingerprint = args.fingerprint
    else:
        request = load_request(args.file)
        if core.validate(request):
            print("INVALID: validate the request first", file=sys.stderr)
            return 1
        fingerprint = canonical_fingerprint(request, document)
    found = matches(args.repo, fingerprint.lower(), document)
    if not found:
        print(f"no reported gap with fingerprint {fingerprint[:16]}")
        return 0
    for m in found:
        print(f"#{m['number']} {m['state']} {' '.join(m['labels']) or '-'} ({m['project']}) {m['url']}")
    return 0


def cmd_submit(args) -> int:
    path = Path(args.file)
    request = load_request(args.file)
    errors = core.validate(request)
    document = None
    if not errors and (Path(args.dir) / "contract.lock").is_file():
        lock, document = pinned(args)
        errors = check_against_pin(request, document, lock)
    if errors:
        for error in errors:
            print(f"INVALID: {error}", file=sys.stderr)
        return 1
    fingerprint = canonical_fingerprint(request, document)
    existing = [m for m in matches(args.repo, fingerprint, document) if m["state"] == "open"]
    mine = [m for m in existing if m["project"] == request["consumer"]["project"]]
    if mine and not args.allow_duplicate:
        print(f"REFUSED: {request['consumer']['project']} already reported this gap as #{mine[0]['number']} "
              f"({mine[0]['url']})", file=sys.stderr)
        return 1
    if existing:
        print(f"note: #{existing[0]['number']} tracks the same gap for another consumer; your report will be "
              "linked to the same backend work")
    title, body = core.render_issue(request)
    payload = {"title": title, "body": body, "labels": ["api-gap", "gap:submitted"]}
    if args.dry_run:
        print(f"DRY RUN — would create in {args.repo}: {title}")
        return 0
    try:
        created = api_post(f"repos/{args.repo}/issues", payload)
    except LookupError:
        issue_file = path.with_suffix(".issue.md")
        issue_file.write_text(f"{title}\n\n{body}", encoding="utf-8")
        query = urllib.parse.urlencode({"title": title, "body": body, "labels": "api-gap"})
        print("NOT_SUBMITTED: no GitHub write credentials (set GITHUB_TOKEN/GH_TOKEN or run `gh auth login`).")
        print(f"The request is kept in {path}; the issue text is in {issue_file}.")
        url = f"https://github.com/{args.repo}/issues/new?{query}"
        print(f"Open: {url}" if len(url) <= 7500 else
              f"Open https://github.com/{args.repo}/issues/new and paste {issue_file}")
        return NOT_SUBMITTED
    if not isinstance(created, dict) or not created.get("number") or not created.get("html_url"):
        print("FAILED: GitHub did not confirm an issue; run `search` before retrying", file=sys.stderr)
        return 1
    record = {"issue": created["number"], "url": created["html_url"], "fingerprint": fingerprint,
              "submitted_at": core.utc_now()}
    path.with_suffix(".submission.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"SUBMITTED #{created['number']} {created['html_url']}")
    return 0


# --------------------------------------------------------------------------- status / confirm

def coordinator_state(repo: str, number: int) -> tuple[dict, dict | None]:
    issue = api_get(f"repos/{repo}/issues/{number}")
    comments = api_get(f"repos/{repo}/issues/{number}/comments?per_page=100")
    state = None
    for comment in comments:
        if comment.get("author_association") not in TRUSTED_ASSOCIATIONS:
            continue  # only repository members can speak for the coordinator
        body = comment.get("body") or ""
        start = body.find(f"<!-- {STATE_MARKER} ")
        if start >= 0:
            try:
                state = json.loads(body[start + len(STATE_MARKER) + 6:body.index(" -->", start)])
            except (ValueError, json.JSONDecodeError):
                continue
    return issue, state


def pin_includes(args, version: str) -> tuple[bool | None, str]:
    try:
        lock = cc.verify_local(Path(args.dir))
    except cc.CheckFailed as exc:
        return None, str(exc)
    index = cc.fetch_json(lock["source"], f"{cc.PUBLISHED_ROOT}/index.json").get("versions", [])
    order = [v["version"] for v in index]
    if version not in order or lock["version"] not in order:
        return None, "version not in the published index"
    return order.index(lock["version"]) >= order.index(version), lock["version"]


def cmd_status(args) -> int:
    issue, state = coordinator_state(args.repo, args.issue)
    labels = [l["name"] for l in issue.get("labels", []) if l["name"].startswith("gap:")]
    print(f"#{args.issue} [{issue['state']}] {issue['title']}")
    print(f"labels: {' '.join(labels) or '-'}")
    if not state:
        print("coordinator: not processed yet")
        return 0
    print(f"coordinator: {state.get('state')} ({state.get('reason')})")
    if state.get("fingerprint"):
        print(f"fingerprint: {state['fingerprint'][:16]}")
    if state.get("backend"):
        print(f"backend ticket: BE-{state['backend']}")
    resolution = state.get("resolution")
    if not resolution:
        print("resolution: none published yet")
        return 0
    print(f"resolution: contract {resolution['version']} (sha256 {resolution['sha256'][:16]}…)")
    included, detail = pin_includes(args, resolution["version"])
    if included is None:
        print(f"your pin: unknown ({detail})")
    elif included:
        print(f"your pin {detail} includes the resolution — run your tests, then `confirm {args.issue} --tests-passed`")
    else:
        print(f"your pin {detail} is older than the resolution. Upgrade explicitly: "
              f"`capitalix_contract.py update --version {resolution['version']}` (nothing changes on its own)")
    return 0


def cmd_confirm(args) -> int:
    if not args.tests_passed:
        print("REFUSED: confirm only after your contract checks and integration tests pass (--tests-passed)",
              file=sys.stderr)
        return 1
    issue, state = coordinator_state(args.repo, args.issue)
    resolution = (state or {}).get("resolution")
    if not resolution:
        print("REFUSED: the coordinator has not published a resolution for this issue", file=sys.stderr)
        return 1
    lock = cc.verify_local(Path(args.dir))
    included, detail = pin_includes(args, resolution["version"])
    if not included:
        print(f"REFUSED: your pin ({detail}) does not include {resolution['version']}; upgrade explicitly first",
              file=sys.stderr)
        return 1
    payload = {"fingerprint": state["fingerprint"], "version": lock["version"], "sha256": lock["sha256"],
               "tests_passed": True, "tool": f"capitalix_gap.py {core.CORE_VERSION}"}
    body = (f"<!-- {VERIFY_MARKER} {json.dumps(payload, sort_keys=True)} -->\n"
            f"Consumer verification: pinned `{lock['version']}`, local verification passed, tests passed.")
    try:
        created = api_post(f"repos/{args.repo}/issues/{args.issue}/comments", {"body": body})
    except LookupError:
        print("NOT_SUBMITTED: no GitHub write credentials. Post this comment on the issue yourself:\n")
        print(body)
        return NOT_SUBMITTED
    if not isinstance(created, dict) or not created.get("id"):
        print("FAILED: GitHub did not confirm the comment", file=sys.stderr)
        return 1
    print(f"CONFIRMED on #{args.issue}; the coordinator records it on its next run")
    return 0


# --------------------------------------------------------------------------- CLI

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="capitalix_gap.py", description=__doc__.split("\n\n")[0])
    parser.add_argument("--dir", default=cc.DEFAULT_DIR, help="pin directory (default .capitalix-contract)")
    parser.add_argument("--repo", default=DEFAULT_REPO, help="intake repository")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("new", help="create a structured gap request from your pinned contract")
    p.add_argument("--type", required=True, choices=core.GAP_TYPES)
    p.add_argument("--actor", required=True, choices=core.ACTORS)
    p.add_argument("--feature", required=True)
    p.add_argument("--project", required=True, help="your consumer project name")
    p.add_argument("--platform", required=True, choices=core.PLATFORMS)
    p.add_argument("--capability", help="capability id, e.g. CAP-OWN-180 (required when the route does not exist)")
    p.add_argument("--operation", help="operationId of the existing operation")
    p.add_argument("--method", choices=core.METHODS + tuple(m.lower() for m in core.METHODS))
    p.add_argument("--path", help="canonical /api/... path (existing operation, or a suggestion for a missing one)")
    p.add_argument("--location", help="field/schema location (e.g. data.items[].phone) or the missing action")
    p.add_argument("--expected", required=True, help="text, or @file")
    p.add_argument("--actual", required=True, help="text, or @file")
    p.add_argument("--criterion", action="append", required=True, help="acceptance criterion (repeat)")
    p.add_argument("--requirement", action="append", help="requirement reference (repeat)")
    p.add_argument("--evidence", action="append", help="sanitized evidence file (repeat)")
    p.add_argument("--evidence-kind", action="append", choices=core.EVIDENCE_KINDS)
    p.add_argument("--severity", choices=core.SEVERITIES, help="a suggestion; the backend decides")
    p.add_argument("--gaps", default=DEFAULT_GAPS)
    p.add_argument("--out")
    p.set_defaults(func=cmd_new)

    p = sub.add_parser("validate", help="validate a request file")
    p.add_argument("file")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("search", help="find already reported gaps (anonymous)")
    p.add_argument("file", nargs="?")
    p.add_argument("--fingerprint")
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("submit", help="create the GitHub issue (write credentials required)")
    p.add_argument("file")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--allow-duplicate", action="store_true", help="file even if your project already reported it")
    p.set_defaults(func=cmd_submit)

    p = sub.add_parser("status", help="coordinator state, resolution version, and whether your pin includes it")
    p.add_argument("issue", type=int)
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("confirm", help="record your verification after upgrading and testing")
    p.add_argument("issue", type=int)
    p.add_argument("--tests-passed", action="store_true")
    p.set_defaults(func=cmd_confirm)

    args = parser.parse_args(argv)
    if args.command == "search" and not (args.file or args.fingerprint):
        parser.error("search needs FILE or --fingerprint")
    try:
        return args.func(args)
    except Refused as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1
    except cc.CheckFailed as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 1
    except cc.SourceError as exc:
        print(f"SOURCE UNREACHABLE: {exc}", file=sys.stderr)
        return 2
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
