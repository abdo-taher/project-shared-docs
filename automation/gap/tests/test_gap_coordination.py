import json
import multiprocessing
import os
import stat
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import gap_coordination as gc  # noqa: E402
from coord_fixtures import OWNER_API, make_dev_repo, task_state, write_hotfix, write_state  # noqa: E402
from fakes import gap_request  # noqa: E402
from gap_dispatch import Refused  # noqa: E402
from test_gap_dispatch import DispatchBase, MAINTAINER, POLICY, V, D  # noqa: E402

ACTIVE = dict(agent="agy-cap-own-210", write_set=[f"{OWNER_API}/OpenApi/OwnerResponseSamples.php",
                                                  "bootstrap/providers.php", "tests/Feature/Owner/Thing.php"])


class Fixture(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)
        self.repo = make_dev_repo(self.tmp, {"CAP-OWN-210": task_state("IN_PROGRESS", **ACTIVE)})
        self.coord = gc.Coordination(self.repo)

    def footprint(self, **request):
        return self.coord.footprint(request, POLICY, request.pop("_explicit", []))


class ReservationTests(Fixture):

    def test_only_active_unreleased_tasks_reserve(self):
        write_state(self.repo, {
            "CAP-OWN-210": task_state("IN_PROGRESS", **ACTIVE),
            "CAP-REG-005": task_state("DONE"), "CAP-CUS-001": task_state("PENDING"),
            "CAP-OWN-180": task_state("READY_FOR_REVIEW", released=True)})
        self.assertEqual([r.task for r in self.coord.reservations()], ["CAP-OWN-210"])
        for status in ("CLAIMED", "IN_PROGRESS", "HANDOFF_READY", "BLOCKED", "READY_FOR_REVIEW"):
            write_state(self.repo, {"CAP-REG-005": task_state(status)})
            self.assertIn("CAP-REG-005", [r.task for r in self.coord.reservations()], status)

    def test_expired_lease_is_still_reserved_but_flagged(self):
        past = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
        write_state(self.repo, {"CAP-REG-005": task_state("IN_PROGRESS", lease=past)})
        resv = next(r for r in self.coord.reservations() if r.task == "CAP-REG-005")
        self.assertTrue(resv.lease_expired)
        self.assertTrue(self.coord.conflicts(self.footprint(capability_id="CAP-REG-005")))

    def test_reading_never_writes_and_works_on_a_read_only_copy(self):
        state = self.repo / ".git/capitalix-agent-coordination/state.json"
        before = (state.read_bytes(), state.stat().st_mtime_ns)
        self.coord.reservations()
        self.coord.conflicts(self.footprint(actor="owner"))
        self.assertEqual((state.read_bytes(), state.stat().st_mtime_ns), before)
        self.assertFalse((state.parent / ".state.lock").exists(), "the coordinator's lock file is never created")
        for path in (state, state.parent, self.repo / "docs/final"):
            os.chmod(path, stat.S_IRUSR | (stat.S_IXUSR if path.is_dir() else 0))
        try:
            self.assertEqual(len(gc.Coordination(self.repo).reservations()), 1)
        finally:
            for path in (state.parent, self.repo / "docs/final", state):
                os.chmod(path, 0o755 if path.is_dir() else 0o644)

    def test_unreadable_state_fails_closed(self):
        (self.repo / ".git/capitalix-agent-coordination/state.json").write_text("{not json")
        with self.assertRaises(gc.CoordinationUnavailable):
            self.coord.reservations()
        with self.assertRaises(gc.CoordinationUnavailable):
            gc.Coordination(self.tmp / "missing").reservations()


