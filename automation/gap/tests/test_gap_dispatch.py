import json
import os
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import gap_core as core  # noqa: E402
import gap_dispatch  # noqa: E402
import gap_sandbox  # noqa: E402
from fakes import FakeBackend, gap_request  # noqa: E402
from gap_coordinator import RESOLUTION_SCHEMA, Coordinator, Intake, load_policy, parse_resolution  # noqa: E402
from gap_dispatch import Dispatcher, Refused, Shutdown, probe, runner_env  # noqa: E402

POLICY = load_policy(HERE.parent / "policy.json")
V, D = "2026.10.18-06d388692794", "06d3886927947b77daad9c38c677bee4beb0b6f39ff8f0b8ad8c5d1bc257578c"
MAINTAINER, DEVELOPER, OWNER = 7, 8, 9
IMAGE = "capitalix-gap-agent:2"

RUNNER = textwrap.dedent('''
    import json, os, re, subprocess, sys
    from pathlib import Path
    prompt = sys.stdin.read()
    probe = re.search(r"GAP-PROBE-[0-9a-f]+", prompt)
    if probe:
        print(probe.group(0)); sys.exit(0)
    mode = Path(sys.argv[1]).read_text().strip()
    work = Path.cwd()
    if mode != "sandboxed":
        (work.parent / "runner-env.json").write_text(json.dumps(sorted(os.environ)))
    fp = re.search(r'"fingerprint": "([0-9a-f]{64})"', prompt).group(1)
    iid = int(re.search(r'"backend_issue": (\\d+)', prompt).group(1))
    def commit(paths):
        subprocess.run(["git", "add", *paths], check=True)
        subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.com", "commit", "-qm", "fix"], check=True)
    if mode == "fail":
        sys.exit(9)
    if mode == "hang":
        import time; time.sleep(60)
    if mode == "classify":
        (work / ".gap-result.json").write_text(json.dumps({"root_cause": "E", "summary": "app bug"}))
        sys.exit(0)
    Path("app.txt").write_text("fixed\\n")
    paths = ["app.txt"]
    if mode in ("good", "sandboxed", "causec-withtest"):
        Path("tests").mkdir(exist_ok=True); Path("tests/test_new.txt").write_text("test\\n"); paths.append("tests/test_new.txt")
    for protected in {"ci": [".gitlab-ci.yml"], "lock": ["composer.lock"], "final": ["docs/final/x.json"]}.get(mode, []):
        Path(protected).parent.mkdir(parents=True, exist_ok=True); Path(protected).write_text("x\\n"); paths.append(protected)
    if mode != "no-evidence":
        target = Path("docs/api-gap/resolutions") / f"{fp[:16]}.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        cause = "C" if mode.startswith("causec") else "A"
        target.write_text(json.dumps({"schema": "capitalix.api-gap-resolution.v1", "fingerprint": fp,
            "backend_issue": iid, "root_cause": cause, "summary": "adds the list",
            "checks": [{"check": "operation_exists", "operation_id": "owner.sales.customers.index"}] if cause == "A" else [],
            "tests": ["tests/test_new.txt"]}))
        paths.append(str(target))
    commit(paths)
''')


def git(*args, cwd):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


class FakeForge:
    name = "fake"

    def __init__(self):
        self.opened = []

    def open_review(self, branch, base, title, body, worktree=None):
        self.opened.append({"branch": branch, "base": base, "title": title, "body": body})
        return f"https://example.invalid/review/{len(self.opened)}", f"#{len(self.opened)}"


