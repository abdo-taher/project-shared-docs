import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from fakes import LIST_OPERATION, contract, merge_paths, publish  # noqa: E402
from gap_contract import IntegrityError, PublishedContracts, evaluate_check  # noqa: E402


class PublishedContractTests(unittest.TestCase):

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.version, self.digest = publish(self.root, "2026.10.18", merge_paths(contract(), LIST_OPERATION))
        self.vdir = self.root / "api/implemented/versions" / self.version

    def contracts(self):
        return PublishedContracts(f"file:{self.root}")

    def test_verified_document(self):
        document = self.contracts().document(self.version)
        self.assertIn("/api/owner/sales/customers", document["paths"])

    def test_tampered_bytes(self):
        (self.vdir / "openapi.json").write_text("{}")
        with self.assertRaisesRegex(IntegrityError, "digest"):
            self.contracts().document(self.version)

    def test_approval_evidence_must_match(self):
        (self.vdir / "approval.json").write_text(json.dumps({"decision": "APPROVED"}))
        with self.assertRaisesRegex(IntegrityError, "approval"):
            self.contracts().document(self.version)

    def test_index_and_pointer_must_agree(self):
        pointer = self.root / "api/implemented/current.json"
        pointer.write_text(json.dumps({"version": self.version, "sha256": "0" * 64}))
        with self.assertRaisesRegex(IntegrityError, "current.json"):
            self.contracts().current()

    def test_unpublished_version(self):
        with self.assertRaisesRegex(IntegrityError, "not published"):
            self.contracts().manifest("2026.01.01-000000000000")

    def test_index_order(self):
        v2, _ = publish(self.root, "2026.10.20", contract(), commit="b" * 40)
        contracts = self.contracts()
        self.assertLess(contracts.position(self.version), contracts.position(v2))
        self.assertEqual(contracts.position("nope"), -1)

    def test_checks(self):
        document = self.contracts().document(self.version)
        op = "owner.sales.customers.index"
        holds = [{"check": "operation_exists", "operation_id": op},
                 {"check": "operation_exists", "method": "GET", "path": "/api/owner/sales/customers"},
                 {"check": "field_present", "operation_id": op, "field": "data.items[].name"},
                 {"check": "field_type", "operation_id": op, "field": "data.meta.total", "type": "integer"},
                 {"check": "field_required", "operation_id": "owner.sales.customers.store", "in": "request",
                  "field": "name"},
                 {"check": "parameter_present", "operation_id": op, "name": "page", "in": "query"}]
        fails = [{"check": "field_present", "operation_id": op, "field": "data.items[].email"},
                 {"check": "field_required", "operation_id": "owner.sales.customers.store", "in": "request",
                  "field": "phone"},
                 {"check": "parameter_required", "operation_id": op, "name": "page"},
                 {"check": "operation_exists", "operation_id": "owner.sales.customers.export"},
                 {"check": "__import__('os').system('id')"},
                 {"check": "field_type", "operation_id": op, "field": "data.meta.total", "type": "string"}]
        for check in holds:
            self.assertIsNone(evaluate_check(document, check), check)
        for check in fails:
            self.assertIsNotNone(evaluate_check(document, check), check)