class FootprintAndConflictTests(Fixture):

    def test_owner_gap_is_blocked_by_the_live_owner_api_reservation_even_if_the_capability_points_elsewhere(self):
        fp = self.footprint(capability_id="CAP-OWN-180", actor="owner")
        self.assertIn(OWNER_API, fp.roots)
        self.assertIn("app/ERP/Modules/Expenses", fp.roots)
        conflicts = self.coord.conflicts(fp)
        self.assertEqual([c["task"] for c in conflicts], ["CAP-OWN-210"])

    def test_unrelated_module_is_clear(self):
        self.assertEqual(self.coord.conflicts(self.footprint(capability_id="CAP-REG-005", actor="public")), [])

    def test_nested_roots_overlap_both_ways(self):
        self.assertTrue(self.coord.conflicts(self.footprint(_explicit=[OWNER_API + "/ReadModels"])))
        write_state(self.repo, {"CAP-OWN-210": task_state("IN_PROGRESS", agent="a")})
        self.assertTrue(self.coord.conflicts(self.footprint(_explicit=["app/ERP/Capabilities"])))

    def test_write_set_path_inside_the_root_conflicts_without_a_matching_root(self):
        write_state(self.repo, {"CAP-CUS-001": task_state("IN_PROGRESS", agent="a",
                                                          write_set=["app/ERP/Modules/Billing/Foo.php"])})
        conflicts = self.coord.conflicts(self.footprint(_explicit=["app/ERP/Modules/Billing"]))
        self.assertEqual(conflicts[0]["task"], "CAP-CUS-001")

    def test_undeterminable_module_is_refused(self):
        with self.assertRaisesRegex(gc.CoordinationConflict, "cannot determine"):
            self.coord.footprint({"actor": "public", "capability_id": "CAP-UNKNOWN-001"}, POLICY, [])

    def test_conflict_clears_when_the_sprint_task_is_done_or_released(self):
        fp = self.footprint(actor="owner")
        self.assertTrue(self.coord.conflicts(fp))
        write_state(self.repo, {"CAP-OWN-210": task_state("DONE")})
        self.assertEqual(self.coord.conflicts(fp), [])
        write_state(self.repo, {"CAP-OWN-210": task_state("IN_PROGRESS", released=True)})
        self.assertEqual(self.coord.conflicts(fp), [])


class HotfixLaneTests(Fixture):
    """The hotfix lane is a second source of live work, invisible to the coordinator's state."""

    CONTENT = "app/ERP/Capabilities/Content"

    def content_gap(self):
        return self.coord.footprint({"capability_id": "CAP-REG-005", "actor": "public"}, POLICY, [self.CONTENT])

    def test_active_hotfix_states_reserve_terminal_ones_do_not(self):
        for state in ("QUEUED", "CLASSIFYING", "READY", "RUNNING", "VALIDATING", "WAITING_INTEGRATION_LOCK", "MERGING",
                      "SYNCHRONIZING", "BLOCKED"):
            write_hotfix(self.repo, "HF-1", state, hints=[self.CONTENT])
            self.assertTrue(self.coord.conflicts(self.content_gap()), state)
        for state in ("COMPLETED", "FAILED", "CANCELLED"):
            write_hotfix(self.repo, "HF-1", state, hints=[self.CONTENT])
            self.assertEqual(self.coord.conflicts(self.content_gap()), [], state)

    def test_declared_paths_decide_which_gaps_are_blocked(self):
        write_hotfix(self.repo, "HF-2", "RUNNING", hints=["app/ERP/Core/Access/Http/Input"], changed=["lang/ar/x.php"])
        self.assertEqual(self.coord.conflicts(self.content_gap()), [])
        elsewhere = self.coord.footprint({"actor": "public"}, POLICY, ["app/ERP/Core/Access"])
        self.assertEqual(self.coord.conflicts(elsewhere)[0]["task"], "hotfix:HF-2", "nested roots overlap both ways")
        lang = self.coord.footprint({"actor": "public"}, POLICY, ["lang/ar"])
        self.assertTrue(self.coord.conflicts(lang), "changed files count too")

    def test_a_running_hotfix_that_declares_nothing_blocks_everything_a_blocked_one_does_not(self):
        write_hotfix(self.repo, "HF-3", "RUNNING")
        self.assertIn("declares no paths", self.coord.conflicts(self.content_gap())[0]["reason"])
        write_hotfix(self.repo, "HF-3", "BLOCKED")
        self.assertEqual(self.coord.conflicts(self.content_gap()), [])

    def test_hotfix_worktrees_and_branches_collide(self):
        write_hotfix(self.repo, "HF-4", "BLOCKED", worktree=str(self.tmp / "hf-wt"), branch="hotfix/x")
        self.assertTrue(self.coord.collisions(self.tmp / "hf-wt" / "inner", "gap/1-a"))
        self.assertTrue(self.coord.collisions(self.tmp / "other", "hotfix/x"))
        self.assertEqual(self.coord.collisions(self.tmp / "other", "gap/1-a"), [])

    def test_a_diff_touching_a_hotfix_path_is_flagged(self):
        write_hotfix(self.repo, "HF-5", "RUNNING", hints=[self.CONTENT], changed=["docs/x.md"])
        clashes = self.coord.check_changed_paths([f"{self.CONTENT}/Http/Y.php", "docs/x.md", "tests/Other.php"])
        self.assertEqual(sorted(c["path"] for c in clashes), [f"{self.CONTENT}/Http/Y.php", "docs/x.md"])

    def test_malformed_hotfix_state_fails_closed_and_no_lane_means_no_hotfixes(self):
        self.assertEqual(self.coord.hotfix_reservations(), [])
        (self.repo / ".state/hotfix/requests").mkdir(parents=True)
        (self.repo / ".state/hotfix/requests/HF-9.json").write_text("{broken")
        with self.assertRaises(gc.CoordinationUnavailable):
            self.coord.reservations()
        (self.repo / ".state/hotfix/requests/HF-9.json").write_text(json.dumps({"id": "HF-9"}))
        with self.assertRaises(gc.CoordinationUnavailable):
            self.coord.reservations()

    def test_the_dispatcher_waits_for_a_running_hotfix(self):
        write_state(self.repo, {"CAP-OWN-210": task_state("DONE")})
        write_hotfix(self.repo, "HF-6", "RUNNING", hints=[OWNER_API])
        gl_policy_roots = self.coord.footprint({"actor": "owner"}, POLICY, [])
        self.assertEqual(self.coord.conflicts(gl_policy_roots)[0]["task"], "hotfix:HF-6")