class DispatchBase(unittest.TestCase):

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)
        self.remote = self.tmp / "dev.git"
        seed = self.tmp / "seed"
        git("init", "-q", "--bare", "-b", "integration", str(self.remote), cwd=self.tmp)
        git("init", "-q", "-b", "integration", str(seed), cwd=self.tmp)
        (seed / "README.md").write_text("development\n")
        git("add", "README.md", cwd=seed)
        git("-c", "user.name=t", "-c", "user.email=t@example.com", "commit", "-qm", "init", cwd=seed)
        git("push", "-q", str(self.remote), "integration", cwd=seed)
        (self.tmp / "runner.py").write_text(RUNNER)
        self.mode = self.tmp / "mode"
        self.mode.write_text("good")
        self.template = f"{sys.executable} {self.tmp / 'runner.py'} {self.mode}"
        self.gl = FakeBackend()
        self.gl.access = {MAINTAINER: 40, DEVELOPER: 20, OWNER: 50}
        self.forge = FakeForge()
        self.request = gap_request(V, D)
        coordinator = Coordinator({**POLICY, "coordinator_github_login": "bot"}, None, self.gl, None)
        intake = Intake(number=1, author="alice", request=self.request, fingerprint=core.fingerprint(self.request))
        self.fp = intake.fingerprint
        self.gl.create_issue(coordinator.backend_title(intake), coordinator.backend_description(intake),
                             ["api-gap", "gap::accepted"])
        self.workdir = self.tmp / "work"

    def dispatcher(self, **kwargs) -> Dispatcher:
        coordination = kwargs.pop("coordination", None)
        allowed = kwargs.pop("always_allowed", None)
        policy = {**POLICY, "coordination": {**POLICY["coordination"], "required": kwargs.pop("coordination_required", False),
                                             **({"always_allowed": allowed} if allowed is not None else {})},
                  "verification": kwargs.pop("verification", {}),   # the Laravel verification only where a test opts in
                  "evidence": kwargs.pop("evidence", {}),           # likewise the published-contract negative control
                  **({"contract_source": kwargs.pop("contract_source")} if "contract_source" in kwargs else {})}
        return Dispatcher(policy, self.gl, workdir=kwargs.pop("workdir", self.workdir), coordination=coordination,
                          template=kwargs.pop("template", self.template), timeout=kwargs.pop("timeout", 30),
                          forge=self.forge, remote=str(self.remote), base_branch="integration",
                          sandbox_cfg=kwargs.pop("sandbox_cfg", None), log=lambda m: None, **kwargs)

    def approve(self, user=MAINTAINER, owner=False):
        self.gl.add_label_by(1, "gap-dispatch::approved", user)
        if owner:
            self.gl.add_label_by(1, "gap-owner::approved", OWNER, username="abdo-taher")

    def remote_branches(self) -> str:
        return subprocess.run(["git", "branch", "--format=%(refname:short)"], cwd=self.remote, capture_output=True,
                              text=True).stdout


