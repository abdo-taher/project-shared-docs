#!/usr/bin/env python3
"""GitHub-only publication of the official Capitalix API contract.

  capitalix_publish.py fetch-build --backend-repo R --run-id N --out DIR      verify a backend build and download it
  capitalix_publish.py prepare --artifact F --build-record F --shared-repo D  lay out one new immutable version
  capitalix_publish.py verify [--shared-repo D] [--base-ref REF]              offline integrity + immutability check
  capitalix_publish.py verify-merge --repo R --sha S                          the change on main came through an approved publisher PR

The flow (docs/api-gap/README.md, step 7):

  1. `capitalix` workflow `contract-build.yml` generates docs/api/openapi.json from a commit of the development branch
     and uploads {openapi.json, build-record.json}.
  2. `fetch-build` asks the GitHub API whether that run is genuine (repository, workflow file, successful,
     manually dispatched, built from a commit that is on the development branch) and whether the downloaded bytes
     are the bytes the run recorded. Nothing the record says is believed without the API agreeing.
  3. `prepare` classifies the change against the current published contract (BREAKING and UNKNOWN fail closed unless
     explicitly allowed), refuses stale/rollback/duplicate publications, and writes the new version directory plus
     current.json / index.json. It never rewrites or deletes an existing version.
  4. The workflow opens a pull request. The owner's review of that pull request IS the approval (branch protection and
     the `verify` check enforce it); nothing is pushed to main.

Exit codes: 0 ok; 1 refused (a rule was violated); 3 input/environment error.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import openapi_compatibility as compat  # noqa: E402

ROOT = Path("api/implemented")
BUILD_WORKFLOW = ".github/workflows/contract-build.yml"
BUILD_ARTIFACT = "contract-build"
BUILD_SCHEMA = "capitalix-contract-build/1"
APPROVAL_SCHEMA = "capitalix-contract-approval/2"
MANIFEST_SCHEMA = "capitalix-contract-manifest/2"
APPROVAL_METHOD = "github-pull-request-review"
MAX_ARTIFACT_BYTES = 64 * 1024 * 1024
SUMMARY_KEYS = ("BREAKING", "UNKNOWN", "NON_BREAKING", "DOCUMENTATION_ONLY", "total")


class Refused(Exception):
    """A publication rule was violated (exit 1)."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def utc_timestamp(value: str) -> str:
    moment = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if moment.tzinfo is None:
        raise Refused(f"source commit date [{value}] has no UTC offset")
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def version_id(commit_date_utc: str, digest: str) -> str:
    """<source commit date UTC>-<sha256[:12]>: one identity can never name different bytes."""
    return f"{commit_date_utc[:10].replace('-', '.')}-{digest[:12]}"


def count_operations(document: dict) -> int:
    methods = {"get", "put", "post", "delete", "patch", "head", "options", "trace"}
    return sum(1 for item in document.get("paths", {}).values() for method in item if method in methods)


# --------------------------------------------------------------------------- GitHub API (read only)

