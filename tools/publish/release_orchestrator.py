#!/usr/bin/env python3
"""GitHub-side orchestrator of the contract release (runs in the `contract-release` workflow, no operator machine).

    release_orchestrator.py tick          # one stateless pass: is there a new backend commit to release?
    release_orchestrator.py notify TEXT   # post TEXT to the release status issue

A pass never waits for a person and never approves or merges. It looks at GitHub and does at most the next step:

  1. a publication pull request is open        -> nothing (waiting for the owner's merge)
  2. a publish run is queued/waiting/running   -> nothing (waiting for the owner's deployment approval)
  3. the branch head already has a build       -> nothing (a failed or refused commit is not retried; push again)
  4. otherwise: build the head, wait for it; if the built contract is byte-identical to the published one there is
     nothing to publish, otherwise dispatch the publisher with that run id and post the approval link

A pass is started by the 10-minute schedule and, immediately, by the `contract-release-trigger` workflow of the backend
after a push. It always releases the CURRENT head of the branch (several quick pushes collapse into one build: with
--settle it waits until the head has been still for that long), and the workflow's concurrency group allows only one
pass at a time, so a trigger that arrives during a pass finds the build or the pending approval and does nothing.
Failures are reported once to the status issue and end the pass quietly, so a persistent fault cannot email the owner
every ten minutes.

Each later hand-off (approve the deployment, review and merge the PR, published) is reported by the workflow that
reaches it with `notify`, so the owner gets one GitHub notification per action with the link in it. The publisher is
always dispatched WITHOUT allow_breaking / allow_unknown: accepting incompatible changes stays a manual owner decision.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SHARED_REPO = "abdo-taher/project-shared-docs"
BACKEND_REPO = "abdo-taher/capitalix"
BRANCH = "integration/E01-FOUNDATION-SAAS"
BUILD_WORKFLOW = "contract-build.yml"
PUBLISH_WORKFLOW = "contract-publish.yml"
TEST_BRANCH_PREFIX = "test/release-"   # throwaway branches used to test the pipeline end to end
STATUS_LABEL = "contract-release"
STATUS_TITLE = "Contract release status"
ACTIVE = {"queued", "in_progress", "waiting", "requested", "pending"}


class Failed(Exception):
    pass


def make_gh(shared_token: str, backend_token: str):
    """`gh` with the right token for the repository named by -R (each token is limited to one repository)."""
    def gh(args: list[str]) -> str:
        repo = args[args.index("-R") + 1] if "-R" in args else None
        if "api" == args[0]:
            repo = args[1].split("/")[1:3]
            repo = "/".join(repo) if len(repo) == 2 else None
        token = backend_token if repo == BACKEND_REPO else shared_token
        proc = subprocess.run(["gh", *args], capture_output=True, text=True, env={**os.environ, "GH_TOKEN": token})
        if proc.returncode != 0:
            raise Failed(f"gh {' '.join(args[:3])}: {(proc.stderr or proc.stdout).strip()[:300]}")
        return proc.stdout
    return gh


class Orchestrator:
    def __init__(self, gh, say=print, sleep=time.sleep, poll: int = 15, build_timeout: int = 1800, settle_poll: int = 5):
        self.gh, self.say, self.sleep, self.poll, self.build_timeout = gh, say, sleep, poll, build_timeout
        self.settle_poll = settle_poll

    def json(self, args):
        out = self.gh(args)
        return json.loads(out) if out.strip() else None

    # -- the status issue --------------------------------------------------------------------------------------
    def status_issue(self) -> str:
        """Number of the one status issue; created if missing. With duplicates the oldest is used."""
        rows = self.json(["issue", "list", "-R", SHARED_REPO, "--label", STATUS_LABEL, "--state", "open",
                          "--json", "number"]) or []
        if rows:
            return str(min(r["number"] for r in rows))
        self.gh(["label", "create", STATUS_LABEL, "-R", SHARED_REPO, "--force",
                 "--description", "Contract release status (written by automation)"])
        url = self.gh(["issue", "create", "-R", SHARED_REPO, "--title", STATUS_TITLE, "--label", STATUS_LABEL,
                       "--body", "Every step of the automatic contract release that needs you, or finishes, is "
                                 "posted here with its link. Subscribe to this issue to be notified."]).strip()
        return url.rsplit("/", 1)[-1]

    def notify(self, text: str) -> None:
        self.gh(["issue", "comment", self.status_issue(), "-R", SHARED_REPO, "--body", text])
        self.say(f"notified: {text.splitlines()[0]}")

    def notify_once(self, key: str, text: str) -> bool:
        """Post `text` unless the newest comment already carries the same key (a persistent fault is reported once)."""
        marker = f"<!-- release-key:{key} -->"
        number = self.status_issue()
        comments = (self.json(["issue", "view", number, "-R", SHARED_REPO, "--json", "comments"]) or {}).get("comments", [])
        if comments and marker in (comments[-1].get("body") or ""):
            self.say(f"already reported ({key}); not repeating")
            return False
        self.gh(["issue", "comment", number, "-R", SHARED_REPO, "--body", f"{text}\n\n{marker}"])
        self.say(f"notified once: {text.splitlines()[0]}")
        return True

    # -- one pass ----------------------------------------------------------------------------------------------
    def new_run(self, repo: str, workflow: str, before: set) -> dict:
        deadline = 0
        while deadline < 20:
            rows = self.json(["run", "list", "-R", repo, "--workflow", workflow, "-L", "10", "--json",
                              "databaseId,url,event"]) or []
            fresh = [r for r in rows if r["databaseId"] not in before and r["event"] == "workflow_dispatch"]
            if fresh:
                return fresh[0]
            deadline += 1
            self.sleep(3)
        raise Failed(f"{workflow} did not start")

    def run_ids(self, repo: str, workflow: str) -> set:
        return {r["databaseId"] for r in
                self.json(["run", "list", "-R", repo, "--workflow", workflow, "-L", "30", "--json", "databaseId"]) or []}

    def head(self, branch: str) -> str:
        return self.gh(["api", f"repos/{BACKEND_REPO}/commits/{branch}", "--jq", ".sha"]).strip()

    def settled_head(self, branch: str, settle: int) -> str:
        """The branch head once it has not moved for `settle` seconds (quick successive pushes become one release)."""
        head, still = self.head(branch), 0
        while still < settle:
            self.sleep(self.settle_poll)
            latest = self.head(branch)
            head, still = (latest, 0) if latest != head else (head, still + self.settle_poll)
        return head

    def published_digest(self) -> str | None:
        try:
            raw = self.json(["api", f"repos/{SHARED_REPO}/contents/api/implemented/current.json"])
            return json.loads(base64.b64decode(raw["content"])).get("sha256")
        except (Failed, KeyError, ValueError):
            return None

    def built_digest(self, run_id: int) -> str | None:
        try:
            with tempfile.TemporaryDirectory() as tmp:
                self.gh(["run", "download", str(run_id), "-R", BACKEND_REPO, "-n", "contract-build", "-D", tmp])
                return json.loads((Path(tmp) / "build-record.json").read_text()).get("sha256")
        except (Failed, OSError, ValueError):
            return None

    def tick(self, force: bool = False, branch: str = BRANCH, settle: int = 0, pushed: str | None = None) -> str:
        if branch != BRANCH and not branch.startswith(TEST_BRANCH_PREFIX):
            raise Failed(f"refusing to release branch {branch!r}: only {BRANCH} (or {TEST_BRANCH_PREFIX}* for tests)")
        self.status_issue()   # exists from the first pass on, so the owner can subscribe before the first action
        head = self.settled_head(branch, settle)
        if pushed and not head.startswith(pushed[:12]):
            self.say(f"push {pushed[:12]} is not the head any more; releasing the latest, {head[:12]}")

        open_prs = self.json(["pr", "list", "-R", SHARED_REPO, "--state", "open", "--search", "publish contract in:title",
                              "--json", "number,url"]) or []
        if open_prs:
            self.say(f"waiting for the owner to merge {open_prs[0]['url']}")
            return "waiting-for-merge"

        publishes = self.json(["run", "list", "-R", SHARED_REPO, "--workflow", PUBLISH_WORKFLOW, "-L", "10", "--json",
                               "databaseId,status,url"]) or []
        if any(r["status"] in ACTIVE for r in publishes):
            self.say("a publish run is waiting for approval or still running")
            return "publish-in-flight"

        builds = self.json(["run", "list", "-R", BACKEND_REPO, "--workflow", BUILD_WORKFLOW, "-L", "50", "--json",
                            "databaseId,headSha,status,conclusion,url"]) or []
        if any(b["status"] in ACTIVE for b in builds):
            self.say("a build is still running")
            return "build-in-flight"
        if not force and any(b["headSha"] == head for b in builds):
            self.say(f"{head[:12]} was already built; nothing new")
            return "up-to-date"

        self.say(f"new backend commit {head[:12]} on {branch}: building")
        before = self.run_ids(BACKEND_REPO, BUILD_WORKFLOW)
        self.gh(["workflow", "run", BUILD_WORKFLOW, "-R", BACKEND_REPO, "--ref", branch])
        build = self.new_run(BACKEND_REPO, BUILD_WORKFLOW, before)
        waited = 0
        while True:
            row = self.json(["run", "view", str(build["databaseId"]), "-R", BACKEND_REPO, "--json",
                             "status,conclusion,url"])
            if row["status"] == "completed":
                break
            if waited > self.build_timeout:
                self.notify(f"Build of `{head[:12]}` did not finish in {self.build_timeout // 60} minutes: {build['url']}\n"
                            "Nothing was published.")
                return "build-timeout"
            self.sleep(self.poll)
            waited += self.poll
        if row["conclusion"] != "success":
            self.notify(f"Build of `{head[:12]}` ended `{row['conclusion']}`: {build['url']}\n"
                        "Nothing was published. It will not be retried for this commit; push a fix or run "
                        "`contract-release` with force.")
            return "build-failed"

        built = self.built_digest(build["databaseId"])
        if built and built == self.published_digest():
            self.say(f"{head[:12]} built; its contract is byte-identical to the published one: nothing to publish")
            return "no-contract-change"

        before = self.run_ids(SHARED_REPO, PUBLISH_WORKFLOW)
        self.say(f"dispatching {PUBLISH_WORKFLOW} with build_run_id={build['databaseId']} only "
                 "(allow_breaking and allow_unknown are never sent)")
        self.gh(["workflow", "run", PUBLISH_WORKFLOW, "-R", SHARED_REPO, "-f", f"build_run_id={build['databaseId']}"])
        publish = self.new_run(SHARED_REPO, PUBLISH_WORKFLOW, before)
        self.notify(f"**ACTION NEEDED — approve the deployment** (build `{head[:12]}` succeeded, run {build['databaseId']}):\n"
                    f"{publish['url']}\n\n"
                    "Open the link, click **Review deployments**, tick `contract-publisher`, **Approve and deploy**. "
                    "After that I open the publication pull request and post its link here.\n"
                    "Do not approve if you already know the contract still has breaking or unclassified changes: the "
                    "publisher will refuse it. Cancel the run instead.")
        return "publish-started"


QUIET = {"up-to-date", "waiting-for-merge", "publish-in-flight", "build-in-flight", "publish-started",
         "no-contract-change"}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)
    tick = sub.add_parser("tick")
    tick.add_argument("--force", action="store_true", help="release the head even if it was built before")
    tick.add_argument("--branch", default=BRANCH, help=f"{BRANCH} (default) or a {TEST_BRANCH_PREFIX}* test branch")
    tick.add_argument("--settle", type=int, default=0, help="wait until the head has been still for this many seconds")
    tick.add_argument("--pushed", default="", help="commit whose push started this pass (informational)")
    note = sub.add_parser("notify")
    note.add_argument("text")
    once = sub.add_parser("notify-once")
    once.add_argument("--key", required=True)
    once.add_argument("text")
    args = ap.parse_args(argv)
    shared = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not shared:
        print("release: GH_TOKEN is not set", file=sys.stderr)
        return 3
    backend = os.environ.get("BACKEND_GH_TOKEN", shared)
    orchestrator = Orchestrator(make_gh(shared, backend))
    try:
        if args.command == "notify":
            orchestrator.notify(args.text)
            return 0
        if args.command == "notify-once":
            orchestrator.notify_once(args.key, args.text)
            return 0
        outcome = orchestrator.tick(force=args.force, branch=args.branch, settle=args.settle, pushed=args.pushed or None)
        print(f"release: {outcome}")
        return 0 if outcome in QUIET else 1     # a failed or timed-out build ends red once; the commit is not retried
    except Failed as exc:
        # A fault must not turn every scheduled pass red: say it once on the status issue and end quietly.
        print(f"::warning::release: {exc}")
        if args.command == "tick":
            try:
                orchestrator.notify_once("tick-error", f"**The release pass could not run:** {exc}\n"
                                                       "Nothing was published. This is reported once; it will be "
                                                       "retried by the next scheduled pass.")
            except Failed as inner:
                print(f"::warning::release: could not post the status comment either: {inner}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
