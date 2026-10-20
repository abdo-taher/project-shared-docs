import base64
import json
import sys
import types
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "publish"))
import capitalix_release as R  # noqa: E402


class FakeGh:
    """Scripted GitHub: dispatching a workflow creates a run that advances through `states`."""

    def __init__(self, build=("completed/success",), publish=("waiting", "completed/success"), pr_states=("OPEN", "MERGED"),
                 variable="false", heads=("A",), preopen=0):
        self.calls, self.variable = [], variable
        self.heads, self.preopen, self.pr_no, self.last_pr = list(heads), preopen, 6, "OPEN"
        self.head_calls = 0
        self.script = {"contract-build.yml": list(build), "contract-publish.yml": list(publish)}
        self.runs, self.next_id, self.pr_states, self.pr_made = {}, 100, list(pr_states), False
        self.version = "2026.10.20-aaaaaaaaaaaa"

    def __call__(self, a):
        self.calls.append(a)
        if a[:2] == ["variable", "get"]:
            if self.variable is None:
                raise R.Stop("not found", 2)
            return self.variable
        if a[:2] == ["variable", "set"]:
            self.variable = a[a.index("--body") + 1]
            return ""
        if a[:2] == ["workflow", "run"]:
            self.next_id += 1
            wf = a[2]
            self.runs[self.next_id] = {"wf": wf, "steps": list(self.script[wf]), "inputs": a, "sha": self.heads[0]}
            if wf == "contract-publish.yml" and self.script[wf][-1].endswith("success"):
                self.pr_made, self.pr_no, self.last_pr = True, self.pr_no + 1, "OPEN"
            return ""
        if a[:2] == ["run", "list"]:
            wf = a[a.index("--workflow") + 1]
            return json.dumps([{"databaseId": i, "url": f"https://x/run/{i}", "status": "queued", "conclusion": "",
                                "event": "workflow_dispatch"} for i, r in self.runs.items() if r["wf"] == wf])
        if a[:2] == ["run", "view"] and "--log-failed" in a:
            return "job\tstep\t2026-10-20T15:00:52.1Z publish: REFUSED: 215 unclassified change(s)\n"
        if a[:2] == ["run", "view"]:
            run = self.runs[int(a[2])]
            state = run["steps"][0] if len(run["steps"]) == 1 else run["steps"].pop(0)
            status, _, concl = state.partition("/")
            return json.dumps({"status": status, "conclusion": concl, "url": f"https://x/run/{a[2]}",
                               "headSha": run["sha"]})
        if a[:2] == ["pr", "list"]:
            if a[a.index("--state") + 1] == "open":
                if self.preopen > 0:
                    self.preopen -= 1
                    return json.dumps([{"number": 3, "url": "https://x/pull/3", "headRefName": "publish/old"}])
                return json.dumps([{"number": self.pr_no, "url": f"https://x/pull/{self.pr_no}", "headRefName": "publish/v"}]
                                  if self.pr_made and self.last_pr == "OPEN" else [])
            return json.dumps([{"number": n, "url": f"https://x/pull/{n}", "headRefName": "publish/v", "state": "OPEN"}
                               for n in range(7, self.pr_no + 1)] if self.pr_made else [])
        if a[:2] == ["pr", "view"]:
            state = self.pr_states[0] if len(self.pr_states) == 1 else self.pr_states.pop(0)
            self.last_pr = state
            return json.dumps({"state": state, "mergedAt": None})
        if a[0] == "api" and "commits" in a[1]:
            self.head_calls += 1
            return (self.heads[0] if len(self.heads) == 1 else self.heads.pop(0)) + "\n"
        if a[0] == "api":
            return json.dumps({"content": base64.b64encode(json.dumps({"version": self.version}).encode()).decode()})
        raise AssertionError(a)


def args(**kw):
    base = dict(ref=R.BACKEND_REF, build_run_id=None, allow_breaking=False, allow_unknown=False, scope="",
                now=False, settle=0)
    base.update(kw)
    return types.SimpleNamespace(**base)


def make(gh, out):
    ticks = iter(range(0, 10**6))
    return R.Release(gh=gh, sleep=lambda s: None, now=lambda: next(ticks), say=out.append, poll=1, timeout_minutes=60)