class _NoAuthRedirect(urllib.request.HTTPRedirectHandler):
    """Artifact downloads redirect to a storage host: never forward the token there."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new is not None:
            new.headers.pop("Authorization", None)
            new.unredirected_hdrs.pop("Authorization", None)
        return new


class GitHubApi:
    def __init__(self, token: str, base: str = "https://api.github.com", timeout: float = 60):
        self.token, self.base, self.timeout = token, base.rstrip("/"), timeout

    def _request(self, path: str, accept: str) -> bytes:
        request = urllib.request.Request(f"{self.base}/{path}", headers={
            "Accept": accept, "Authorization": f"Bearer {self.token}", "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "capitalix-publish"})
        opener = urllib.request.build_opener(_NoAuthRedirect)
        try:
            with opener.open(request, timeout=self.timeout) as response:
                return response.read(MAX_ARTIFACT_BYTES + 1)
        except urllib.error.HTTPError as exc:
            raise Refused(f"GitHub API {path.split('?')[0]}: HTTP {exc.code}") from None
        except urllib.error.URLError as exc:
            raise Refused(f"GitHub API unreachable ({type(exc.reason).__name__})") from None

    def get(self, path: str) -> dict:
        return json.loads(self._request(path, "application/vnd.github+json"))

    def download(self, path: str) -> bytes:
        data = self._request(path, "application/vnd.github+json")
        if len(data) > MAX_ARTIFACT_BYTES:
            raise Refused("build artifact is larger than the allowed maximum")
        return data


def verify_build(api, repo: str, run_id: int, branch: str) -> tuple[bytes, dict, str]:
    """Return (openapi bytes, verified build record, commit date UTC) or raise Refused.

    Every property is checked against GitHub's own record of the run, not against the artifact's claims."""
    run = api.get(f"repos/{repo}/actions/runs/{run_id}")
    problems = []
    if (run.get("repository") or {}).get("full_name") != repo:
        problems.append("the run belongs to another repository")
    if not str(run.get("path", "")).startswith(BUILD_WORKFLOW):
        problems.append(f"the run is not of workflow {BUILD_WORKFLOW}")
    if run.get("status") != "completed" or run.get("conclusion") != "success":
        problems.append("the run did not complete successfully")
    if run.get("event") != "workflow_dispatch":
        problems.append("the run was not manually dispatched")
    if run.get("head_branch") != branch:
        problems.append(f"the run was not built from {branch}")
    if (run.get("head_repository") or {}).get("full_name", repo) != repo:
        problems.append("the run was built from a fork")
    sha = run.get("head_sha", "")
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        problems.append("the run has no commit")
    if problems:
        raise Refused("build run rejected: " + "; ".join(problems))
    compare = api.get(f"repos/{repo}/compare/{sha}...{branch}")
    if compare.get("status") not in ("ahead", "identical"):
        raise Refused(f"build commit {sha[:12]} is not on {branch}")
    artifacts = [a for a in api.get(f"repos/{repo}/actions/runs/{run_id}/artifacts").get("artifacts", [])
                 if a.get("name") == BUILD_ARTIFACT and not a.get("expired")]
    if len(artifacts) != 1:
        raise Refused(f"expected exactly one live '{BUILD_ARTIFACT}' artifact, found {len(artifacts)}")
    blob = api.download(f"repos/{repo}/actions/artifacts/{artifacts[0]['id']}/zip")
    openapi, record = extract_build(blob)
    if record.get("repository") != repo or record.get("commit") != sha or record.get("run_id") != run_id:
        raise Refused("build record does not match the GitHub run (repository, commit or run id)")
    if record.get("sha256") != sha256_bytes(openapi) or record.get("size") != len(openapi):
        raise Refused("the downloaded contract is not the contract the build recorded")
    commit = api.get(f"repos/{repo}/commits/{sha}")
    date = utc_timestamp(((commit.get("commit") or {}).get("committer") or {}).get("date", ""))
    record = {**record, "run_url": run.get("html_url", ""), "branch": branch}
    return openapi, record, date


def extract_build(blob: bytes) -> tuple[bytes, dict]:
    try:
        archive = zipfile.ZipFile(io.BytesIO(blob))
    except zipfile.BadZipFile:
        raise Refused("build artifact is not a zip archive") from None
    names = sorted(archive.namelist())
    if names != ["build-record.json", "openapi.json"]:
        raise Refused(f"build artifact must contain exactly build-record.json and openapi.json, found {names}")
    for info in archive.infolist():
        if info.file_size > MAX_ARTIFACT_BYTES:
            raise Refused("build artifact member is too large")
    try:
        record = json.loads(archive.read("build-record.json"))
    except json.JSONDecodeError:
        raise Refused("build-record.json is not valid JSON") from None
    if not isinstance(record, dict) or record.get("schema") != BUILD_SCHEMA:
        raise Refused("build-record.json has an unsupported schema")
    return archive.read("openapi.json"), record


# --------------------------------------------------------------------------- prepare

def blocking_changes(report: dict, category: str, limit: int = 12) -> str:
    """One `publish:` line per change that blocks the publication (kind, location, what changed), so the log of a
    refused run names the offending changes instead of only counting them."""
    rows = [c for c in report["changes"] if c["category"] == category]
    lines = [f"\npublish:   {category} {c['kind']} at {c['location']}: {c['description']}" for c in rows[:limit]]
    if len(rows) > limit:
        lines.append(f"\npublish:   ... and {len(rows) - limit} more {category} change(s)")
    return "".join(lines)


def prepare(artifact: Path, record: dict, commit_date: str, shared_repo: Path, *, allow_breaking: bool = False,
            allow_unknown: bool = False, approved_scope: list[str] | None = None, repo: str = "") -> str:
    """Write one new version into shared_repo/api/implemented. Returns the version id (or the existing one)."""
    data = artifact.read_bytes()
    digest = sha256_bytes(data)
    if record.get("sha256") != digest:
        raise Refused("the artifact is not the contract named by the verified build record")
    if repo and record.get("repository") != repo:
        raise Refused(f"the build is from {record.get('repository')}, publication accepts only {repo}")
    document = json.loads(data)
    commit_date = utc_timestamp(commit_date)

    root = shared_repo / ROOT
    index_path, current_path = root / "index.json", root / "current.json"
    index = load_json(index_path) if index_path.is_file() else {"schema": "capitalix-contract-index/1", "versions": []}
    current = load_json(current_path) if current_path.is_file() else None

    existing = next((v for v in index["versions"] if v["sha256"] == digest), None)
    if existing:
        if current and current.get("sha256") != digest:
            raise Refused(f"contract {digest[:12]} was published as {existing['version']} but current is "
                          f"{current.get('version')}: refusing to roll back")
        return existing["version"]
    if current and current.get("source_commit_date", "") > commit_date:
        raise Refused(f"source commit date {commit_date} is older than the current version {current['version']} "
                      f"({current['source_commit_date']}): refusing a stale publication")

    version = version_id(commit_date, digest)
    version_dir = root / "versions" / version
    if version_dir.exists():
        raise Refused(f"version directory [{version}] already exists: immutable versions are never rewritten")

    initial = current is None
    if initial:
        baseline_doc, baseline_label, baseline_digest = document, "(initial publication)", digest
    else:
        baseline_doc = load_json(root / current["openapi"])
        baseline_label, baseline_digest = f"published {current['version']}", current["sha256"]
    report = compat.build_report(baseline_doc, document, baseline_label, f"build {record['commit'][:12]}")
    summary = report["summary"]
    blockers = []
    if summary["UNKNOWN"] and not allow_unknown:
        blockers.append(("UNKNOWN", f"{summary['UNKNOWN']} unclassified change(s): UNKNOWN fails closed unless the "
                         "owner explicitly allows it for this publication"))
    if summary["BREAKING"] and not allow_breaking:
        blockers.append(("BREAKING", f"{summary['BREAKING']} breaking change(s): publication requires an explicit "
                         "allow-breaking decision recorded in the approval"))
    if blockers:
        raise Refused("; ".join(text for _, text in blockers)
                      + "".join(blocking_changes(report, category) for category, _ in blockers))
    markdown = compat.render_markdown(report)
    compatibility_digest = sha256_bytes(json.dumps(report["changes"], sort_keys=True).encode())

    approval = {
        "schema": APPROVAL_SCHEMA,
        "decision": "APPROVED",
        "approval_method": APPROVAL_METHOD,
        "approval_note": "Takes effect only when the owner approves and merges the publication pull request; "
                         "branch protection and the contract-publication-verify check enforce that on GitHub.",
        "approved_artifact_sha256": digest,
        "baseline_artifact_sha256": baseline_digest,
        "compatibility_digest": compatibility_digest,
        "compatibility_summary": {"BREAKING": summary["BREAKING"], "UNKNOWN": summary["UNKNOWN"]},
        "approved_scope": list(approved_scope or []),
        "allow_breaking": bool(allow_breaking),
        "allow_unknown": bool(allow_unknown),
        "initial_publication": initial,
        "build": {k: record[k] for k in ("repository", "commit", "run_id", "run_url", "branch") if k in record},
    }
    approval_bytes = (json.dumps(approval, indent=2, ensure_ascii=False) + "\n").encode()
    md_bytes = markdown.encode()

    version_dir.mkdir(parents=True)
    (version_dir / "openapi.json").write_bytes(data)
    (version_dir / "approval.json").write_bytes(approval_bytes)
    (version_dir / "compatibility.md").write_bytes(md_bytes)
    compat_summary = {k: summary.get(k, 0) for k in SUMMARY_KEYS}
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "version": version,
        "sha256": digest,
        "size": len(data),
        "openapi": document.get("openapi"),
        "info_version": document.get("info", {}).get("version"),
        "operations": count_operations(document),
        "source": {
            "repository": record["repository"],
            "commit": record["commit"],
            "commit_date": commit_date,
            "ref": record.get("branch", ""),
            "build_run_id": record["run_id"],
            "build_run_url": record.get("run_url", ""),
            "build_workflow": BUILD_WORKFLOW,
        },
        "approval": {
            "approved_by": "GitHub pull request review (owner)",
            "trusted_approval_id": "github-pull-request-review",
            "approval_method": APPROVAL_METHOD,
            "initial_publication": initial,
            "approval_manifest_sha256": sha256_bytes(approval_bytes),
            "signature": "None: approval is the owner's review of the publication pull request on GitHub. "
                         "Consumers verify the sha256 digests in this manifest and the build run named in source.",
        },
        "baseline": {"initial_publication": initial, "identity": baseline_label, "sha256": baseline_digest},
        "compatibility": compat_summary,
        "files": {"openapi.json": digest, "approval.json": sha256_bytes(approval_bytes),
                  "compatibility.md": sha256_bytes(md_bytes)},
    }
    write_json(version_dir / "manifest.json", manifest)
    index["versions"].append({
        "version": version, "sha256": digest, "source_commit": record["commit"], "source_commit_date": commit_date,
        "initial_publication": initial, "compatibility": compat_summary,
        "manifest": f"versions/{version}/manifest.json"})
    write_json(index_path, index)
    write_json(current_path, {
        "schema": "capitalix-contract-pointer/1", "version": version, "sha256": digest,
        "source_commit": record["commit"], "source_commit_date": commit_date,
        "openapi": f"versions/{version}/openapi.json", "manifest": f"versions/{version}/manifest.json"})
    add_changelog(root / "CHANGELOG.md", version, record, compat_summary)
    return version


def add_changelog(path: Path, version: str, record: dict, summary: dict) -> None:
    marker = "Newest first."
    entry = (f"\n## {version}\n\nBuilt by {record['repository']}@{record['commit'][:12]} "
             f"(run {record.get('run_url') or record['run_id']}). Changes vs the previous version: "
             f"{summary['BREAKING']} breaking, {summary['UNKNOWN']} unclassified, {summary['NON_BREAKING']} "
             f"non-breaking, {summary['DOCUMENTATION_ONLY']} documentation-only. Full list: "
             f"`versions/{version}/compatibility.md`. Upgrade explicitly: "
             f"`python3 tool/capitalix_contract.py update --version {version}`, then run your tests.\n")
    if not path.is_file():
        path.write_text("# Consumer-visible contract changes\n\nNewest first." + entry, encoding="utf-8")
        return
    text = path.read_text(encoding="utf-8")
    if marker in text:
        head, _, tail = text.partition(marker)
        # keep the paragraph that ends the introduction intact: insert after the first blank line that follows it
        rest = tail.split("\n\n", 1)
        text = head + marker + rest[0] + "\n" + entry + ("\n" + rest[1] if len(rest) > 1 else "")
    else:
        text += entry
    path.write_text(text, encoding="utf-8")


# --------------------------------------------------------------------------- verify (offline)

def verify_tree(shared_repo: Path, base_ref: str | None = None, max_new_versions: int | None = None) -> list[str]:
    """Return a list of problems (empty = the published tree is sound)."""
    root = shared_repo / ROOT
    problems: list[str] = []
    try:
        index = load_json(root / "index.json")
        current = load_json(root / "current.json")
    except (OSError, json.JSONDecodeError) as exc:
        return [f"index.json/current.json unreadable: {exc}"]
    versions = index.get("versions", [])
    if not versions:
        return ["index.json lists no versions"]
    on_disk = sorted(p.name for p in (root / "versions").iterdir() if p.is_dir()) if (root / "versions").is_dir() else []
    if on_disk != sorted(v["version"] for v in versions):
        problems.append("version directories and index.json disagree")
    dates = [v.get("source_commit_date", "") for v in versions]
    if dates != sorted(dates):
        problems.append("index.json is not ordered oldest to newest by source commit date")
    last = versions[-1]
    if (current.get("version"), current.get("sha256")) != (last["version"], last["sha256"]):
        problems.append("current.json does not point at the newest indexed version")
    for entry in versions:
        v = entry["version"]
        vdir = root / "versions" / v
        try:
            data = (vdir / "openapi.json").read_bytes()
            manifest = load_json(vdir / "manifest.json")
            approval_bytes = (vdir / "approval.json").read_bytes()
            approval = json.loads(approval_bytes)
            md = (vdir / "compatibility.md").read_bytes()
        except (OSError, json.JSONDecodeError) as exc:
            problems.append(f"{v}: unreadable ({type(exc).__name__})")
            continue
        digest = sha256_bytes(data)
        if digest != entry["sha256"] or manifest.get("sha256") != digest:
            problems.append(f"{v}: openapi.json digest differs from the index/manifest")
        if version_id(entry["source_commit_date"], digest) != v:
            problems.append(f"{v}: version id is not <commit date>-<sha256[:12]>")
        files = manifest.get("files", {})
        if files != {"openapi.json": digest, "approval.json": sha256_bytes(approval_bytes),
                     "compatibility.md": sha256_bytes(md)}:
            problems.append(f"{v}: manifest.files do not match the files")
        if (manifest.get("approval") or {}).get("approval_manifest_sha256") != sha256_bytes(approval_bytes):
            problems.append(f"{v}: manifest does not record the approval file digest")
        if approval.get("decision") != "APPROVED" or approval.get("approved_artifact_sha256") != digest:
            problems.append(f"{v}: approval does not approve these exact bytes")
        if approval.get("schema") == APPROVAL_SCHEMA:
            build = approval.get("build") or {}
            src = manifest.get("source") or {}
            if approval.get("approval_method") != APPROVAL_METHOD:
                problems.append(f"{v}: unsupported approval method")
            if (build.get("repository"), build.get("commit"), build.get("run_id")) != \
                    (src.get("repository"), src.get("commit"), src.get("build_run_id")):
                problems.append(f"{v}: approval build differs from the manifest source")
            summary = approval.get("compatibility_summary", {})
            if summary.get("BREAKING") and not approval.get("allow_breaking"):
                problems.append(f"{v}: breaking changes without an allow-breaking decision")
            if summary.get("UNKNOWN") and not approval.get("allow_unknown"):
                problems.append(f"{v}: unclassified changes without an allow-unknown decision")
        elif not approval.get("trusted_approval_signature"):
            problems.append(f"{v}: approval has neither a v2 GitHub method nor a v1 signature")
        if json.loads(data) and manifest.get("operations") != count_operations(json.loads(data)):
            problems.append(f"{v}: manifest operation count is wrong")
    if base_ref:
        problems += immutability_problems(shared_repo, base_ref, [v["version"] for v in versions], max_new_versions)
    return problems


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True)


def immutability_problems(repo: Path, base_ref: str, versions_now: list[str], max_new: int | None) -> list[str]:
    listing = _git(repo, "ls-tree", "-r", "--name-only", base_ref, "--", f"{ROOT}/versions")
    if listing.returncode != 0:
        return [f"cannot read {base_ref}: {listing.stderr.decode(errors='replace').strip()[:120]}"]
    problems, base_versions = [], set()
    for name in listing.stdout.decode().splitlines():
        base_versions.add(name.split("/")[3])
        old = _git(repo, "show", f"{base_ref}:{name}").stdout
        try:
            new = (repo / name).read_bytes()
        except OSError:
            problems.append(f"{name}: published file was deleted")
            continue
        if new != old:
            problems.append(f"{name}: published file was modified (versions are immutable)")
    added = [v for v in versions_now if v not in base_versions]
    if max_new is not None and len(added) > max_new:
        problems.append(f"{len(added)} new versions in one change (maximum {max_new})")
    return problems


# --------------------------------------------------------------------------- single-writer check (after merge)

def verify_merge(api, repo: str, sha: str) -> list[str]:
    """The commit that changed api/implemented on main must be the merge of a publisher pull request that somebody
    other than its author approved. Anything else (a direct push, e.g. by the retired publisher) is reported."""
    pulls = [p for p in api.get(f"repos/{repo}/commits/{sha}/pulls") if p.get("merged_at")]
    if not pulls:
        return [f"{sha[:12]} changed api/implemented without a merged pull request (direct push)"]
    pull = pulls[0]
    problems = []
    if not str(pull.get("head", {}).get("ref", "")).startswith("publish/"):
        problems.append(f"pull request #{pull['number']} is not a publisher branch (publish/*)")
    author = (pull.get("user") or {}).get("login", "")
    approvals = {}
    for review in api.get(f"repos/{repo}/pulls/{pull['number']}/reviews"):
        user = (review.get("user") or {}).get("login", "")
        approvals[user] = review.get("state") == "APPROVED" and review.get("author_association") in (
            "OWNER", "MEMBER", "COLLABORATOR")
    if not any(ok and user != author for user, ok in approvals.items()):
        problems.append(f"pull request #{pull['number']} has no approving review from a repository writer other "
                        f"than its author ({author})")
    return problems


# --------------------------------------------------------------------------- CLI

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    fb = sub.add_parser("fetch-build")
    fb.add_argument("--backend-repo", required=True)
    fb.add_argument("--run-id", type=int, required=True)
    fb.add_argument("--branch", default="integration/E01-FOUNDATION-SAAS")
    fb.add_argument("--out", required=True)
    pr = sub.add_parser("prepare")
    pr.add_argument("--artifact", required=True)
    pr.add_argument("--build-record", required=True)
    pr.add_argument("--commit-date", required=True)
    pr.add_argument("--shared-repo", default=".")
    pr.add_argument("--expected-repo", default="abdo-taher/capitalix")
    pr.add_argument("--allow-breaking", action="store_true")
    pr.add_argument("--allow-unknown", action="store_true")
    pr.add_argument("--scope", action="append", default=[])
    vf = sub.add_parser("verify")
    vf.add_argument("--shared-repo", default=".")
    vf.add_argument("--base-ref")
    vf.add_argument("--max-new-versions", type=int)
    vm = sub.add_parser("verify-merge")
    vm.add_argument("--repo", required=True)
    vm.add_argument("--sha", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "verify-merge":
            token = os.environ.get("GITHUB_TOKEN", "")
            if not token:
                print("publish: GITHUB_TOKEN is not set", file=sys.stderr)
                return 3
            problems = verify_merge(GitHubApi(token), args.repo, args.sha)
            for problem in problems:
                print(f"publish-verify-merge: {problem}", file=sys.stderr)
            if problems:
                return 1
            print("publish-verify-merge: the change came through an approved publisher pull request")
        elif args.command == "fetch-build":
            token = os.environ.get("PUBLISH_BACKEND_TOKEN", "")
            if not token:
                print("publish: PUBLISH_BACKEND_TOKEN is not set", file=sys.stderr)
                return 3
            openapi, record, date = verify_build(GitHubApi(token), args.backend_repo, args.run_id, args.branch)
            out = Path(args.out)
            out.mkdir(parents=True, exist_ok=True)
            (out / "openapi.json").write_bytes(openapi)
            write_json(out / "build-record.json", record)
            (out / "commit-date.txt").write_text(date + "\n")
            print(f"publish: build {args.run_id} verified: {record['commit'][:12]} sha256 {record['sha256'][:12]}")
        elif args.command == "prepare":
            version = prepare(Path(args.artifact), load_json(Path(args.build_record)), args.commit_date,
                              Path(args.shared_repo), allow_breaking=args.allow_breaking,
                              allow_unknown=args.allow_unknown, approved_scope=args.scope, repo=args.expected_repo)
            print(f"publish: prepared version {version}")
        else:
            problems = verify_tree(Path(args.shared_repo), args.base_ref, args.max_new_versions)
            for problem in problems:
                print(f"publish-verify: {problem}", file=sys.stderr)
            if problems:
                return 1
            print("publish-verify: the published tree is sound")
    except Refused as exc:
        print(f"publish: REFUSED: {exc}", file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError) as exc:
        print(f"publish: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
