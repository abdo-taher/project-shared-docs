import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "publish"))
import release_orchestrator as O  # noqa: E402


class FakeGh:
    def __init__(self, head="H2", open_prs=(), publishes=(), builds=(), build_result="success", issue=True):
        self.head, self.open_prs, self.publishes, self.builds = head, list(open_prs), list(publishes), list(builds)
        self.build_result, self.issue, self.calls, self.comments, self.next_id = build_result, issue, [], [], 500
        self.issue_numbers = [9]

    def __call__(self, a):
        self.calls.append(a)
        if a[0] == "api":
            return self.head + "\n"
        if a[:2] == ["pr", "list"]:
            return json.dumps(self.open_prs)
        if a[:2] == ["run", "list"]:
            wf = a[a.index("--workflow") + 1]
            if wf == O.PUBLISH_WORKFLOW:
                return json.dumps(self.publishes)
            return json.dumps(self.builds)
        if a[:2] == ["workflow", "run"]:
            self.next_id += 1
            run = {"databaseId": self.next_id, "url": f"https://x/run/{self.next_id}", "event": "workflow_dispatch",
                   "status": "completed", "conclusion": self.build_result, "headSha": self.head}
            (self.builds if a[2] == O.BUILD_WORKFLOW else self.publishes).append(run)
            return ""
        if a[:2] == ["run", "view"]:
            run = next(r for r in self.builds if str(r["databaseId"]) == a[2])
            return json.dumps({"status": run["status"], "conclusion": run["conclusion"], "url": run["url"]})
        if a[:2] == ["issue", "list"]:
            return json.dumps([{"number": n} for n in self.issue_numbers] if self.issue else [])
        if a[:2] == ["label", "create"]:
            return ""
        if a[:2] == ["issue", "create"]:
            self.issue = True
            return "https://github.com/x/y/issues/9\n"
        if a[:2] == ["issue", "comment"]:
            self.comments.append(a[a.index("--body") + 1])
            return ""
        raise AssertionError(a)


def orch(gh):
    return O.Orchestrator(gh, say=lambda *_: None, sleep=lambda _: None, poll=1)


def dispatched(gh, wf):
    return [c for c in gh.calls if c[:2] == ["workflow", "run"] and c[2] == wf]


class TickTests(unittest.TestCase):

    def test_new_commit_builds_then_starts_the_publisher_and_posts_the_approval_link(self):
        gh = FakeGh(builds=[{"databaseId": 1, "headSha": "H1", "status": "completed", "conclusion": "success", "url": "u"}])
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

    def test_nothing_new_does_nothing(self):
        gh = FakeGh(head="H1", builds=[{"databaseId": 1, "headSha": "H1", "status": "completed", "conclusion": "success", "url": "u"}])
        self.assertEqual(orch(gh).tick(), "up-to-date")
        self.assertEqual(dispatched(gh, O.BUILD_WORKFLOW), [])
        self.assertEqual(gh.comments, [])

    def test_a_failed_build_is_reported_once_and_not_retried_for_that_commit(self):
        gh = FakeGh(build_result="failure")
        self.assertEqual(orch(gh).tick(), "build-failed")
        self.assertEqual(dispatched(gh, O.PUBLISH_WORKFLOW), [])
        self.assertIn("Nothing was published", gh.comments[0])
        self.assertEqual(orch(gh).tick(), "up-to-date")          # the next pass leaves the same commit alone
        self.assertEqual(len(dispatched(gh, O.BUILD_WORKFLOW)), 1)

    def test_force_rebuilds_the_same_commit(self):
        gh = FakeGh(head="H1", builds=[{"databaseId": 1, "headSha": "H1", "status": "completed", "conclusion": "failure", "url": "u"}])
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

    def test_status_issue_is_created_once_when_missing(self):
        gh = FakeGh(issue=False)
        orch(gh).notify("hello")
        orch(gh).notify("again")
        self.assertEqual(sum(1 for c in gh.calls if c[:2] == ["issue", "create"]), 1)
        self.assertEqual(gh.comments, ["hello", "again"])

    def test_status_issue_exists_after_a_pass_that_does_nothing(self):
        gh = FakeGh(head="H1", issue=False, builds=[{"databaseId": 1, "headSha": "H1", "status": "completed",
                                                      "conclusion": "success", "url": "u"}])
        self.assertEqual(orch(gh).tick(), "up-to-date")
        self.assertEqual(sum(1 for c in gh.calls if c[:2] == ["issue", "create"]), 1)
        self.assertEqual(gh.comments, [])

    def test_with_duplicate_status_issues_the_oldest_is_used(self):
        gh = FakeGh()
        gh.issue_numbers = [14, 9, 12]
        orch(gh).notify("hello")
        self.assertEqual(next(c for c in gh.calls if c[:2] == ["issue", "comment"])[2], "9")

    def test_never_merges_approves_or_pushes(self):
        gh = FakeGh()
        orch(gh).tick()
        for c in gh.calls:
            self.assertNotIn(c[:2], (["pr", "merge"], ["pr", "review"]))


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