class DocumentationCheckTests(unittest.TestCase):

    def doc(self, **op):
        return {"openapi": "3.1.0", "paths": {"/api/public/general/countries": {"get": {
            "operationId": "public.general.countries", "responses": {}, **op}}}}

    def test_summary_and_description_checks(self):
        bare, described = self.doc(), self.doc(summary="List the active countries",
                                              description="Names follow `Accept-Language`; cacheable for one hour.")
        has = {"check": "operation_has_summary", "operation_id": "public.general.countries"}
        mentions = {"check": "operation_description_contains", "operation_id": "public.general.countries",
                    "text": "Accept-Language"}
        self.assertIn("no summary", evaluate_check(bare, has))
        self.assertIsNone(evaluate_check(described, has))
        self.assertIn("does not mention", evaluate_check(bare, mentions))
        self.assertIsNone(evaluate_check(described, mentions))
        self.assertIn("does not mention", evaluate_check(described, {**mentions, "text": "max-age"}))
        self.assertIsNotNone(evaluate_check(described, {**mentions, "text": ""}))
        self.assertIsNotNone(evaluate_check(described, {**mentions, "text": "x" * 121}))
        self.assertIn("not in the contract", evaluate_check(described, {**has, "operation_id": "nope"}))
        self.assertIsNotNone(evaluate_check(self.doc(summary="   "), has), "blank is not a summary")

    def test_expect_failure_is_a_negative_control(self):
        import contextlib, io, json, tempfile
        import check_resolutions
        from gap_coordinator import RESOLUTION_SCHEMA
        fp = "d" * 64
        tmp = Path(tempfile.mkdtemp())
        (tmp / "res").mkdir()
        (tmp / "res" / f"{fp[:16]}.json").write_text(json.dumps({
            "schema": RESOLUTION_SCHEMA, "fingerprint": fp, "backend_issue": 1, "root_cause": "D", "summary": "s",
            "tests": ["t"], "checks": [{"check": "operation_has_summary", "operation_id": "public.general.countries"}]}))
        today, fixed = tmp / "today.json", tmp / "fixed.json"
        today.write_text(json.dumps(self.doc()))
        fixed.write_text(json.dumps(self.doc(summary="List the active countries")))
        run = lambda c, *extra: check_resolutions.main(["--dir", str(tmp / "res"), "--contract", str(c), *extra])
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(run(today, "--expect-failure"), 0, "fails today: the evidence shows the fix")
            self.assertEqual(run(fixed, "--expect-failure"), 1, "already holds: vacuous")
            self.assertEqual(run(fixed), 0)
            self.assertEqual(run(today), 1)


WORKFLOWS = ROOT / ".github/workflows"


def workflow(name: str) -> str:
    return (WORKFLOWS / name).read_text()


class WorkflowIsolationTests(unittest.TestCase):
    """The GitHub Actions side of the automation: inert until the owner enables it, never an agent, never a publisher."""

    def test_coordinator_is_manual_only_and_off_until_the_flag_is_true(self):
        text = workflow("api-gap-coordinator.yml")
        triggers = text.split("\non:")[1].split("\npermissions:")[0]
        self.assertIn("workflow_dispatch:", triggers)
        self.assertIsNone(re.search(r"(?m)^  (schedule|pull_request|push|issues|issue_comment|workflow_run):", triggers))
        self.assertIn("if: ${{ vars.API_GAP_AUTOMATION_ENABLED == 'true' }}", text)
        self.assertIn("environment: api-gap-coordinator", text)
        self.assertIn("group: api-gap-coordinator", text)

    def test_coordinator_has_read_only_repository_permissions(self):
        text = workflow("api-gap-coordinator.yml")
        self.assertRegex(text, r"(?m)^permissions:\n  contents: read\n")
        self.assertNotIn("write", text.split("jobs:")[0].split("permissions:")[1])

    def test_inputs_are_validated_not_evaluated(self):
        text = workflow("api-gap-coordinator.yml")
        self.assertIn('*[!0-9]*) echo "ERROR: issues takes issue numbers"; exit 3;;', text)
        self.assertNotIn("eval ", text)
        # untrusted inputs reach the shell only through environment variables, never interpolated into the script
        run_blocks = text.split("run: |")[1]
        self.assertNotIn("${{ inputs", run_blocks)

    def test_the_job_can_never_start_an_agent_or_publish(self):
        text = workflow("api-gap-coordinator.yml")
        for forbidden in ("gap_dispatch", "gap_worker", "CAPITALIX_GAP_EXECUTOR_CMD", "docker", "claude",
                          "API_GAP_DISPATCH_TOKEN", "API_GAP_AGENT", "gh pr merge", "contents: write"):
            self.assertNotIn(forbidden, text)
        self.assertIn("gap_preflight.py", text)

    def test_gap_credentials_are_used_only_by_the_coordinator_workflow(self):
        for path in WORKFLOWS.glob("*.yml"):
            if path.name == "api-gap-coordinator.yml":
                continue
            for secret in ("API_GAP_GITHUB_TOKEN", "API_GAP_BACKEND_TOKEN", "API_GAP_DISPATCH_TOKEN"):
                self.assertNotIn(secret, path.read_text(), path.name)

    def test_the_test_workflow_has_no_secrets_and_read_only_permissions(self):
        text = workflow("api-gap-automation-tests.yml")
        self.assertNotIn("secrets.", text)
        self.assertIn("contents: read", text)

    def test_existing_workflows_are_untouched_by_the_gap_automation(self):
        names = sorted(p.name for p in WORKFLOWS.glob("*.yml"))
        self.assertEqual(names, ["api-gap-automation-tests.yml", "api-gap-coordinator.yml", "contract-toolkit.yml"])


if __name__ == "__main__":
    unittest.main()
