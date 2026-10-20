import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

COMPAT = Path(__file__).resolve().parents[1] / "publish" / "openapi_compatibility.py"


def operation_id_doc(op_id, path="/api/owner/things", verb="get", responses=None,
                     summary=None, tags=None):
    operation = {
        "operationId": op_id,
        "tags": tags or ["Owner / Things"],
        "responses": responses or {"200": {"description": "Success."}},
        "security": [{"sanctumBearer": []}],
    }
    if summary is not None:
        operation["summary"] = summary
    return {
        "openapi": "3.1.0",
        "info": {"title": "Capitalix API", "version": "1.0.0"},
        "paths": {path: {verb: operation}},
        "components": {
            "securitySchemes": {
                "sanctumBearer": {"type": "http", "scheme": "bearer"}
            }
        },
    }


class CompatibilityToolTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write_doc(self, name, doc):
        target = self.dir / name
        target.write_text(json.dumps(doc, indent=2))
        return target

    def run_compat(self, baseline, candidate, *extra):
        return subprocess.run(
            [sys.executable, str(COMPAT),
             "--baseline", str(baseline),
             "--candidate", str(candidate),
             *extra],
            text=True, capture_output=True,
        )

    def changes_of(self, json_path):
        return json.loads(json_path.read_text())["changes"]

    def codes_of(self, json_path):
        return {c["kind"] for c in self.changes_of(json_path)}

    def test_identical_documents_are_compatible(self):
        doc = operation_id_doc("owner.things.index")
        baseline = self.write_doc("baseline.json", doc)
        candidate = self.write_doc("candidate.json", doc)
        out = self.dir / "report.json"

        result = self.run_compat(baseline, candidate,
                                 "--fail-on-breaking", "--fail-on-unknown",
                                 "--json-out", str(out))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.changes_of(out), [])

    def test_removed_operation_is_breaking(self):
        baseline = self.write_doc("baseline.json",
                                  operation_id_doc("owner.things.index"))
        candidate_doc = operation_id_doc("owner.things.index")
        candidate_doc["paths"] = {}
        candidate = self.write_doc("candidate.json", candidate_doc)
        out = self.dir / "report.json"

        result = self.run_compat(baseline, candidate,
                                 "--fail-on-breaking", "--json-out", str(out))

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("operation_removed", self.codes_of(out))

    def test_removed_4xx_status_is_documentation_only(self):
        baseline = self.write_doc(
            "baseline.json",
            operation_id_doc("owner.things.index", responses={
                "200": {"description": "ok"},
                "404": {"description": "not found"}}))
        candidate = self.write_doc(
            "candidate.json",
            operation_id_doc("owner.things.index", responses={
                "200": {"description": "ok"}}))
        out = self.dir / "report.json"

        result = self.run_compat(baseline, candidate,
                                 "--fail-on-breaking", "--fail-on-unknown",
                                 "--json-out", str(out))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(out.read_text())
        self.assertGreater(report["summary"]["DOCUMENTATION_ONLY"], 0)

    def test_operation_id_change_is_breaking(self):
        baseline = self.write_doc("baseline.json",
                                  operation_id_doc("owner.things.index"))
        candidate = self.write_doc("candidate.json",
                                   operation_id_doc("owner.things.reindex"))
        out = self.dir / "report.json"

        result = self.run_compat(baseline, candidate,
                                 "--fail-on-breaking", "--json-out", str(out))

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        codes = self.codes_of(out)
        self.assertTrue(any("operation_id" in c for c in codes), codes)
        report = json.loads(out.read_text())
        self.assertEqual(report["summary"]["BREAKING"],
                         len(report["changes"]))

    def test_added_operation_is_non_breaking(self):
        baseline = self.write_doc("baseline.json",
                                  operation_id_doc("owner.things.index"))
        candidate_doc = operation_id_doc("owner.things.index")
        candidate_doc["paths"]["/api/owner/other"] = {
            "post": {"operationId": "owner.other.store",
                     "tags": ["Owner / Other"],
                     "responses": {"201": {"description": "Created."}}}
        }
        candidate = self.write_doc("candidate.json", candidate_doc)
        out = self.dir / "report.json"

        result = self.run_compat(baseline, candidate,
                                 "--fail-on-breaking", "--fail-on-unknown",
                                 "--json-out", str(out))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(out.read_text())
        self.assertGreater(report["summary"]["NON_BREAKING"], 0)

    def test_new_required_response_field_is_breaking(self):
        baseline = self.write_doc(
            "baseline.json",
            operation_id_doc("owner.things.index", responses={
                "200": {"description": "ok", "content": {
                    "application/json": {"schema": {"type": "object",
                                                    "properties": {"id": {"type": "integer"}}}}}}}))
        candidate = self.write_doc(
            "candidate.json",
            operation_id_doc("owner.things.index", responses={
                "200": {"description": "ok", "content": {
                    "application/json": {"schema": {"type": "object",
                                                    "required": ["audit_id"],
                                                    "properties": {"id": {"type": "integer"},
                                                                   "audit_id": {"type": "string"}}}}}}}))
        out = self.dir / "report.json"

        result = self.run_compat(baseline, candidate,
                                 "--fail-on-breaking", "--json-out", str(out))

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        codes = self.codes_of(out)
        self.assertTrue(any("required" in c for c in codes), codes)

    def test_removed_5xx_status_is_documentation_only(self):
        baseline = self.write_doc(
            "baseline.json",
            operation_id_doc("owner.things.index", responses={
                "200": {"description": "ok"},
                "500": {"description": "server error"}}))
        candidate = self.write_doc(
            "candidate.json",
            operation_id_doc("owner.things.index", responses={
                "200": {"description": "ok"}}))
        out = self.dir / "report.json"

        result = self.run_compat(baseline, candidate,
                                 "--fail-on-breaking", "--json-out", str(out))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(out.read_text())
        self.assertGreater(report["summary"]["DOCUMENTATION_ONLY"], 0)

    def test_shared_component_removal_reports_blast_radius(self):
        baseline_doc = operation_id_doc("owner.things.index")
        baseline_doc["components"]["schemas"] = {
            "LoginRequest": {"type": "object",
                             "properties": {"email": {"type": "string"}}}}
        baseline_doc["paths"]["/api/owner/things"]["get"]["responses"]["200"] = {
            "content": {"application/json": {
                "schema": {"$ref": "#/components/schemas/LoginRequest"}}}}
        baseline = self.write_doc("baseline.json", baseline_doc)

        candidate_doc = operation_id_doc("owner.things.index")
        candidate_doc["paths"]["/api/owner/things"]["get"]["responses"]["200"] = {
            "content": {"application/json": {
                "schema": {"type": "object",
                           "properties": {"email": {"type": "string"}}}}}}
        candidate = self.write_doc("candidate.json", candidate_doc)
        out = self.dir / "report.json"

        result = self.run_compat(baseline, candidate,
                                 "--fail-on-breaking", "--json-out", str(out))

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        report = json.loads(out.read_text())
        shared = [c for c in report["changes"]
                  if c["kind"] == "shared_component_removed"]
        self.assertEqual(len(shared), 1)
        self.assertGreaterEqual(len(shared[0].get("affected_operations") or []), 1)

    def test_security_scheme_change_is_breaking(self):
        baseline = self.write_doc("baseline.json",
                                  operation_id_doc("owner.things.index"))
        candidate_doc = operation_id_doc("owner.things.index")
        candidate_doc["components"]["securitySchemes"]["sanctumBearer"] = {
            "type": "apiKey", "name": "X-Custom", "in": "header"}
        candidate = self.write_doc("candidate.json", candidate_doc)
        out = self.dir / "report.json"

        result = self.run_compat(baseline, candidate,
                                 "--fail-on-breaking", "--json-out", str(out))

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("security_scheme_changed", self.codes_of(out))

    def test_unknown_classification_fails_closed_with_precedence(self):
        baseline = self.write_doc(
            "baseline.json",
            operation_id_doc("owner.things.index", responses={
                "200": {"description": "ok",
                        "content": {"application/json": {
                            "schema": {"oneOf": [{"type": "object"},
                                                 {"type": "array"}]}}}}}))
        candidate = self.write_doc(
            "candidate.json",
            operation_id_doc("owner.things.index", responses={
                "200": {"description": "ok",
                        "content": {"application/json": {
                            "schema": {"oneOf": [{"type": "object"},
                                                 {"type": "string"}]}}}}}))
        out = self.dir / "report.json"

        result = self.run_compat(baseline, candidate,
                                 "--fail-on-breaking", "--fail-on-unknown",
                                 "--json-out", str(out))

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("UNKNOWN", json.loads(out.read_text())["summary"])

    def test_unknown_takes_precedence_over_breaking(self):
        baseline_doc = operation_id_doc("owner.things.index", responses={
            "200": {"description": "ok",
                    "content": {"application/json": {
                        "schema": {"oneOf": [{"type": "object"},
                                             {"type": "array"}]}}}}})
        baseline_doc["paths"]["/api/owner/things"]["get"]["responses"]["418"] = {
            "description": "teapot"}
        baseline = self.write_doc("baseline.json", baseline_doc)
        candidate = self.write_doc("candidate.json", {
            "openapi": "3.1.0",
            "info": {"title": "Capitalix API", "version": "1.0.0"},
            "paths": {"/api/owner/things": {"get": {
                "operationId": "owner.things.index",
                "tags": ["Owner / Things"],
                "responses": {"200": {"description": "ok", "content": {
                    "application/json": {"schema": {
                        "oneOf": [{"type": "object"}, {"type": "string"}]}}}}},
                "security": [{"sanctumBearer": []}]}}},
            "components": {"securitySchemes": {
                "sanctumBearer": {"type": "http", "scheme": "bearer"}}},
        })
        out = self.dir / "report.json"

        result = self.run_compat(baseline, candidate,
                                 "--fail-on-breaking", "--fail-on-unknown",
                                 "--json-out", str(out))

        self.assertEqual(result.returncode, 2,
                         "UNKNOWN must win over BREAKING: " + result.stderr)

    def test_markdown_report_is_written(self):
        doc = operation_id_doc("owner.things.index")
        baseline = self.write_doc("baseline.json", doc)
        candidate = self.write_doc("candidate.json", doc)
        md = self.dir / "report.md"

        result = self.run_compat(baseline, candidate, "--markdown-out", str(md))

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("OpenAPI Contract Compatibility", md.read_text())

    def test_missing_baseline_is_input_error(self):
        candidate = self.write_doc("candidate.json",
                                   operation_id_doc("owner.things.index"))
        result = self.run_compat(self.dir / "absent.json", candidate)

        self.assertEqual(result.returncode, 3, result.stdout + result.stderr)

    def test_real_repository_documents_produce_expected_report(self):
        repo = Path(__file__).resolve().parents[3]
        baseline = repo / "docs" / "api" / "openapi.json"
        if not baseline.exists():
            self.skipTest("committed contract not present")
        out = self.dir / "report.json"

        result = self.run_compat(baseline, baseline,
                                 "--fail-on-breaking", "--fail-on-unknown",
                                 "--json-out", str(out))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(out.read_text())["changes"], [])


if __name__ == "__main__":
    unittest.main()
