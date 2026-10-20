import base64
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "publish"))
import release_orchestrator as O  # noqa: E402

PUBLISHED = "p" * 64


class FakeGh:
    """A small GitHub: branch heads, runs of both workflows, the status issue and its comments."""

    def __init__(self, heads=("H2",), open_prs=(), publishes=(), builds=(), build_result="success", issue=True,
                 built_sha256="b" * 64, published_sha256=PUBLISHED, fail_on=None):
        self.heads, self.open_prs, self.publishes, self.builds = list(heads), list(open_prs), list(publishes), list(builds)
        self.build_result, self.issue, self.fail_on = build_result, issue, fail_on
        self.built_sha256, self.published_sha256 = built_sha256, published_sha256
        self.calls, self.comments, self.next_id, self.issue_numbers = [], [], 500, [9]
        self.created_issues = 0

    @property
    def head(self):
        return self.heads[0]

    def __call__(self, a):
        self.calls.append(a)
        if self.fail_on and a[:2] == self.fail_on:
            raise O.Failed("boom")
        if a[0] == "api" and "/commits/" in a[1]:
            return (self.heads[0] if len(self.heads) == 1 else self.heads.pop(0)) + "\n"
        if a[0] == "api" and a[1].endswith("current.json"):
            return json.dumps({"content": base64.b64encode(json.dumps({"sha256": self.published_sha256}).encode()).decode()})
        if a[:2] == ["pr", "list"]:
            return json.dumps(self.open_prs)
        if a[:2] == ["run", "list"]:
            wf = a[a.index("--workflow") + 1]
            return json.dumps(self.publishes if wf == O.PUBLISH_WORKFLOW else self.builds)
        if a[:2] == ["workflow", "run"]:
            self.next_id += 1
            run = {"databaseId": self.next_id, "url": f"https://x/run/{self.next_id}", "event": "workflow_dispatch",
                   "status": "completed", "conclusion": self.build_result, "headSha": self.head, "args": a}
            if a[2] == O.PUBLISH_WORKFLOW:                      # a real publish run waits for the owner's approval
                run.update(status="waiting", conclusion="")
            (self.builds if a[2] == O.BUILD_WORKFLOW else self.publishes).append(run)
            return ""
        if a[:2] == ["run", "view"]:
            run = next(r for r in self.builds if str(r["databaseId"]) == a[2])
            return json.dumps({"status": run["status"], "conclusion": run["conclusion"], "url": run["url"]})
        if a[:2] == ["run", "download"]:
            Path(a[a.index("-D") + 1], "build-record.json").write_text(json.dumps({"sha256": self.built_sha256}))
            return ""
        if a[:2] == ["issue", "list"]:
            return json.dumps([{"number": n} for n in self.issue_numbers] if self.issue else [])
        if a[:2] == ["label", "create"]:
            return ""
        if a[:2] == ["issue", "create"]:
            self.issue, self.created_issues = True, self.created_issues + 1
            return "https://github.com/x/y/issues/9\n"
        if a[:2] == ["issue", "view"]:
            return json.dumps({"comments": [{"body": c} for c in self.comments]})
        if a[:2] == ["issue", "comment"]:
            self.comments.append(a[a.index("--body") + 1])
            return ""
        raise AssertionError(a)


def orch(gh, **kw):
    return O.Orchestrator(gh, say=lambda *_: None, sleep=lambda _: None, poll=1, **kw)


def dispatched(gh, wf):
    return [c for c in gh.calls if c[:2] == ["workflow", "run"] and c[2] == wf]


BUILT_H1 = {"databaseId": 1, "headSha": "H1", "status": "completed", "conclusion": "success", "url": "u"}


