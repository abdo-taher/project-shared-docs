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



def schema_doc(response_schema=None, request_schema=None, schemas=None):
    """One POST operation whose response and/or request body carry the given schemas."""
    operation = {
        "operationId": "owner.things.store",
        "tags": ["Owner / Things"],
        "responses": {"200": {"description": "ok"}},
        "security": [{"sanctumBearer": []}],
    }
    if response_schema is not None:
        operation["responses"]["200"]["content"] = {
            "application/json": {"schema": response_schema}}
    if request_schema is not None:
        operation["requestBody"] = {"required": True, "content": {
            "application/json": {"schema": request_schema}}}
    return {
        "openapi": "3.1.0",
        "info": {"title": "Capitalix API", "version": "1.0.0"},
        "paths": {"/api/owner/things": {"post": operation}},
        "components": {
            "schemas": schemas or {},
            "securitySchemes": {"sanctumBearer": {"type": "http", "scheme": "bearer"}},
        },
    }


def envelope(data_schema):
    return {"allOf": [{"$ref": "#/components/schemas/SuccessEnvelope"},
                      {"type": "object", "properties": {"data": data_schema}}]}


ENVELOPE_COMPONENT = {"SuccessEnvelope": {"type": "object", "required": ["success"],
                                          "properties": {"success": {"type": "boolean"}}}}