class DispatchTests(DispatchBase):

    def test_probe_proves_the_runner_starts(self):
        status, detail = probe(self.template, 20)
        self.assertEqual(status, "RUNTIME_OK")
        self.assertIn("WITHOUT a sandbox", detail)

    def test_probe_reports_missing_runtime(self):
        self.assertEqual(probe(None, 5)[0], "BLOCKED_AGENT_RUNTIME")
        self.assertEqual(probe("/nonexistent/agent --x", 5)[0], "BLOCKED_AGENT_RUNTIME")
        self.assertEqual(probe("true", 5)[0], "BLOCKED_AGENT_RUNTIME", "a runner that does not answer is not proof")

    def test_probe_blocks_when_the_sandbox_is_unavailable(self):
        status, detail = probe(self.template, 5, {"image": "capitalix-gap-agent:does-not-exist"})
        self.assertEqual(status, "BLOCKED_AGENT_RUNTIME")
        self.assertIn("sandbox unavailable", detail)

    def test_dispatch_requires_maintainer_approval(self):
        with self.assertRaisesRegex(Refused, "gap-dispatch::approved"):
            self.dispatcher().run(1)
        self.approve(user=DEVELOPER)
        with self.assertRaisesRegex(Refused, "write access"):
            self.dispatcher().run(1)

    def test_sensitive_gap_requires_owner_approval(self):
        sensitive = gap_request(V, D, capability_id="CAP-TAX-001", location="vat.report")
        self.gl.issues[1]["description"] = self.gl.issues[1]["description"].replace(
            json.dumps(self.request, indent=2, ensure_ascii=False), json.dumps(sensitive, indent=2, ensure_ascii=False))
        self.gl.issues[1]["description"] = self.gl.issues[1]["description"].replace(
            self.fp, core.fingerprint(sensitive))
        self.approve()
        with self.assertRaisesRegex(Refused, "owner"):
            self.dispatcher().run(1)
        self.gl.add_label_by(1, "gap-owner::approved", MAINTAINER, username="someone-else")
        with self.assertRaisesRegex(Refused, "owner"):
            self.dispatcher().run(1)

    def test_open_mr_prevents_duplicate_execution(self):
        self.approve()
        self.gl.mrs[1] = [{"iid": 3, "state": "opened"}]
        with self.assertRaisesRegex(Refused, "already linked"):
            self.dispatcher().run(1)

    def test_edited_request_is_refused(self):
        self.approve()
        self.gl.issues[1]["description"] = self.gl.issues[1]["description"].replace('"actor": "owner"', '"actor": "admin"')
        with self.assertRaisesRegex(Refused, "fingerprint"):
            self.dispatcher().run(1)

    def test_successful_dispatch_opens_a_draft_review_on_the_development_source(self):
        self.approve()
        outcome = self.dispatcher().run(1)
        self.assertEqual(outcome["status"], "MR_OPENED")
        review = self.forge.opened[0]
        self.assertTrue(review["title"].startswith("Draft: "))
        self.assertEqual(review["base"], "integration")
        self.assertIn(self.fp, review["body"])
        self.assertIn(f"gap/1-{self.fp[:16]}", self.remote_branches())
        self.assertIn("gap::in-progress", self.gl.issues[1]["labels"])
        self.assertNotIn("gap::accepted", self.gl.issues[1]["labels"])
        statuses = [json.loads(n["body"].split(" ", 2)[2].split(" -->")[0])["status"] for n in self.gl.notes(1)]
        self.assertEqual(statuses, ["STARTED", "REVIEW_OPENED"])
        self.assertIn("https://example.invalid/review/1", self.gl.notes(1)[-1]["body"], "GitLab issue links the review")
        self.assertEqual(json.loads((self.workdir / "state/dispatch/1.json").read_text())["status"], "MR_OPENED")
        self.assertEqual(self.gl.created_mrs, [], "no GitLab MR: the fix lives on the development source")

    def test_duplicate_dispatch_is_prevented(self):
        self.approve()
        self.dispatcher().run(1)
        with self.assertRaisesRegex(Refused, "already in progress"):
            self.dispatcher(workdir=self.tmp / "work2").run(1)
        self.assertEqual(len(self.forge.opened), 1)

    def test_runner_never_receives_credentials(self):
        self.approve()
        env = {"API_GAP_DISPATCH_TOKEN": "x", "GITLAB_TOKEN": "y", "GH_TOKEN": "z", "SOME_SECRET": "s",
               "SSH_AUTH_SOCK": "/s", "CLAUDE_CODE_MESSAGING_TOKEN": "m", "CLAUDECODE": "1", "ANTHROPIC_API_KEY": "k"}
        with mock.patch.dict(os.environ, env):
            self.assertFalse(set(env) & set(runner_env()))
            self.dispatcher().run(1)
        seen = set(json.loads((self.workdir / "runner-env.json").read_text()))
        self.assertFalse(set(env) & seen)

    def test_protected_paths_are_refused(self):
        for mode in ("ci", "lock", "final"):
            with self.subTest(mode):
                self.setUp()
                self.approve()
                self.mode.write_text(mode)
                with self.assertRaisesRegex(Refused, "protected paths"):
                    self.dispatcher().run(1)
                self.assertEqual(self.forge.opened, [])
                self.assertEqual(self.remote_branches().strip(), "integration", "nothing was pushed")

    def test_missing_resolution_evidence_is_refused(self):
        self.approve()
        self.mode.write_text("no-evidence")
        with self.assertRaisesRegex(Refused, "does not add"):
            self.dispatcher().run(1)

    def test_root_cause_c_needs_a_test_changed_by_the_change(self):
        self.approve()
        self.mode.write_text("causec-notest")  # evidence claims a test file the change does not contain
        with self.assertRaisesRegex(Refused, "root cause C needs a test"):
            self.dispatcher().run(1)
        self.setUp()
        self.approve()
        self.mode.write_text("causec-withtest")
        self.assertEqual(self.dispatcher().run(1)["status"], "MR_OPENED")

    def test_classification_without_code_change(self):
        self.approve()
        self.mode.write_text("classify")
        outcome = self.dispatcher().run(1)
        self.assertEqual(outcome, {"status": "CLASSIFIED", "root_cause": "E"})
        self.assertEqual(self.forge.opened, [])
        self.assertIn("gap-triage::not-backend", self.gl.notes(1)[-1]["body"])
        self.assertNotIn("gap-triage::not-backend", self.gl.issues[1]["labels"], "a human confirms it")
        self.assertIn("gap::accepted", self.gl.issues[1]["labels"])

    def test_failure_recovery_is_visible_and_needs_an_explicit_retry(self):
        self.approve()
        self.mode.write_text("fail")
        with self.assertRaisesRegex(Refused, "exited 9"):
            self.dispatcher().run(1)
        labels = self.gl.issues[1]["labels"]
        self.assertIn("gap-dispatch::failed", labels)
        self.assertIn("gap::accepted", labels)
        self.assertNotIn("gap::in-progress", labels)
        with self.assertRaisesRegex(Refused, "previous dispatch failed"):
            self.dispatcher(workdir=self.tmp / "work2").run(1)
        self.mode.write_text("good")
        outcome = self.dispatcher(workdir=self.tmp / "work3").run(1, retry=True)
        self.assertEqual(outcome["status"], "MR_OPENED")
        self.assertNotIn("gap-dispatch::failed", self.gl.issues[1]["labels"])

    def test_timeout_is_a_recorded_failure(self):
        self.approve()
        self.mode.write_text("hang")
        with self.assertRaisesRegex(Refused, "did not finish"):
            self.dispatcher(timeout=3).run(1)
        self.assertIn("gap-dispatch::failed", self.gl.issues[1]["labels"])
        self.assertEqual(json.loads((self.workdir / "state/dispatch/1.json").read_text())["status"], "FAILED")

    def test_existing_remote_branch_is_never_overwritten(self):
        self.approve()
        git("push", "-q", str(self.remote), f"integration:refs/heads/gap/1-{self.fp[:16]}", cwd=self.remote)
        with self.assertRaisesRegex(Refused, "already exists on the development remote"):
            self.dispatcher().run(1)

    def test_existing_workspace_is_kept_and_blocks_a_rerun(self):
        self.approve()
        self.mode.write_text("fail")
        with self.assertRaises(Refused):
            self.dispatcher().run(1)
        self.mode.write_text("good")
        with self.assertRaisesRegex(Refused, "already exists"):
            self.dispatcher().run(1, retry=True)

    def test_restart_recovery_settles_interrupted_dispatches(self):
        self.approve()
        d = self.dispatcher()
        self.gl.update_issue(1, add_labels="gap::in-progress", remove_labels="gap::accepted")
        d._write_record(1, status="STARTED", pid=999999, worktree="/x", branch="b")
        self.assertEqual(d.recover(alive=lambda pid: False), [1])
        labels = self.gl.issues[1]["labels"]
        self.assertIn("gap-dispatch::failed", labels)
        self.assertNotIn("gap::in-progress", labels)
        self.assertIn("restart recovery", self.gl.notes(1)[-1]["body"])
        self.assertEqual(d.recover(alive=lambda pid: False), [], "settled once")

    def test_recovery_removes_stale_copies_of_the_agents_login(self):
        import gap_dispatch
        stale = gap_dispatch.secret_run_root(self.workdir) / "gap-9" / "agent-config"
        stale.mkdir(parents=True)
        (stale / ".credentials.json").write_text("{}")
        self.dispatcher().recover()
        self.assertFalse(stale.exists(), "a crashed dispatcher's login copy is removed at the next start")

    def test_the_login_copy_is_private_and_never_inside_the_worktree(self):
        import gap_dispatch
        root = gap_dispatch.secret_run_root(self.workdir)
        self.assertNotIn(str(self.workdir / "gap-1-"), str(root))
        with mock.patch.dict(os.environ, {"XDG_RUNTIME_DIR": str(self.tmp)}):
            self.assertEqual(gap_dispatch.secret_run_root(self.workdir), self.tmp / "capitalix-gap-run")

    def test_recovery_leaves_live_dispatches_alone(self):
        d = self.dispatcher()
        d._write_record(1, status="STARTED", pid=os.getpid(), worktree="/x", branch="b")
        self.assertEqual(d.recover(), [])

    def test_shutdown_during_a_run_fails_it_cleanly(self):
        import gap_dispatch
        self.approve()
        real = gap_dispatch.run_agent

        def interrupt_the_real_run_only(argv, **kwargs):
            if "Reply with exactly" in kwargs["stdin_text"]:
                return real(argv, **kwargs)  # the runtime probe still works
            raise Shutdown()

        with mock.patch("gap_dispatch.run_agent", side_effect=interrupt_the_real_run_only):
            with self.assertRaises(Shutdown):
                self.dispatcher().run(1)
        self.assertIn("gap-dispatch::failed", self.gl.issues[1]["labels"])
        self.assertNotIn("gap::in-progress", self.gl.issues[1]["labels"])
        self.assertEqual(json.loads((self.workdir / "state/dispatch/1.json").read_text())["status"], "INTERRUPTED")

    def test_dry_run_touches_nothing(self):
        self.approve()
        outcome = self.dispatcher(dry_run=True).run(1)
        self.assertEqual(outcome["status"], "DRY_RUN_ELIGIBLE")
        self.assertEqual(outcome["base"], "integration")
        self.assertFalse(self.workdir.exists())
        self.assertEqual(self.gl.notes(1), [])

    def published_fixture(self, with_summary: bool):
        from fakes import contract, publish
        root = self.tmp / "published"
        root.mkdir(exist_ok=True)
        document = contract()
        document["paths"]["/api/owner/sales/customers/{id}"]["get"]["operationId"] = "owner.sales.customers.show"
        if with_summary:
            document["paths"]["/api/owner/sales/customers/{id}"]["get"]["summary"] = "Show a customer"
        publish(root, "2026.10.18", document)
        return f"file:{root}"

    def evidence_runner(self, checks):
        (self.tmp / "ev_runner.py").write_text(textwrap.dedent(f'''
            import json, re, subprocess, sys
            from pathlib import Path
            prompt = sys.stdin.read()
            m = re.search(r"GAP-PROBE-[0-9a-f]+", prompt)
            if m:
                print(m.group(0)); sys.exit(0)
            fp = re.search(r'"fingerprint": "([0-9a-f]{{64}})"', prompt).group(1)
            iid = int(re.search(r'"backend_issue": (\\d+)', prompt).group(1))
            Path("tests").mkdir(exist_ok=True); Path("tests/t.txt").write_text("t")
            Path("docs/api-gap/resolutions").mkdir(parents=True, exist_ok=True)
            Path(f"docs/api-gap/resolutions/{{fp[:16]}}.json").write_text(json.dumps({{
                "schema": "capitalix.api-gap-resolution.v1", "fingerprint": fp, "backend_issue": iid, "root_cause": "D",
                "summary": "s", "tests": ["tests/t.txt"], "checks": {json.dumps(checks)}}}))
            subprocess.run(["git", "add", "-A"], check=True)
            subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.com", "commit", "-qm", "doc"], check=True)
        '''))
        return f"{sys.executable} {self.tmp / 'ev_runner.py'}"

    def test_vacuous_evidence_is_refused_and_a_check_that_fails_today_is_accepted(self):
        self.approve()
        source = self.published_fixture(with_summary=False)
        holds_today = [{"check": "operation_exists", "operation_id": "owner.sales.customers.show"}]
        fails_today = holds_today + [{"check": "operation_has_summary", "operation_id": "owner.sales.customers.show"}]
        evidence = {"require_failing_on_published": True}
        d = self.dispatcher(template=self.evidence_runner(holds_today), evidence=evidence, contract_source=source)
        with self.assertRaisesRegex(Refused, "evidence is vacuous"):
            d.run(1)
        self.assertEqual(self.forge.opened, [])
        self.assertNotIn(f"gap/1-{self.fp[:16]}", self.remote_branches())
        self.setUp()
        self.approve()
        d = self.dispatcher(template=self.evidence_runner(fails_today), evidence=evidence, contract_source=source)
        self.assertEqual(d.run(1)["status"], "MR_OPENED")

    def test_the_agent_is_told_about_the_negative_control_and_given_the_published_contract(self):
        self.approve()
        source = self.published_fixture(with_summary=False)
        d = self.dispatcher(evidence={"require_failing_on_published": True}, contract_source=source)
        d.prepare_published_contract(1)
        prompt = d.prompt(1, self.fp, self.request)
        self.assertIn("NEGATIVE CONTROL", prompt)
        self.assertIn(str(d.published_path(1)), prompt)
        self.assertIn("--expect-failure", prompt)
        self.assertIn("operation_has_summary", prompt)
        self.assertTrue(d.published_path(1).exists())
        off = self.dispatcher()
        self.assertNotIn("NEGATIVE CONTROL", off.prompt(1, self.fp, self.request))

    def test_prompt_is_self_contained_and_marks_input_untrusted(self):
        prompt = self.dispatcher().prompt(1, self.fp, self.request)
        self.assertIn("UNTRUSTED consumer input", prompt)
        self.assertIn("capitalix.api-gap-resolution.v1", prompt)
        self.assertIn(self.fp, prompt)
        self.assertIn("php vendor/bin/phpunit", prompt)
        self.assertIn(".gap-result.json", prompt)

    def test_resolution_evidence_schema(self):
        good = {"schema": RESOLUTION_SCHEMA, "fingerprint": self.fp, "backend_issue": 1, "root_cause": "A",
                "checks": [{"check": "operation_exists", "operation_id": "x"}], "tests": [], "summary": "s"}
        self.assertIsNone(parse_resolution(json.dumps(good).encode(), self.fp, 1)[1])
        for change in ({"root_cause": "E"}, {"checks": []}, {"backend_issue": 2}, {"fingerprint": "0" * 64},
                       {"root_cause": "C", "tests": []}, {"summary": "x" * 501}):
            self.assertIsNotNone(parse_resolution(json.dumps({**good, **change}).encode(), self.fp, 1)[1], change)
        self.assertIsNotNone(parse_resolution(b"not json", self.fp, 1)[1])