class TickTests(unittest.TestCase):

    def test_new_commit_builds_then_starts_the_publisher_and_posts_the_approval_link(self):
        gh = FakeGh(builds=[dict(BUILT_H1)])
        self.assertEqual(orch(gh).tick(), "publish-started")
        self.assertEqual(len(dispatched(gh, O.BUILD_WORKFLOW)), 1)
        publish = dispatched(gh, O.PUBLISH_WORKFLOW)[0]
        self.assertIn("build_run_id=501", publish)
        self.assertIn("ACTION NEEDED", gh.comments[0])
        self.assertIn("https://x/run/502", gh.comments[0])
        self.assertIn("Review deployments", gh.comments[0])

    def test_never_accepts_incompatible_changes_by_itself(self):
        gh = FakeGh()
        orch(gh).tick()
        publish = " ".join(dispatched(gh, O.PUBLISH_WORKFLOW)[0])
        self.assertNotIn("allow_breaking", publish)
        self.assertNotIn("allow_unknown", publish)
        self.assertEqual([x for x in dispatched(gh, O.PUBLISH_WORKFLOW)[0] if x.startswith("-")], ["-R", "-f"])

    def test_nothing_new_does_nothing(self):
        gh = FakeGh(heads=("H1",), builds=[dict(BUILT_H1)])
        self.assertEqual(orch(gh).tick(), "up-to-date")
        self.assertEqual(dispatched(gh, O.BUILD_WORKFLOW), [])
        self.assertEqual(gh.comments, [])

    def test_the_same_commit_is_never_built_twice_even_by_repeated_triggers(self):
        gh = FakeGh(heads=("H2",))
        self.assertEqual(orch(gh).tick(pushed="H2"), "publish-started")
        gh.publishes[0]["status"] = "completed"                     # the owner resolved the approval
        self.assertEqual(orch(gh).tick(pushed="H2"), "up-to-date")
        self.assertEqual(orch(gh).tick(pushed="H2"), "up-to-date")
        self.assertEqual(len(dispatched(gh, O.BUILD_WORKFLOW)), 1)

    def test_a_failed_build_is_reported_once_and_not_retried_for_that_commit(self):
        gh = FakeGh(build_result="failure")
        self.assertEqual(orch(gh).tick(), "build-failed")
        self.assertEqual(dispatched(gh, O.PUBLISH_WORKFLOW), [])
        self.assertIn("Nothing was published", gh.comments[0])
        self.assertEqual(orch(gh).tick(), "up-to-date")
        self.assertEqual(len(dispatched(gh, O.BUILD_WORKFLOW)), 1)

    def test_force_rebuilds_the_same_commit(self):
        gh = FakeGh(heads=("H1",), builds=[dict(BUILT_H1, conclusion="failure")])
        self.assertEqual(orch(gh).tick(force=True), "publish-started")

    def test_waits_while_a_publication_pr_is_open(self):
        gh = FakeGh(open_prs=[{"number": 3, "url": "https://x/pull/3"}])
        self.assertEqual(orch(gh).tick(), "waiting-for-merge")
        self.assertEqual(dispatched(gh, O.BUILD_WORKFLOW), [])

    def test_waits_while_a_publish_run_waits_for_approval(self):
        gh = FakeGh(publishes=[{"databaseId": 7, "status": "waiting", "url": "u"}])
        self.assertEqual(orch(gh).tick(), "publish-in-flight")
        self.assertEqual(dispatched(gh, O.BUILD_WORKFLOW), [])

    def test_waits_while_a_build_is_running(self):
        gh = FakeGh(builds=[{"databaseId": 1, "headSha": "H0", "status": "in_progress", "conclusion": "", "url": "u"}])
        self.assertEqual(orch(gh).tick(), "build-in-flight")

    def test_a_contract_identical_to_the_published_one_asks_for_no_approval(self):
        gh = FakeGh(built_sha256=PUBLISHED)
        self.assertEqual(orch(gh).tick(), "no-contract-change")
        self.assertEqual(dispatched(gh, O.PUBLISH_WORKFLOW), [])
        self.assertEqual(gh.comments, [])

    def test_if_the_digests_cannot_be_compared_the_owner_is_asked(self):
        gh = FakeGh(fail_on=["run", "download"])
        self.assertEqual(orch(gh).tick(), "publish-started")

    def test_never_merges_approves_or_pushes(self):
        gh = FakeGh()
        orch(gh).tick()
        for c in gh.calls:
            self.assertNotIn(c[:2], (["pr", "merge"], ["pr", "review"]))


class QuickPushesTests(unittest.TestCase):

    def test_several_quick_pushes_become_one_build_of_the_latest_head(self):
        gh = FakeGh(heads=("A", "B", "C", "C", "C", "C", "C", "C", "C"))
        self.assertEqual(orch(gh).tick(pushed="A", settle=10), "publish-started")
        builds = dispatched(gh, O.BUILD_WORKFLOW)
        self.assertEqual(len(builds), 1)
        self.assertEqual(next(r for r in gh.builds)["headSha"], "C")

    def test_a_trigger_for_an_older_push_releases_the_latest_head_only(self):
        said = []
        gh = FakeGh(heads=("NEW",))
        o = O.Orchestrator(gh, say=said.append, sleep=lambda _: None, poll=1)
        o.tick(pushed="OLD1234567890")
        self.assertTrue(any("not the head any more" in m for m in said))

    def test_two_triggers_one_after_the_other_make_one_build(self):
        # the workflow's concurrency group runs passes one at a time; the second finds the first one's work
        gh = FakeGh(heads=("H9",))
        first = orch(gh).tick(pushed="H9", settle=0)
        second = orch(gh).tick(pushed="H9", settle=0)
        self.assertEqual((first, second), ("publish-started", "publish-in-flight"))
        self.assertEqual(len(dispatched(gh, O.BUILD_WORKFLOW)), 1)
        self.assertEqual(len(dispatched(gh, O.PUBLISH_WORKFLOW)), 1)