class SchemaRuleTests(unittest.TestCase):
    """Classification of schema rewrites that used to fall through to UNKNOWN."""

    def report(self, baseline, candidate):
        sys.path.insert(0, str(COMPAT.parent))
        try:
            import openapi_compatibility as compat
        finally:
            sys.path.pop(0)
        return compat.build_report(baseline, candidate, "baseline", "candidate")

    def by_category(self, report):
        result = {}
        for change in report["changes"]:
            result.setdefault(change["category"], set()).add(change["kind"])
        return result

    def response_pair(self, before, after, schemas=None):
        return self.report(schema_doc(response_schema=before, schemas=schemas),
                           schema_doc(response_schema=after, schemas=schemas))

    def request_pair(self, before, after, schemas=None):
        return self.report(schema_doc(request_schema=before, schemas=schemas),
                           schema_doc(request_schema=after, schemas=schemas))

    # -- allOf / anyOf member-wise comparison --------------------------------

    def test_envelope_allof_with_added_optional_field_is_non_breaking(self):
        before = envelope({"type": "object", "properties": {"id": {"type": "string"}}})
        after = envelope({"type": "object", "properties": {"id": {"type": "string"},
                                                           "name": {"type": "string"}}})
        report = self.response_pair(before, after, ENVELOPE_COMPONENT)

        self.assertEqual(self.by_category(report), {"NON_BREAKING": {"response_schema_field_added"}})
        self.assertEqual(report["changes"][0]["location"],
                         "paths./api/owner/things.post.responses.200.content.application/json"
                         ".schema.allOf[1].properties.data.properties.name")

    def test_envelope_allof_with_changed_field_type_is_breaking_not_unknown(self):
        before = envelope({"type": "object", "properties": {"id": {"type": "integer"}}})
        after = envelope({"type": "object", "properties": {"id": {"type": "string"}}})

        categories = self.by_category(self.response_pair(before, after, ENVELOPE_COMPONENT))

        self.assertEqual(categories, {"BREAKING": {"response_schema_type_changed"}})

    def test_unchanged_shared_allof_member_is_left_to_the_component_diff(self):
        before = envelope({"type": "string"})
        after = envelope({"type": "string", "description": "x"})
        changed = {"SuccessEnvelope": {"type": "object", "properties": {"success": {"type": "boolean"}}}}

        report = self.report(schema_doc(response_schema=before, schemas=ENVELOPE_COMPONENT),
                             schema_doc(response_schema=after, schemas=changed))

        locations = [c["location"] for c in report["changes"] if c["category"] != "DOCUMENTATION_ONLY"]
        self.assertEqual(locations, ["components.schemas.SuccessEnvelope.properties.success"])

    def test_allof_member_count_change_still_fails_closed(self):
        before = envelope({"type": "string"})
        after = {"allOf": before["allOf"] + [{"type": "object"}]}

        categories = self.by_category(self.response_pair(before, after, ENVELOPE_COMPONENT))

        self.assertEqual(categories, {"UNKNOWN": {"response_schema_allOf_changed"}})

    def test_anyof_members_are_compared_pairwise(self):
        before = {"anyOf": [{"type": "object", "properties": {"a": {"type": "string"}}},
                            {"type": "array", "items": {}}]}
        after = {"anyOf": [{"type": "object", "properties": {"a": {"type": ["string", "null"]}}},
                           {"type": "array", "items": {}}]}

        categories = self.by_category(self.response_pair(before, after))

        self.assertEqual(categories, {"NON_BREAKING": {"response_schema_nullability_added"}})

    def test_oneof_pairwise_rewrite_stays_unknown(self):
        before = {"oneOf": [{"type": "object", "properties": {"a": {"type": "string"}}}, {"type": "array"}]}
        after = {"oneOf": [{"type": "object", "properties": {"a": {"type": ["string", "null"]}}}, {"type": "array"}]}

        categories = self.by_category(self.response_pair(before, after))

        self.assertEqual(categories, {"UNKNOWN": {"response_schema_oneOf_changed"}})

    # -- nullable anyOf spelling ---------------------------------------------

    def test_nullable_anyof_ref_equals_inline_nullable_enum(self):
        schemas = {"Status": {"type": "string", "enum": ["open", "closed"]}}
        before = {"type": "object", "properties": {"status": {
            "anyOf": [{"$ref": "#/components/schemas/Status"}, {"type": "null"}]}}}
        after = {"type": "object", "properties": {"status": {
            "type": ["string", "null"], "enum": ["open", "closed", None]}}}

        categories = self.by_category(self.request_pair(before, after, schemas))

        self.assertEqual(set(categories) - {"DOCUMENTATION_ONLY"}, set())

    def test_nullable_anyof_collapse_still_reports_enum_differences(self):
        schemas = {"Status": {"type": "string", "enum": ["OPEN", "CLOSED"]}}
        before = {"anyOf": [{"$ref": "#/components/schemas/Status"}, {"type": "null"}]}
        after = {"type": ["string", "null"], "enum": ["open", None]}

        categories = self.by_category(self.request_pair(before, after, schemas))

        self.assertEqual(categories["BREAKING"], {"request_schema_enum_value_removed"})
        self.assertEqual(categories["NON_BREAKING"], {"request_schema_enum_value_added"})

    def test_ref_becoming_nullable_anyof_is_nullability_added(self):
        schemas = {"Kind": {"type": "string", "enum": ["a", "b"]}}
        before = {"$ref": "#/components/schemas/Kind"}
        after = {"anyOf": [{"$ref": "#/components/schemas/Kind"}, {"type": "null"}]}

        categories = self.by_category(self.request_pair(before, after, schemas))

        self.assertNotIn("UNKNOWN", categories)
        self.assertNotIn("BREAKING", categories)
        self.assertIn("request_schema_nullability_added", categories["NON_BREAKING"])

    # -- enum added / removed --------------------------------------------------

    def test_enum_added_to_request_is_breaking(self):
        categories = self.by_category(self.request_pair(
            {"type": "string"}, {"type": "string", "enum": ["faq", "terms"]}))
        self.assertEqual(categories, {"BREAKING": {"request_schema_enum_added"}})

    def test_enum_added_to_response_is_non_breaking(self):
        categories = self.by_category(self.response_pair(
            {"type": "string"}, {"type": "string", "enum": ["faq", "terms"]}))
        self.assertEqual(categories, {"NON_BREAKING": {"response_schema_enum_added"}})

    def test_enum_removed_from_response_is_breaking(self):
        categories = self.by_category(self.response_pair(
            {"type": "string", "enum": ["faq"]}, {"type": "string"}))
        self.assertEqual(categories, {"BREAKING": {"response_schema_enum_removed"}})

    # -- bounds and pattern ----------------------------------------------------

    def test_request_max_length_decrease_is_breaking(self):
        categories = self.by_category(self.request_pair(
            {"type": "string", "maxLength": 512}, {"type": "string", "maxLength": 255}))
        self.assertEqual(categories, {"BREAKING": {"request_schema_constraint_narrowed"}})

    def test_request_max_length_added_is_breaking_and_removed_is_not(self):
        added = self.by_category(self.request_pair({"type": "string"}, {"type": "string", "maxLength": 64}))
        removed = self.by_category(self.request_pair({"type": "string", "maxLength": 64}, {"type": "string"}))
        self.assertEqual(added, {"BREAKING": {"request_schema_constraint_narrowed"}})
        self.assertEqual(removed, {"NON_BREAKING": {"request_schema_constraint_widened"}})

    def test_response_bound_widening_is_breaking(self):
        categories = self.by_category(self.response_pair(
            {"type": "array", "items": {}, "maxItems": 5}, {"type": "array", "items": {}}))
        self.assertEqual(categories, {"BREAKING": {"response_schema_constraint_widened"}})

    def test_restating_the_default_bound_is_documentation_only(self):
        categories = self.by_category(self.request_pair(
            {"type": "array", "items": {}}, {"type": "array", "items": {}, "minItems": 0}))
        self.assertEqual(categories, {"DOCUMENTATION_ONLY": {"request_schema_constraint_restated"}})

    def test_non_numeric_bound_stays_unknown(self):
        categories = self.by_category(self.request_pair(
            {"type": "string", "maxLength": 5}, {"type": "string", "maxLength": "5"}))
        self.assertEqual(categories, {"UNKNOWN": {"request_schema_keyword_changed"}})

    def test_replaced_pattern_is_breaking_in_both_directions(self):
        before = {"type": "string", "pattern": "^[a-z]+$"}
        after = {"type": "string", "pattern": "^[A-Za-z]+$"}
        self.assertEqual(self.by_category(self.request_pair(before, after)),
                         {"BREAKING": {"request_schema_pattern_changed"}})
        self.assertEqual(self.by_category(self.response_pair(before, after)),
                         {"BREAKING": {"response_schema_pattern_changed"}})

    def test_request_pattern_removed_is_non_breaking(self):
        categories = self.by_category(self.request_pair(
            {"type": "string", "pattern": "^[A-Za-z0-9:._-]+$"}, {"type": "string"}))
        self.assertEqual(categories, {"NON_BREAKING": {"request_schema_pattern_removed"}})

    # -- format added / removed ------------------------------------------------

    def test_response_format_removed_is_breaking(self):
        categories = self.by_category(self.response_pair(
            {"type": "string", "format": "date-time"}, {"type": "string"}))
        self.assertEqual(categories, {"BREAKING": {"response_schema_format_removed"}})

    def test_request_format_removed_is_non_breaking(self):
        categories = self.by_category(self.request_pair(
            {"type": "string", "format": "uuid"}, {"type": "string"}))
        self.assertEqual(categories, {"NON_BREAKING": {"request_schema_format_removed"}})

    # -- absent type -----------------------------------------------------------

    def test_type_added_to_untyped_schema_depends_on_direction(self):
        before, after = {"type": "array", "items": {}}, {"type": "array", "items": {"type": "object"}}
        self.assertEqual(self.by_category(self.response_pair(before, after)),
                         {"NON_BREAKING": {"response_schema_type_added"}})
        self.assertEqual(self.by_category(self.request_pair(before, after)),
                         {"BREAKING": {"request_schema_type_added"}})

    # -- still fail closed -----------------------------------------------------

    def test_unrecognized_keyword_still_fails_closed(self):
        categories = self.by_category(self.response_pair(
            {"type": "array", "items": {}}, {"type": "array", "items": {}, "prefixItems": [{"type": "string"}]}))
        self.assertEqual(categories, {"UNKNOWN": {"response_schema_keyword_changed"}})


if __name__ == "__main__":
    unittest.main()