class AgentImageDefinitionTests(unittest.TestCase):
    def test_base_images_are_pinned_by_digest_and_nothing_from_the_host_is_baked_in(self):
        text = (HERE.parent / "image/gap-agent.Dockerfile").read_text()
        self.assertRegex(text, r"(?m)^FROM php:8\.5-cli-bookworm@sha256:[0-9a-f]{64}$")
        self.assertRegex(text, r"COPY --from=composer:2@sha256:[0-9a-f]{64} ")
        lines = [l for l in text.splitlines() if l.strip() and not l.lstrip().startswith("#") and not l.startswith((" ", "\t"))]
        instructions = [l.split()[0].upper() for l in lines]
        self.assertFalse({"ADD", "ARG"} & set(instructions), instructions)
        for line in lines:
            if line.upper().startswith("COPY"):
                self.assertIn("--from=", line, "COPY may only come from a pinned image, never from the host")
        env_names = {tok.split("=")[0] for l in text.splitlines() if l.startswith("ENV") for tok in l.split()[1:] if "=" in tok}
        self.assertFalse([n for n in env_names if any(w in n for w in ("TOKEN", "SECRET", "PASSWORD", "KEY"))], env_names)

    def test_the_image_provides_the_php_the_backend_lockfile_requires(self):
        agent = (HERE.parent / "image/gap-agent.Dockerfile").read_text()
        self.assertIn("PHP 8.5.11", agent)
        self.assertIn("composer.lock", agent)