class ReleaseTests(unittest.TestCase):

    def test_full_cycle_prints_both_links_and_restores_the_flag(self):
        gh, out = FakeGh(), []
        self.assertEqual(make(gh, out).execute(args()), 0)
        text = "\n".join(out)
        self.assertIn("Review deployments", text)
        self.assertIn("https://x/pull/7", text)
        self.assertIn("2026.10.20-aaaaaaaaaaaa", text)
        self.assertEqual(gh.variable, "false")
        # the build runs on the backend ref; the publisher gets the build run id
        build = next(r for r in gh.runs.values() if r["wf"] == "contract-build.yml")
        self.assertIn(R.BACKEND_REF, build["inputs"])
        publish = next(r for r in gh.runs.values() if r["wf"] == "contract-publish.yml")
        self.assertIn("build_run_id=101", publish["inputs"])

    def test_never_approves_or_merges(self):
        gh = FakeGh()
        make(gh, []).execute(args())
        for call in gh.calls:
            self.assertNotIn("merge", call[:2])
            self.assertNotIn("review", call[:2])
            self.assertFalse(call[:2] == ["pr", "merge"] or call[:2] == ["pr", "review"])

    def test_refusal_prints_the_reason_exits_nonzero_and_restores_flag(self):
        gh, out = FakeGh(publish=("completed/failure",)), []
        self.assertEqual(make(gh, out).execute(args()), 3)
        self.assertIn("REFUSED: 215 unclassified", "\n".join(out))
        self.assertEqual(gh.variable, "false")

    def test_failed_build_stops_before_publishing(self):
        gh, out = FakeGh(build=("completed/failure",)), []
        self.assertEqual(make(gh, out).execute(args()), 3)
        self.assertFalse(any(r["wf"] == "contract-publish.yml" for r in gh.runs.values()))

    def test_existing_build_run_is_reused_and_owner_flags_are_passed_through(self):
        gh = FakeGh()
        gh.runs[555] = {"wf": "earlier-build", "steps": ["completed/success"], "inputs": [], "sha": "A"}
        make(gh, []).execute(args(build_run_id="555", allow_unknown=True, scope="envelope change"))
        self.assertFalse(any(r["wf"] == "contract-build.yml" for r in gh.runs.values()))
        inputs = next(r for r in gh.runs.values() if r["wf"] == "contract-publish.yml")["inputs"]
        for expected in ("build_run_id=555", "allow_unknown=true", "scope=envelope change"):
            self.assertIn(expected, inputs)
        self.assertNotIn("allow_breaking=true", inputs)

    def test_pr_closed_without_merge_is_reported(self):
        gh, out = FakeGh(pr_states=("OPEN", "CLOSED")), []
        self.assertEqual(make(gh, out).execute(args()), 5)
        self.assertEqual(gh.variable, "false")

    def test_flag_is_restored_to_its_previous_value(self):
        gh = FakeGh(variable="true")
        make(gh, []).execute(args())
        self.assertEqual(gh.variable, "true")

    def test_missing_flag_is_restored_to_false(self):
        gh = FakeGh(variable=None)
        make(gh, []).execute(args())
        self.assertEqual(gh.variable, "false")

    def test_timeout_while_waiting_for_a_human(self):
        gh, out = FakeGh(publish=("waiting",)), []
        rel = R.Release(gh=gh, sleep=lambda s: None, now=iter(range(0, 10**6, 600)).__next__, say=out.append,
                        poll=1, timeout_minutes=60)
        self.assertEqual(rel.execute(args()), 4)
        self.assertEqual(gh.variable, "false")


class WatchTests(unittest.TestCase):

    def test_a_new_push_starts_the_whole_cycle_then_it_keeps_listening(self):
        gh, out = FakeGh(heads=("A", "A", "B"), pr_states=("MERGED",)), []
        self.assertEqual(make(gh, out).watch(args(), max_cycles=1), 0)
        text = "\n".join(out)
        self.assertIn("Push detected: B", text)
        self.assertIn("https://x/pull/7", text)
        self.assertIn("Review deployments", text)
        self.assertEqual(sum(1 for r in gh.runs.values() if r["wf"] == "contract-build.yml"), 1)

    def test_no_push_means_no_build(self):
        gh = FakeGh(heads=("A",), pr_states=("MERGED",))
        rel = make(gh, [])
        polls = iter(range(30))

        def sleep(_):
            if next(polls) > 20:
                raise KeyboardInterrupt
        rel.sleep = sleep
        self.assertEqual(rel.watch(args()), 130)
        self.assertEqual(gh.runs, {})

    def test_now_builds_the_current_head_without_waiting_for_a_push(self):
        gh, out = FakeGh(heads=("A",), pr_states=("MERGED",)), []
        make(gh, out).watch(args(now=True), max_cycles=1)
        self.assertTrue(any(r["wf"] == "contract-build.yml" for r in gh.runs.values()))

    def test_refused_commit_is_reported_and_not_retried_but_the_next_push_is_built(self):
        gh, out = FakeGh(heads=("A", "B", "B", "B", "C"), publish=("completed/failure",), pr_states=("MERGED",)), []
        rel = make(gh, out)
        rel.watch(args(), max_cycles=2)
        builds = [r["sha"] for r in gh.runs.values() if r["wf"] == "contract-build.yml"]
        self.assertEqual(builds, ["B", "C"])
        self.assertIn("REFUSED: 215 unclassified", "\n".join(out))
        self.assertEqual(gh.variable, "false")

    def test_waits_while_an_earlier_publication_pr_is_still_open(self):
        gh, out = FakeGh(heads=("A", "B"), pr_states=("MERGED",), preopen=2), []
        make(gh, out).watch(args(), max_cycles=1)
        text = "\n".join(out)
        self.assertIn("still open", text)
        self.assertIn("https://x/pull/3", text)
        self.assertLess(text.index("still open"), text.index("Push detected"))

    def test_watch_does_not_keep_the_flag_on_between_cycles(self):
        gh = FakeGh(heads=("A", "B"), pr_states=("MERGED",))
        make(gh, []).watch(args(), max_cycles=1)
        self.assertEqual(gh.variable, "false")

    def test_watch_never_merges_or_approves(self):
        gh = FakeGh(heads=("A", "B"), pr_states=("MERGED",))
        make(gh, []).watch(args(), max_cycles=1)
        self.assertFalse(any(c[:2] in (["pr", "merge"], ["pr", "review"]) for c in gh.calls))


if __name__ == "__main__":
    unittest.main()
