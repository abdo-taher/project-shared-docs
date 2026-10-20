import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github/workflows"
BACKEND_BUILD = ROOT / "docs/api-gap/backend/contract-build.yml"


def text(name: str) -> str:
    return (WORKFLOWS / name).read_text()


def triggers(body: str) -> str:
    return body.split("\non:")[1].split("\npermissions:")[0]


class PublishWorkflowTests(unittest.TestCase):

    def test_publisher_is_manual_flag_gated_environment_reviewed_and_single(self):
        body = text("contract-publish.yml")
        self.assertIsNone(re.search(r"(?m)^  (schedule|push|pull_request|issues|workflow_run):", triggers(body)))
        self.assertIn("workflow_dispatch:", triggers(body))
        self.assertIn("if: ${{ vars.API_CONTRACT_PUBLICATION_ENABLED == 'true' }}", body)
        self.assertIn("environment: contract-publisher", body)
        self.assertIn("group: contract-publish", body)
        # nothing else may write api/implemented: only this workflow mentions the publisher entry point
        writers = [p.name for p in WORKFLOWS.glob("*.yml") if "capitalix_publish.py prepare" in p.read_text()]
        self.assertEqual(writers, ["contract-publish.yml"])

    def test_publisher_never_pushes_to_main_or_merges_or_forces(self):
        body = text("contract-publish.yml")
        for forbidden in ("push origin main", "HEAD:main", "--force", "-f origin", "gh pr merge", "--admin",
                          "auto-merge", "gh api -X PUT", "merge_method"):
            self.assertNotIn(forbidden, body)
        self.assertIn('branch="publish/$VERSION"', body)
        self.assertIn("refusing to overwrite", body)

    def test_publisher_tokens_are_short_lived_single_repository_and_minimal(self):
        body = text("contract-publish.yml")
        self.assertEqual(sorted(re.findall(r"(?m)^\s+repositories: (\S+)$", body)), ["capitalix", "project-shared-docs"])
        self.assertEqual(sorted(set(re.findall(r"secrets\.(\w+)", body))), ["API_GAP_APP_PRIVATE_KEY"])
        backend = body.split("id: backend")[1].split("- name: Verify the backend build")[0]
        self.assertNotIn("write", backend, "the backend token is read-only")
        self.assertNotIn("permission-administration", body)
        self.assertNotIn("permission-workflows", body)

    def test_inputs_reach_the_shell_only_through_environment_and_are_validated(self):
        body = text("contract-publish.yml")
        for block in re.findall(r"run: \|\n((?:\s{10}.*\n)+)", body):
            self.assertNotIn("${{ inputs", block)
            self.assertNotIn("${{ github.event", block)
        self.assertIn("build_run_id must be digits", body)
        self.assertNotIn("eval ", body)

    def test_every_action_is_pinned_by_commit_in_privileged_workflows(self):
        for name in ("contract-publish.yml", "contract-publication-verify.yml"):
            for ref in re.findall(r"(?m)^\s*(?:- )?uses: (\S+)", text(name)):
                self.assertRegex(ref, r"@[0-9a-f]{40}$", f"{name}: {ref}")
        for ref in re.findall(r"(?m)^\s*(?:- )?uses: (\S+)", BACKEND_BUILD.read_text()):
            self.assertRegex(ref, r"@[0-9a-f]{40}$", ref)

    def test_verify_workflow_is_secret_free_read_only_and_checks_both_pr_and_main(self):
        body = text("contract-publication-verify.yml")
        self.assertNotIn("secrets.", body)
        self.assertRegex(body, r"(?m)^permissions:\n  contents: read\n  pull-requests: read\n")
        self.assertIn("pull_request:", body)
        self.assertIn("verify-merge", body)
        self.assertIn("api/implemented/versions api/implemented/current.json api/implemented/index.json", body)
        self.assertIn("--max-new-versions 1", body)
        self.assertIn('"origin/$BASE_REF"', body)


class BackendBuildWorkflowTests(unittest.TestCase):

    def setUp(self):
        self.body = BACKEND_BUILD.read_text()

    def test_build_is_manual_read_only_and_limited_to_the_development_branch(self):
        self.assertIsNone(re.search(r"(?m)^  (schedule|push|pull_request):", triggers(self.body)))
        self.assertIn("workflow_dispatch:", triggers(self.body))
        self.assertRegex(self.body, r"(?m)^permissions:\n  contents: read\n")
        self.assertIn("github.ref == 'refs/heads/integration/E01-FOUNDATION-SAAS'", self.body)
        self.assertNotIn("secrets.", self.body)

    def test_build_is_deterministic_records_the_run_and_uploads_exactly_the_two_files(self):
        self.assertIn("cmp build/openapi-1.json build/openapi-2.json", self.body)
        self.assertIn("name: contract-build", self.body)
        self.assertIn("build/out/openapi.json", self.body)
        self.assertIn("build/out/build-record.json", self.body)
        self.assertIn("capitalix-contract-build/1", self.body)
        self.assertIn("github.run_id", self.body)

    def test_workflow_file_name_matches_what_the_publisher_verifies(self):
        sys_path = ROOT / "tools/publish/capitalix_publish.py"
        self.assertIn('BUILD_WORKFLOW = ".github/workflows/contract-build.yml"', sys_path.read_text())
        self.assertTrue(self.body.startswith("name: contract-build"))


class AutoReleaseWorkflowTests(unittest.TestCase):

    def test_release_listener_is_gated_and_cannot_publish_approve_or_merge(self):
        body = text("contract-release.yml")
        self.assertIn("vars.API_CONTRACT_AUTO_RELEASE == 'true'", body)
        self.assertIn("vars.API_CONTRACT_PUBLICATION_ENABLED == 'true'", body)
        self.assertIn("environment: contract-release", body)
        self.assertIn("schedule:", triggers(body))
        self.assertIn("group: contract-release", body)
        code = "\n".join(ln.split(" #")[0] for ln in body.splitlines() if not ln.lstrip().startswith("#"))
        for forbidden in ("pr merge", "pr review", "--admin", "allow_breaking", "allow_unknown", "capitalix_publish.py",
                          "git push", "contents: write"):
            self.assertNotIn(forbidden, code)

    def test_only_the_publisher_workflow_writes_published_versions(self):
        writers = [p.name for p in WORKFLOWS.glob("*.yml") if "capitalix_publish.py prepare" in p.read_text()]
        self.assertEqual(writers, ["contract-publish.yml"])

    def test_owner_hand_offs_are_reported_by_the_workflow_that_reaches_them(self):
        publish, verify = text("contract-publish.yml"), text("contract-publication-verify.yml")
        self.assertIn("ACTION NEEDED", publish)
        self.assertIn("Tell the owner (stopped)", publish)
        self.assertIn("Published:", verify)
        self.assertIn("issues: write", verify)


if __name__ == "__main__":
    unittest.main()