@unittest.skipUnless(gap_sandbox.available(IMAGE)[0], f"docker image {IMAGE} not available")
class SandboxTests(DispatchBase):
    """Real containers. Skipped where docker or the agent image is missing (e.g. a hosted runner)."""

    SANDBOX = {"image": IMAGE, "memory": "1g", "cpus": "1"}

    def test_sandbox_isolation_from_the_agents_point_of_view(self):
        home = str(Path.home())
        probe_script = self.tmp / "isolation.py"
        probe_script.write_text(textwrap.dedent(f'''
            import json, os
            from pathlib import Path
            def writable(p):
                try: Path(p).write_text("x"); return True
                except Exception: return False
            cfg = Path(os.environ["CLAUDE_CONFIG_DIR"]) / ".credentials.json"
            print(json.dumps({{
                "home": os.path.exists({home!r}),
                "ssh": os.path.exists({home + "/.ssh"!r}),
                "claude_dir": os.path.exists({home + "/.claude"!r}),
                "glab": os.path.exists({home + "/.config/glab-cli"!r}),
                "docker_sock": os.path.exists("/var/run/docker.sock"),
                "www": os.path.isdir("/var/www/html") and os.listdir("/var/www/html") != [],
                "write_worktree": writable("w.txt"), "write_etc": writable("/etc/x"), "write_usr": writable("/usr/x"),
                "env": sorted(os.environ),
                # GPG_KEYS is set by the official php image itself: public key fingerprints, not a secret
                "tokens": [k for k in os.environ if any(s in k for s in ("TOKEN", "SECRET", "KEY", "PASSWORD"))
                           and k not in ("CLAUDE_CONFIG_DIR", "GPG_KEYS")],
                "login_entries": sorted(json.loads(cfg.read_text())) if cfg.exists() else None,
                "uid": os.getuid(), "processes": len([p for p in os.listdir("/proc") if p.isdigit()])}}))
        '''))
        work = self.tmp / "wt"
        work.mkdir()
        fake_home = self.tmp / "fakehome"
        (fake_home / ".claude").mkdir(parents=True)
        (fake_home / ".claude/.credentials.json").write_text(json.dumps(
            {"claudeAiOauth": {"accessToken": "agent"}, "mcpOAuth": {"figma": {"accessToken": "UNRELATED"}}}))
        run_dir = self.tmp / "run"
        run_dir.mkdir()
        cfg, env, secret_env = gap_sandbox.agent_config(run_dir, source_home=fake_home)
        cmd = gap_sandbox.docker_command(["python3", str(probe_script)], name=gap_sandbox.new_name(), image=IMAGE,
                                         worktree=work, readonly_files=[probe_script], config_dir=cfg, extra_env=env,
                                         secret_env=secret_env)
        result = subprocess.run(cmd, capture_output=True, text=True,
                                env={"PATH": os.environ["PATH"], "GH_TOKEN": "leak", "API_GAP_BACKEND_TOKEN": "leak"})
        self.assertEqual(result.returncode, 0, result.stderr)
        seen = json.loads(result.stdout)
        self.assertEqual({k: seen[k] for k in ("home", "ssh", "claude_dir", "glab", "docker_sock", "www")},
                         dict.fromkeys(("home", "ssh", "claude_dir", "glab", "docker_sock", "www"), False))
        self.assertEqual((seen["write_worktree"], seen["write_etc"], seen["write_usr"]), (True, False, False))
        self.assertEqual(seen["tokens"], [])
        self.assertIn("CLAUDE_CODE_TMPDIR", seen["env"], "the agent's temp dir is private, never a host path")
        self.assertEqual(seen["login_entries"], ["claudeAiOauth"], "plugin/MCP tokens are never passed in")
        self.assertEqual(seen["uid"], os.getuid())
        self.assertEqual(seen["processes"], 1)

    def test_dispatch_runs_the_agent_inside_the_container(self):
        self.approve()
        self.mode.write_text("sandboxed")
        fake_home = self.tmp / "fakehome"
        (fake_home / ".claude").mkdir(parents=True)
        (fake_home / ".claude/.credentials.json").write_text(json.dumps({"claudeAiOauth": {"accessToken": "a"}}))
        with mock.patch.object(Path, "home", return_value=fake_home):
            outcome = self.dispatcher(sandbox_cfg=self.SANDBOX, template=self.template.replace(
                sys.executable, "python3")).run(1)
        self.assertEqual(outcome["status"], "MR_OPENED")
        self.assertIn("sandboxed", self.gl.notes(1)[0]["body"])
        import gap_dispatch
        self.assertFalse(list(gap_dispatch.secret_run_root(self.workdir).glob("gap-1/agent-config")),
                         "the login copy is removed afterwards")

    def test_timeout_kills_the_container(self):
        script = self.tmp / "sleeper.py"
        script.write_text("import time\ntime.sleep(120)\n")
        work = self.tmp / "wt2"
        work.mkdir()
        run_dir = self.tmp / "run2"
        run_dir.mkdir()
        fake_home = self.tmp / "fakehome2"
        (fake_home / ".claude").mkdir(parents=True)
        (fake_home / ".claude/.credentials.json").write_text(json.dumps({"claudeAiOauth": {"accessToken": "a"}}))
        import gap_dispatch
        with mock.patch.object(Path, "home", return_value=fake_home):
            with self.assertRaises(subprocess.TimeoutExpired):
                gap_dispatch.run_agent(["python3", str(script)], worktree=work, stdin_text="", timeout=3,
                                       sandbox_cfg=self.SANDBOX, run_dir=run_dir, readonly_files=[script])
        left = subprocess.run(["docker", "ps", "-q", "--filter", f"label={gap_sandbox.LABEL}=1"],
                              capture_output=True, text=True).stdout.split()
        self.assertEqual(left, [], "no agent container survives a timeout")

    def test_orphans_from_a_crashed_dispatcher_are_killed_by_recovery(self):
        orphan = subprocess.run(["docker", "run", "-d", "--rm", "--label", f"{gap_sandbox.LABEL}=1", IMAGE,
                                 "sleep", "120"], capture_output=True, text=True).stdout.strip()
        self.assertTrue(orphan)
        d = self.dispatcher(sandbox_cfg=self.SANDBOX)
        d.recover()
        for _ in range(20):
            alive = subprocess.run(["docker", "ps", "-q", "--filter", f"id={orphan}"], capture_output=True,
                                   text=True).stdout.strip()
            if not alive:
                break
            time.sleep(0.5)
        self.assertEqual(alive, "")

    def test_the_command_carries_an_in_container_hard_limit(self):
        cmd = gap_sandbox.docker_command(["python3", "x.py"], name="n", image=IMAGE, worktree=Path("/w"),
                                         readonly_files=[], config_dir=None, extra_env={}, max_seconds=100)
        self.assertEqual(cmd[cmd.index(IMAGE) + 1:cmd.index(IMAGE) + 5], ["timeout", "-s", "KILL", "130"])
        self.assertIn(f"{gap_sandbox.LABEL}=1", cmd)

    def test_verification_commands_share_one_container(self):
        work = self.tmp / "vw2"
        work.mkdir()
        results = gap_sandbox.run_verification(IMAGE, work, [
            "echo from-the-first > /tmp/shared.txt",
            "test \"$(cat /tmp/shared.txt)\" = from-the-first",
            "echo third",
        ], tools_dir=None, timeout=60)
        self.assertEqual([r["exit"] for r in results], [0, 0, 0], results)
        self.assertEqual(results[2]["output_tail"].strip(), "third")

    def test_a_container_that_cannot_start_is_reported_not_swallowed(self):
        work = self.tmp / "vw3"
        work.mkdir()
        results = gap_sandbox.run_verification("capitalix-gap-agent:does-not-exist", work, ["echo hi"], tools_dir=None, timeout=20)
        self.assertEqual(len(results), 1)
        self.assertNotEqual(results[0]["exit"], 0)
        self.assertEqual(results[0]["command"], "(container start)")

    def test_a_command_killed_by_the_time_limit_is_a_failure(self):
        work = self.tmp / "vw4"
        work.mkdir()
        results = gap_sandbox.run_verification(IMAGE, work, ["echo before", "sleep 30"], tools_dir=None, timeout=3)
        self.assertEqual(results[0]["exit"], 0)
        self.assertNotEqual(results[-1]["exit"], 0)

    def test_independent_verification_runs_in_a_fresh_container_without_network_or_secrets(self):
        work = self.tmp / "vw"
        work.mkdir()
        results = gap_sandbox.run_verification(IMAGE, work, [
            "echo ok > proof.txt",
            "python3 -c \"import os,sys; sys.exit(1 if [k for k in os.environ if k in ('GH_TOKEN','GITLAB_TOKEN','API_GAP_BACKEND_TOKEN','ANTHROPIC_API_KEY','CLAUDE_CODE_OAUTH_TOKEN','SSH_AUTH_SOCK')] else 0)\"",
            "python3 -c \"import socket; socket.create_connection(('1.1.1.1', 53), 3)\"",
        ], tools_dir=HERE.parent, timeout=60, memory="512m", cpus="1")
        self.assertEqual([r["exit"] for r in results[:2]], [0, 0])
        self.assertNotEqual(results[2]["exit"], 0, "no network inside verification")
        self.assertEqual((work / "proof.txt").read_text().strip(), "ok", "only the worktree is writable")
        self.assertEqual(len(gap_sandbox.run_verification(IMAGE, work, ["false", "echo never"], tools_dir=None,
                                                          timeout=30)), 1, "stops at the first failure")
        self.assertEqual(gap_sandbox.run_verification(IMAGE, work, ["test -f /opt/gap-tools/gap_core.py"],
                                                      tools_dir=HERE.parent, timeout=30)[0]["exit"], 0)
        self.assertNotEqual(gap_sandbox.run_verification(IMAGE, work, ["touch /opt/gap-tools/x"], tools_dir=HERE.parent,
                                                         timeout=30)[0]["exit"], 0, "tools are read-only")

    def verified_dispatcher(self, commands):
        return self.dispatcher(sandbox_cfg=self.SANDBOX, template=self.template.replace(sys.executable, "python3"),
                               verification={"commands": commands, "timeout_seconds": 60, "require_tests": False})

    def fake_login(self):
        fake_home = self.tmp / "fakehome3"
        (fake_home / ".claude").mkdir(parents=True, exist_ok=True)
        (fake_home / ".claude/.credentials.json").write_text(json.dumps({"claudeAiOauth": {"accessToken": "a" * 30}}))
        return mock.patch.object(Path, "home", return_value=fake_home)

    def test_a_change_that_fails_independent_verification_is_not_pushed_whatever_the_agent_says(self):
        self.approve()
        self.mode.write_text("sandboxed")
        with self.fake_login():
            with self.assertRaisesRegex(Refused, "independent verification failed"):
                self.verified_dispatcher(["python3 -c \"import sys; print('tests: 2 failed'); sys.exit(1)\""]).run(1)
        self.assertEqual(self.forge.opened, [])
        self.assertNotIn(f"gap/1-{self.fp[:16]}", self.remote_branches())
        self.assertIn("gap-dispatch::failed", self.gl.issues[1]["labels"])
        self.assertIn("2 failed", self.gl.notes(1)[-1]["body"])

    def test_a_change_that_passes_independent_verification_says_so_in_the_review(self):
        self.approve()
        self.mode.write_text("sandboxed")
        with self.fake_login():
            outcome = self.verified_dispatcher(["test -f app.txt", "python3 /opt/gap-tools/gap_core.py --help || true"]).run(1)
        self.assertEqual(outcome["status"], "MR_OPENED")
        self.assertIn("2 command(s) passed in a fresh container", self.forge.opened[0]["body"])

    def test_bundle_mode_pushes_nothing_and_leaves_a_verifiable_bundle_and_patch(self):
        self.approve()
        self.mode.write_text("sandboxed")
        forge = gap_dispatch.BundleForge(self.tmp / "reviews")
        d = self.dispatcher(sandbox_cfg=self.SANDBOX, template=self.template.replace(sys.executable, "python3"))
        d.forge = forge
        with self.fake_login():
            outcome = d.run(1)
        self.assertEqual(outcome["status"], "MR_OPENED")
        self.assertNotIn(f"gap/1-{self.fp[:16]}", self.remote_branches(), "the remote was never written")
        bundle = next((self.tmp / "reviews").glob("*.bundle"))
        verified = subprocess.run(["git", "bundle", "verify", str(bundle)], cwd=d.workdir / f"gap-1-{self.fp[:16]}",
                                  capture_output=True, text=True)
        self.assertEqual(verified.returncode, 0, verified.stderr)
        self.assertIn("app.txt", next((self.tmp / "reviews").glob("*.patch")).read_text())

    def test_unreachable_sandbox_blocks_dispatch_without_running_the_agent(self):
        self.approve()
        outcome = self.dispatcher(sandbox_cfg={"image": "capitalix-gap-agent:missing"}).run(1)
        self.assertEqual(outcome["status"], "BLOCKED_AGENT_RUNTIME")
        self.assertFalse(self.workdir.joinpath("gap-1-" + self.fp[:16]).exists())


if __name__ == "__main__":
    unittest.main()
