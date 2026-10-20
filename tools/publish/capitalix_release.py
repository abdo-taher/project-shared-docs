#!/usr/bin/env python3
"""One command for the whole GitHub-only contract release.

    python3 tools/publish/capitalix_release.py            # build -> publish PR -> wait for merge

It drives the two workflows through the operator's own `gh` login: build in the backend repository, dispatch the
publisher with that run id, then wait. Wherever a person must act it prints the link and keeps waiting:

  * approving the deployment of environment `contract-publisher`  (a run link)
  * reviewing and merging the publication pull request             (a PR link)

It never approves or merges anything. The publication flag is switched on for the duration and restored on exit
(also on failure or Ctrl-C). The publisher's own gates (compatibility, provenance, immutability) are unchanged:
if one of them refuses, the reason from the run log is printed and the command exits non-zero.
"""

from __future__ import annotations

import argparse
import base64
import json
import subprocess
import sys
import time

SHARED_REPO = "abdo-taher/project-shared-docs"
BACKEND_REPO = "abdo-taher/capitalix"
BACKEND_REF = "integration/E01-FOUNDATION-SAAS"
FLAG = "API_CONTRACT_PUBLICATION_ENABLED"
BUILD_WORKFLOW = "contract-build.yml"
PUBLISH_WORKFLOW = "contract-publish.yml"
DONE = {"completed"}


class Stop(Exception):
    def __init__(self, message: str, code: int = 1):
        super().__init__(message)
        self.code = code


def run_gh(args: list[str]) -> str:
    proc = subprocess.run(["gh", *args], capture_output=True, text=True)
    if proc.returncode != 0:
        raise Stop(f"gh {' '.join(args[:3])} failed: {(proc.stderr or proc.stdout).strip()[:400]}", 2)
    return proc.stdout