class BranchTests(unittest.TestCase):

    def test_only_the_development_branch_or_a_test_branch_can_be_released(self):
        for bad in ("main", "feature/x", "test/other", "test/release"):
            with self.assertRaises(O.Failed):
                orch(FakeGh()).tick(branch=bad)
        gh = FakeGh()
        orch(gh).tick(branch="test/release-abc")
        self.assertIn("test/release-abc", dispatched(gh, O.BUILD_WORKFLOW)[0])


class StatusIssueTests(unittest.TestCase):

    def test_status_issue_is_created_once_when_missing(self):
        gh = FakeGh(issue=False)
        orch(gh).notify("hello")
        orch(gh).notify("again")
        self.assertEqual(gh.created_issues, 1)
        self.assertEqual(gh.comments, ["hello", "again"])

    def test_status_issue_exists_after_a_pass_that_does_nothing(self):
        gh = FakeGh(heads=("H1",), issue=False, builds=[dict(BUILT_H1)])
        self.assertEqual(orch(gh).tick(), "up-to-date")
        self.assertEqual(gh.created_issues, 1)
        self.assertEqual(gh.comments, [])

    def test_with_duplicate_status_issues_the_oldest_is_used(self):
        gh = FakeGh()
        gh.issue_numbers = [14, 9, 12]
        orch(gh).notify("hello")
        self.assertEqual(next(c for c in gh.calls if c[:2] == ["issue", "comment"])[2], "9")

    def test_notify_once_does_not_repeat_the_same_fault(self):
        gh = FakeGh()
        o = orch(gh)
        self.assertTrue(o.notify_once("backend-token", "cannot create token"))
        self.assertFalse(o.notify_once("backend-token", "cannot create token"))
        self.assertFalse(o.notify_once("backend-token", "cannot create token"))
        self.assertEqual(len(gh.comments), 1)
        o.notify("something else happened")                      # a later event resets it
        self.assertTrue(o.notify_once("backend-token", "cannot create token"))
        self.assertEqual(len(gh.comments), 3)


class QuietFailureTests(unittest.TestCase):

    def run_main(self, gh, argv):
        import subprocess
        real_gh, real_orch = O.make_gh, O.Orchestrator
        O.make_gh = lambda shared, backend: gh
        O.Orchestrator = lambda g, **kw: real_orch(g, say=lambda *_: None, sleep=lambda _: None, poll=1)
        import os
        os.environ["GH_TOKEN"] = "t"
        try:
            return O.main(argv)
        finally:
            O.make_gh, O.Orchestrator = real_gh, real_orch
            os.environ.pop("GH_TOKEN", None)

    def test_a_fault_in_a_pass_ends_quietly_and_is_reported_once(self):
        gh = FakeGh(fail_on=["workflow", "run"])
        self.assertEqual(self.run_main(gh, ["tick"]), 0)
        self.assertEqual(self.run_main(gh, ["tick"]), 0)
        self.assertEqual(self.run_main(gh, ["tick"]), 0)
        faults = [c for c in gh.comments if "could not run" in c]
        self.assertEqual(len(faults), 1)

    def test_a_refused_branch_is_quiet_too(self):
        self.assertEqual(self.run_main(FakeGh(), ["tick", "--branch", "main"]), 0)


class TokenRoutingTests(unittest.TestCase):
    def test_each_repository_gets_its_own_token(self):
        seen = []
        import subprocess
        real = subprocess.run

        def fake(cmd, **kw):
            seen.append((cmd[1:3], kw["env"]["GH_TOKEN"]))
            return subprocess.CompletedProcess(cmd, 0, "", "")
        subprocess.run = fake
        try:
            gh = O.make_gh("shared-tok", "backend-tok")
            gh(["run", "list", "-R", O.BACKEND_REPO])
            gh(["run", "list", "-R", O.SHARED_REPO])
            gh(["api", f"repos/{O.BACKEND_REPO}/commits/x"])
        finally:
            subprocess.run = real
        self.assertEqual([t for _, t in seen], ["backend-tok", "shared-tok", "backend-tok"])


if __name__ == "__main__":
    unittest.main()