class ChangedPathTests(Fixture):

    def test_a_reserved_file_is_a_clash_shared_wiring_is_not(self):
        clashes = self.coord.check_changed_paths([f"{OWNER_API}/OpenApi/OwnerResponseSamples.php",
                                                  "bootstrap/providers.php", "docs/api/openapi.json",
                                                  "tests/Unit/Other.php"])
        self.assertEqual([(c["task"], c["path"]) for c in clashes],
                         [("CAP-OWN-210", f"{OWNER_API}/OpenApi/OwnerResponseSamples.php"),
                          ("CAP-OWN-210", "tests/Feature/Owner/Thing.php")][:1])

    def test_directory_reservations_and_undeclared_same_root_reservations(self):
        write_state(self.repo, {"CAP-CUS-001": task_state("CLAIMED", agent="a"),
                                "CAP-REG-005": task_state("IN_PROGRESS", agent="b",
                                                          write_set=["app/ERP/Capabilities/Onboarding/**"])})
        clashes = self.coord.check_changed_paths(["app/ERP/Modules/Customers/Actions/X.php",
                                                  "app/ERP/Capabilities/Onboarding/Y.php"])
        self.assertEqual(sorted(c["task"] for c in clashes), ["CAP-CUS-001", "CAP-REG-005"])

    def test_worktree_and_branch_collisions(self):
        write_state(self.repo, {"CAP-OWN-210": task_state("IN_PROGRESS", agent="a", branch="agent/x",
                                                          worktree=str(self.tmp / "sprint-wt"))})
        self.assertEqual(self.coord.collisions(self.tmp / "gapwork" / "gap-1", "gap/1-abc"), [])
        self.assertTrue(self.coord.collisions(self.tmp / "sprint-wt" / "inner", "gap/1-abc"))
        self.assertTrue(self.coord.collisions(self.tmp / "gapwork", "agent/x"))
        self.assertTrue(self.coord.collisions(self.repo / "capitalix-agent-worktrees" / "x", "gap/1-abc"))


def _race(args):
    state_dir, issue, barrier_path = args
    store = gc.LeaseStore(Path(state_dir))
    while not Path(barrier_path).exists():
        pass
    try:
        store.acquire(issue, [OWNER_API], 600, pid=os.getppid())
        return True
    except gc.CoordinationConflict:
        return False