class Release:
    def __init__(self, gh=run_gh, sleep=time.sleep, now=time.monotonic, say=print,
                 poll: int = 10, timeout_minutes: int = 120):
        self.gh, self.sleep, self.now, self.say = gh, sleep, now, say
        self.poll, self.deadline_s = poll, timeout_minutes * 60
        self.started = now()

    # -- helpers -----------------------------------------------------------------------------------------------
    def json(self, args: list[str]):
        out = self.gh(args)
        return json.loads(out) if out.strip() else None

    def wait_for(self, what: str, probe, announce=None):
        """Poll `probe()` until it returns a truthy value; `announce(state)` is called once per distinct state."""
        last = None
        while True:
            value = probe()
            if value:
                return value
            if announce:
                last = announce(last)
            if self.now() - self.started > self.deadline_s:
                raise Stop(f"timed out waiting for {what}", 4)
            self.sleep(self.poll)

    def run_ids(self, repo: str, workflow: str) -> set[int]:
        rows = self.json(["run", "list", "-R", repo, "--workflow", workflow, "-L", "30", "--json", "databaseId"]) or []
        return {r["databaseId"] for r in rows}

    def dispatch(self, repo: str, workflow: str, fields: dict[str, str], ref: str | None = None) -> dict:
        before = self.run_ids(repo, workflow)
        cmd = ["workflow", "run", workflow, "-R", repo]
        if ref:
            cmd += ["--ref", ref]
        for key, value in fields.items():
            cmd += ["-f", f"{key}={value}"]
        self.gh(cmd)

        def find():
            rows = self.json(["run", "list", "-R", repo, "--workflow", workflow, "-L", "10", "--json",
                              "databaseId,url,status,conclusion,event"]) or []
            fresh = [r for r in rows if r["databaseId"] not in before and r.get("event") == "workflow_dispatch"]
            return fresh[0] if fresh else None
        return self.wait_for(f"{workflow} to start", find)

    def reason(self, repo: str, run_id: int) -> str:
        try:
            log = self.gh(["run", "view", str(run_id), "-R", repo, "--log-failed"])
        except Stop:
            return "(log not available)"
        keep = [ln.split("Z ", 1)[-1] for ln in log.splitlines()
                if any(k in ln for k in ("publish:", "ERROR", "Error:", "REFUSED", "refus"))]
        return "\n    ".join(keep[-8:]) or "(see the run page)"

    def finish_run(self, repo: str, run: dict, label: str, human_gate: str | None = None) -> dict:
        run_id = run["databaseId"]
        self.say(f"  {label}: {run['url']}")

        seen = {}

        def probe():
            row = self.json(["run", "view", str(run_id), "-R", repo, "--json", "status,conclusion,url"])
            seen["status"] = row["status"]
            return row if row["status"] in DONE else None

        def announce(last):
            state = seen["status"]
            if state != last:
                if state == "waiting" and human_gate:
                    self.say(f"\n  ACTION NEEDED — {human_gate}\n    {run['url']}\n    (waiting for you...)\n")
                else:
                    self.say(f"  ... {state}")
            return state
        row = self.wait_for(label, probe, announce)
        if row["conclusion"] != "success":
            raise Stop(f"{label} ended '{row['conclusion']}'.\n  Why:\n    {self.reason(repo, run_id)}\n  {run['url']}", 3)
        self.say(f"  {label}: success")
        return row

    def find_pr(self, since_ids: set[int]) -> dict:
        def probe():
            rows = self.json(["pr", "list", "-R", SHARED_REPO, "--state", "all", "--search",
                              "publish contract in:title", "--json", "number,url,headRefName,state"]) or []
            fresh = [r for r in rows if r["number"] not in since_ids and r["headRefName"].startswith("publish/")]
            return fresh[0] if fresh else None
        return self.wait_for("the publication pull request", probe)

    def pr_numbers(self) -> set[int]:
        rows = self.json(["pr", "list", "-R", SHARED_REPO, "--state", "all", "--search",
                          "publish contract in:title", "--json", "number"]) or []
        return {r["number"] for r in rows}

    def current_version(self) -> str:
        raw = self.json(["api", f"repos/{SHARED_REPO}/contents/api/implemented/current.json"])
        return json.loads(base64.b64decode(raw["content"]))["version"]

    # -- the cycle ---------------------------------------------------------------------------------------------
    def execute(self, args) -> int:
        previous = None
        try:
            previous = (self.gh(["variable", "get", FLAG, "-R", SHARED_REPO]).strip() or "false")
        except Stop:
            previous = "false"
        self.gh(["variable", "set", FLAG, "--body", "true", "-R", SHARED_REPO])
        self.say(f"Publication enabled for this run (was '{previous}'; restored on exit).")
        try:
            return self._cycle(args)
        except Stop as stop:
            self.say(f"\nSTOPPED: {stop}")
            return stop.code
        except KeyboardInterrupt:
            self.say("\nInterrupted. Nothing was published or merged by this command.")
            return 130
        finally:
            try:
                self.gh(["variable", "set", FLAG, "--body", previous, "-R", SHARED_REPO])
                self.say(f"Publication flag restored to '{previous}'.")
            except Stop as stop:
                self.say(f"WARNING: could not restore {FLAG}: {stop} — run: gh variable set {FLAG} --body {previous} -R {SHARED_REPO}")

    def _cycle(self, args) -> int:
        if args.build_run_id:
            build_id = args.build_run_id
            self.say(f"\n[1/3] Using existing build run {build_id}")
        else:
            self.say(f"\n[1/3] Build the contract ({BACKEND_REPO}@{args.ref})")
            run = self.dispatch(BACKEND_REPO, BUILD_WORKFLOW, {}, ref=args.ref)
            self.finish_run(BACKEND_REPO, run, "contract-build")
            build_id = run["databaseId"]

        self.say("\n[2/3] Verify and prepare the publication (compatibility, provenance, immutability)")
        before = self.pr_numbers()
        fields = {"build_run_id": str(build_id)}
        if args.allow_breaking:
            fields["allow_breaking"] = "true"
        if args.allow_unknown:
            fields["allow_unknown"] = "true"
        if args.scope:
            fields["scope"] = args.scope
        run = self.dispatch(SHARED_REPO, PUBLISH_WORKFLOW, fields)
        self.finish_run(SHARED_REPO, run, "contract-publish",
                        human_gate="open the link, click 'Review deployments', tick contract-publisher, 'Approve and deploy'")

        self.say("\n[3/3] Review and merge the publication pull request")
        pr = self.find_pr(before)
        self.say(f"\n  ACTION NEEDED — review the files, then approve and merge:\n    {pr['url']}\n    (waiting for the merge...)\n")

        def merged():
            row = self.json(["pr", "view", str(pr["number"]), "-R", SHARED_REPO, "--json", "state,mergedAt"])
            if row["state"] == "CLOSED":
                raise Stop(f"PR #{pr['number']} was closed without merging; nothing is published.", 5)
            return row if row["state"] == "MERGED" else None
        self.wait_for(f"PR #{pr['number']} to be merged", merged)
        self.say(f"\nPublished. current.json now points to: {self.current_version()}")
        self.say("Front ends upgrade with: python3 tools/capitalix_contract.py update   (then re-run their tests)")
        return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ref", default=BACKEND_REF, help="backend branch to build (default: %(default)s)")
    ap.add_argument("--build-run-id", help="skip the build and publish this existing contract-build run")
    ap.add_argument("--allow-breaking", action="store_true", help="owner decision: accept BREAKING changes (recorded)")
    ap.add_argument("--allow-unknown", action="store_true", help="owner decision: accept unclassified changes (recorded)")
    ap.add_argument("--scope", default="", help="text naming the accepted changes (recorded in the approval)")
    ap.add_argument("--poll", type=int, default=10, help="seconds between status checks")
    ap.add_argument("--timeout-minutes", type=int, default=120, help="give up waiting after this long")
    args = ap.parse_args(argv)
    if args.build_run_id and not args.build_run_id.isdigit():
        ap.error("--build-run-id must be digits")
    return Release(poll=args.poll, timeout_minutes=args.timeout_minutes).execute(args)


if __name__ == "__main__":
    sys.exit(main())