class LeaseTests(unittest.TestCase):

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)
        self.now = datetime(2026, 10, 19, 12, 0, tzinfo=timezone.utc)
        self.alive = {os.getpid()}
        self.store = gc.LeaseStore(self.dir, now=lambda: self.now, alive=lambda pid: pid in self.alive)

    def test_overlapping_roots_are_exclusive_other_roots_are_not(self):
        self.store.acquire(1, [OWNER_API], 600)
        with self.assertRaises(gc.CoordinationConflict):
            self.store.acquire(2, [OWNER_API + "/ReadModels"], 600)
        self.store.acquire(3, ["app/ERP/Modules/Customers"], 600)
        self.store.acquire(1, [OWNER_API], 600)  # re-acquiring one's own lease is idempotent
        self.assertEqual(sorted(self.store.held()), ["1", "3"])

    def test_release_frees_the_root(self):
        self.store.acquire(1, [OWNER_API], 600)
        self.store.release(1)
        self.store.acquire(2, [OWNER_API], 600)

    def test_abandoned_leases_are_reaped(self):
        self.store.acquire(1, [OWNER_API], 600, pid=424242)  # a dispatcher that crashed
        self.assertEqual(self.store.reap(), ["1"])
        self.store.acquire(2, [OWNER_API], 600)

    def test_expired_lease_of_a_live_process_is_reaped_too(self):
        self.store.acquire(1, [OWNER_API], 600)
        self.now += timedelta(seconds=601)
        self.store.acquire(2, [OWNER_API], 600)
        self.assertEqual(list(self.store.held()), ["2"])

    def test_concurrent_acquisition_has_exactly_one_winner(self):
        barrier = self.dir / "go"
        with multiprocessing.Pool(6) as pool:
            result = pool.map_async(_race, [(str(self.dir), i, str(barrier)) for i in range(6)])
            barrier.write_text("go")
            outcomes = result.get(timeout=30)
        self.assertEqual(outcomes.count(True), 1, outcomes)


class DispatcherIntegrationTests(DispatchBase):

    def setUp(self):
        super().setUp()
        self.dev = make_dev_repo(self.tmp, {"CAP-OWN-210": task_state("IN_PROGRESS", **ACTIVE)})
        self.coord = gc.Coordination(self.dev)
        self.approve()

    def disp(self, **kwargs):
        # the fake agent edits app.txt: allowed here unless a test exercises the strict default
        kwargs.setdefault("always_allowed", ["tests/", "docs/api-gap/resolutions/", "app.txt"])
        return self.dispatcher(coordination=self.coord, coordination_required=True, **kwargs)

    def test_a_reserved_module_is_listed_not_eligible_and_nothing_is_touched(self):
        status = dict(self.disp().eligible())[1]
        self.assertIn("coordination conflict", status)
        self.assertIn("CAP-OWN-210", status)
        before = (list(self.gl.issues[1]["labels"]), len(self.gl.notes(1)))
        with self.assertRaisesRegex(Refused, "coordination conflict"):
            self.disp().run(1)
        self.assertEqual((self.gl.issues[1]["labels"], len(self.gl.notes(1))), before, "not a failure: no label, no note")
        self.assertFalse(self.workdir.exists(), "no clone, no agent")
        self.assertEqual(self.forge.opened, [])

    def test_dispatch_proceeds_once_the_sprint_task_is_done(self):
        write_state(self.dev, {"CAP-OWN-210": task_state("DONE")})
        self.assertEqual(dict(self.disp().eligible())[1], "ELIGIBLE")
        self.assertEqual(self.disp().run(1)["status"], "MR_OPENED")
        self.assertEqual(self.coord and gc.LeaseStore(self.workdir / "state").held(), {}, "lease released")

    def test_required_coordination_that_is_missing_or_unreadable_fails_closed(self):
        with self.assertRaisesRegex(Refused, "required but not configured"):
            self.dispatcher(coordination_required=True).run(1)
        (self.dev / ".git/capitalix-agent-coordination/state.json").write_text("garbage")
        with self.assertRaisesRegex(Refused, "fail closed"):
            self.disp().run(1)

    def test_a_second_dispatch_on_the_same_module_waits_for_the_lease(self):
        write_state(self.dev, {"CAP-OWN-210": task_state("DONE")})
        gc.LeaseStore(self.workdir / "state").acquire(99, [OWNER_API], 600)
        with self.assertRaisesRegex(Refused, "already holds a lease"):
            self.disp().run(1)
        self.assertEqual(self.forge.opened, [])

    def test_the_lease_is_released_when_the_dispatch_fails(self):
        write_state(self.dev, {"CAP-OWN-210": task_state("DONE")})
        self.mode.write_text("fail")
        with self.assertRaises(Refused):
            self.disp().run(1)
        self.assertEqual(gc.LeaseStore(self.workdir / "state").held(), {})

    def test_a_diff_touching_files_a_sprint_task_reserved_is_refused(self):
        # the sprint task claims the file the agent will touch only AFTER the dispatch started
        write_state(self.dev, {"CAP-OWN-210": task_state("DONE")})
        self.mode.write_text("good")
        real_check = gc.Coordination.check_changed_paths

        def late_claim(coord_self, changed):
            write_state(self.dev, {"CAP-CUS-001": task_state("IN_PROGRESS", agent="late", write_set=["app.txt"])})
            return real_check(coord_self, changed)

        from unittest import mock
        with mock.patch.object(gc.Coordination, "check_changed_paths", late_claim):
            with self.assertRaisesRegex(Refused, "reserved by an active sprint task"):
                self.disp().run(1)
        self.assertEqual(self.forge.opened, [])
        self.assertNotIn(f"gap/1-{self.fp[:16]}", self.remote_branches(), "nothing was pushed")
        self.assertIn("gap-dispatch::failed", self.gl.issues[1]["labels"])

    def test_migrations_are_never_part_of_a_gap_change(self):
        write_state(self.dev, {"CAP-OWN-210": task_state("DONE")})
        policy_paths = self.dispatcher().protected
        self.assertIn("database/migrations/", policy_paths)

    def test_a_change_outside_the_reserved_write_area_is_refused(self):
        write_state(self.dev, {"CAP-OWN-210": task_state("DONE")})
        self.mode.write_text("good")      # the fake agent edits app.txt, which is outside OwnerApi/Expenses and tests/
        with self.assertRaisesRegex(Refused, "outside the write area reserved for this gap.*app.txt"):
            self.disp(always_allowed=["tests/", "docs/api-gap/resolutions/"]).run(1)
        self.assertEqual(self.forge.opened, [])
        self.assertNotIn(f"gap/1-{self.fp[:16]}", self.remote_branches())
        self.assertEqual(gc.LeaseStore(self.workdir / "state").held(), {})

    def test_a_maintainer_can_widen_the_write_area_explicitly(self):
        write_state(self.dev, {"CAP-OWN-210": task_state("DONE")})
        self.gl.add_label_by(1, "gap-root::app.txt", MAINTAINER)  # not under app/, tests/, docs/, lang/: ignored
        with self.assertRaisesRegex(Refused, "outside the write area"):
            self.disp(always_allowed=["tests/", "docs/api-gap/resolutions/"]).run(1)

    def test_the_prompt_states_the_write_area_and_forbids_running_the_coordinator(self):
        d = self.disp()
        d.write_area = [OWNER_API]
        prompt = d.prompt(1, self.fp, self.request)
        self.assertIn("Task claim and write area", prompt)
        self.assertIn(OWNER_API + "/", prompt)
        self.assertIn("do NOT run scripts/agent-wave-coordinator.py", prompt)
        d.write_area = None
        self.assertNotIn("Task claim and write area", d.prompt(1, self.fp, self.request))

    def test_maintainer_declared_root_widens_the_footprint_but_a_developer_cannot(self):
        write_state(self.dev, {"CAP-OWN-210": task_state("DONE"), "CAP-CUS-001": task_state(
            "IN_PROGRESS", agent="a", write_set=["app/ERP/Modules/Customers/X.php"])})
        label = "gap-root::app/ERP/Modules/Customers"
        self.gl.add_label_by(1, label, 8)  # Developer
        self.assertEqual(dict(self.disp().eligible())[1], "ELIGIBLE", "a developer's label is ignored")
        self.gl.issues[1]["labels"].remove(label)
        self.gl.add_label_by(1, label, MAINTAINER)
        self.assertIn("CAP-CUS-001", dict(self.disp().eligible())[1])

    def test_recovery_releases_the_lease_of_a_crashed_dispatcher(self):
        store = gc.LeaseStore(self.workdir / "state")
        store.acquire(1, [OWNER_API], 600, pid=999999)
        self.disp().recover()
        self.assertEqual(store.held(), {})


if __name__ == "__main__":
    unittest.main()
