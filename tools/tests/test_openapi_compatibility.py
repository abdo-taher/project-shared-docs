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

    def test_new_required_response_field_is_non_breaking(self):
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

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual([(c["category"], c["kind"]) for c in self.changes_of(out)],
                         [("NON_BREAKING", "response_schema_required_field_added")])

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

        self.assertEqual(categories, {"BREAKING": {"response_schema_nullability_added"}})

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

    # -- one rule for requests and responses -----------------------------------

    def test_required_field_added_breaks_requests_not_responses(self):
        before = {"type": "object", "properties": {"id": {"type": "string"}}}
        after = {"type": "object", "required": ["code"],
                 "properties": {"id": {"type": "string"}, "code": {"type": "string"}}}
        self.assertEqual(self.by_category(self.request_pair(before, after)),
                         {"BREAKING": {"request_schema_required_field_added"}})
        self.assertEqual(self.by_category(self.response_pair(before, after)),
                         {"NON_BREAKING": {"response_schema_required_field_added"}})

    def test_field_becoming_optional_breaks_responses_not_requests(self):
        before = {"type": "object", "required": ["id"], "properties": {"id": {"type": "string"}}}
        after = {"type": "object", "properties": {"id": {"type": "string"}}}
        self.assertEqual(self.by_category(self.response_pair(before, after)),
                         {"BREAKING": {"response_schema_field_became_optional"}})
        self.assertEqual(self.by_category(self.request_pair(before, after)),
                         {"NON_BREAKING": {"request_schema_field_became_optional"}})

    def test_field_becoming_required_breaks_requests_not_responses(self):
        before = {"type": "object", "properties": {"id": {"type": "string"}}}
        after = {"type": "object", "required": ["id"], "properties": {"id": {"type": "string"}}}
        self.assertEqual(self.by_category(self.request_pair(before, after)),
                         {"BREAKING": {"request_schema_field_became_required"}})
        self.assertEqual(self.by_category(self.response_pair(before, after)),
                         {"NON_BREAKING": {"response_schema_field_became_required"}})

    def test_null_newly_returned_is_breaking_and_newly_accepted_is_not(self):
        before, after = {"type": "string"}, {"type": ["string", "null"]}
        self.assertEqual(self.by_category(self.response_pair(before, after)),
                         {"BREAKING": {"response_schema_nullability_added"}})
        self.assertEqual(self.by_category(self.request_pair(before, after)),
                         {"NON_BREAKING": {"request_schema_nullability_added"}})

    def test_openapi_30_nullable_flag_follows_the_same_rule(self):
        before, after = {"type": "string"}, {"type": "string", "nullable": True}
        self.assertEqual(self.by_category(self.response_pair(before, after)),
                         {"BREAKING": {"response_schema_nullable_changed"}})
        self.assertEqual(self.by_category(self.request_pair(before, after)),
                         {"NON_BREAKING": {"request_schema_nullable_changed"}})

    def test_shared_schema_used_both_ways_breaks_either_way(self):
        schemas = {"Thing": {"type": "object", "properties": {"id": {"type": "string"}}}}
        changed = {"Thing": {"type": "object", "required": ["code"],
                             "properties": {"id": {"type": "string"}, "code": {"type": "string"}}}}
        ref = {"$ref": "#/components/schemas/Thing"}
        report = self.report(schema_doc(response_schema=ref, request_schema=ref, schemas=schemas),
                             schema_doc(response_schema=ref, request_schema=ref, schemas=changed))
        self.assertEqual(self.by_category(report), {"BREAKING": {"component_schema_required_field_added"}})

    def test_component_nested_in_a_request_through_another_component_counts_as_request(self):
        schemas = {"Line": {"type": "object", "properties": {"id": {"type": "string"}}},
                   "Order": {"type": "object", "properties": {"lines": {
                       "type": "array", "items": {"$ref": "#/components/schemas/Line"}}}}}
        changed = {**schemas, "Line": {"type": "object", "required": ["sku"],
                                       "properties": {"id": {"type": "string"}, "sku": {"type": "string"}}}}
        before = schema_doc(response_schema={"$ref": "#/components/schemas/Line"},
                            request_schema={"$ref": "#/components/schemas/Order"}, schemas=schemas)
        after = schema_doc(response_schema={"$ref": "#/components/schemas/Line"},
                           request_schema={"$ref": "#/components/schemas/Order"}, schemas=changed)

        self.assertEqual(self.by_category(self.report(before, after)),
                         {"BREAKING": {"component_schema_required_field_added"}})

    def test_unreferenced_component_is_judged_strictly(self):
        schemas = {"Orphan": {"type": "object", "properties": {"id": {"type": "string"}}}}
        changed = {"Orphan": {"type": "object", "required": ["id"], "properties": {"id": {"type": "string"}}}}
        report = self.report(schema_doc(schemas=schemas), schema_doc(schemas=changed))
        self.assertEqual(self.by_category(report), {"BREAKING": {"component_schema_field_became_required"}})

    # -- still fail closed -----------------------------------------------------

    def test_unrecognized_keyword_still_fails_closed(self):
        categories = self.by_category(self.response_pair(
            {"type": "array", "items": {}}, {"type": "array", "items": {}, "uniqueItems": True}))
        self.assertEqual(categories, {"UNKNOWN": {"response_schema_keyword_changed"}})

    # -- const: a one-value set ------------------------------------------------

    def test_response_const_added_inside_the_accepted_values_is_non_breaking(self):
        categories = self.by_category(self.response_pair(
            {"type": "integer"}, {"type": "integer", "const": 0}))
        self.assertEqual(categories, {"NON_BREAKING": {"response_schema_const_added"}})

    def test_request_const_added_is_breaking(self):
        categories = self.by_category(self.request_pair(
            {"type": "integer"}, {"type": "integer", "const": 0}))
        self.assertEqual(categories, {"BREAKING": {"request_schema_const_added"}})

    def test_response_const_removed_is_breaking(self):
        categories = self.by_category(self.response_pair(
            {"type": "integer", "const": 0}, {"type": "integer"}))
        self.assertEqual(categories, {"BREAKING": {"response_schema_const_removed"}})

    def test_request_const_removed_is_non_breaking(self):
        categories = self.by_category(self.request_pair(
            {"type": "integer", "const": 0}, {"type": "integer"}))
        self.assertEqual(categories, {"NON_BREAKING": {"request_schema_const_removed"}})

    def test_const_added_to_a_shared_component_is_breaking(self):
        schemas = {"Count": {"type": "integer"}}
        narrowed = {"Count": {"type": "integer", "const": 0}}
        report = self.report(schema_doc(schemas=schemas), schema_doc(schemas=narrowed))
        self.assertEqual(self.by_category(report), {"BREAKING": {"component_schema_const_added"}})

    def test_replaced_const_value_is_breaking_in_both_directions(self):
        before, after = {"type": "integer", "const": 0}, {"type": "integer", "const": 1}
        self.assertEqual(self.by_category(self.request_pair(before, after)),
                         {"BREAKING": {"request_schema_const_changed"}})
        self.assertEqual(self.by_category(self.response_pair(before, after)),
                         {"BREAKING": {"response_schema_const_changed"}})

    def test_const_outside_the_previous_values_is_breaking_not_narrowing(self):
        for before, value in (({"type": "integer"}, "zero"),
                              ({"type": "integer", "maximum": 5}, 9),
                              ({"type": "string", "enum": ["a", "b"]}, "c"),
                              ({"type": "string", "minLength": 3}, "ab"),
                              ({"type": "string", "pattern": "^[0-9]+$"}, "abc")):
            with self.subTest(before=before, value=value):
                after = {**before, "const": value}
                self.assertEqual(self.by_category(self.response_pair(before, after)),
                                 {"BREAKING": {"response_schema_const_changed"}})

    def test_const_that_cannot_be_checked_against_the_previous_schema_is_unknown(self):
        for before in ({"anyOf": [{"type": "integer"}, {"type": "string"}]},
                       {"type": "string", "format": "date-time"},
                       {"type": "integer", "multipleOf": 2}):
            with self.subTest(before=before):
                after = {**before, "const": 0 if before.get("type") != "string" else "2020-01-01T00:00:00Z"}
                self.assertEqual(self.by_category(self.response_pair(before, after)),
                                 {"UNKNOWN": {"response_schema_const_changed"}})

    def test_const_null_is_a_value_not_an_absent_keyword(self):
        categories = self.by_category(self.response_pair(
            {"type": ["string", "null"]}, {"type": ["string", "null"], "const": None}))
        self.assertEqual(categories, {"NON_BREAKING": {"response_schema_const_added"}})

    def test_const_zero_and_false_are_different_values(self):
        categories = self.by_category(self.response_pair(
            {"type": "integer", "const": 0}, {"type": "boolean", "const": False}))
        self.assertIn("response_schema_const_changed", categories["BREAKING"])

    # -- prefixItems: tuple arrays ---------------------------------------------

    TUPLE = {"type": "array", "minItems": 2, "maxItems": 2}

    def tuple_of(self, first, second):
        return {**self.TUPLE, "prefixItems": [first, second]}

    def test_response_tuple_position_narrowed_by_const_is_non_breaking(self):
        before = self.tuple_of({"type": "string"}, {"type": "integer"})
        after = self.tuple_of({"type": "string"}, {"type": "integer", "const": 0})
        report = self.response_pair(before, after)
        self.assertEqual(self.by_category(report), {"NON_BREAKING": {"response_schema_const_added"}})
        self.assertTrue(report["changes"][0]["location"].endswith(".prefixItems[1]"))

    def test_request_tuple_position_narrowed_is_breaking(self):
        before = self.tuple_of({"type": "string"}, {"type": "integer"})
        after = self.tuple_of({"type": "string"}, {"type": "integer", "const": 0})
        self.assertEqual(self.by_category(self.request_pair(before, after)),
                         {"BREAKING": {"request_schema_const_added"}})

    def test_tuple_position_member_properties_are_compared_recursively(self):
        member = {"type": "object", "properties": {"limit": {"type": "integer"}}}
        grown = {"type": "object", "properties": {"limit": {"type": "integer"}, "used": {"type": "integer"}}}
        report = self.response_pair(self.tuple_of(member, member), self.tuple_of(member, grown))
        self.assertEqual(self.by_category(report), {"NON_BREAKING": {"response_schema_field_added"}})
        removed = self.response_pair(self.tuple_of(member, grown), self.tuple_of(member, member))
        self.assertEqual(self.by_category(removed), {"BREAKING": {"response_schema_field_removed"}})

    def test_tuple_position_type_change_is_breaking(self):
        categories = self.by_category(self.response_pair(
            self.tuple_of({"type": "string"}, {"type": "integer"}),
            self.tuple_of({"type": "integer"}, {"type": "integer"})))
        self.assertEqual(categories, {"BREAKING": {"response_schema_type_changed"}})

    def test_tuple_resized_added_or_removed_stays_unknown(self):
        two = self.tuple_of({"type": "string"}, {"type": "integer"})
        three = {**two, "prefixItems": two["prefixItems"] + [{"type": "boolean"}]}
        plain = {"type": "array", "minItems": 2, "maxItems": 2}
        for before, after in ((two, three), (three, two), (plain, two), (two, plain)):
            with self.subTest(before=before, after=after):
                self.assertEqual(self.by_category(self.response_pair(before, after)),
                                 {"UNKNOWN": {"response_schema_prefixItems_changed"}})

    def test_identical_tuple_is_no_change(self):
        tuple_schema = self.tuple_of({"type": "string"}, {"type": "integer"})
        self.assertEqual(self.response_pair(tuple_schema, dict(tuple_schema))["changes"], [])


class SchemaAdmitsTests(unittest.TestCase):
    """schema_admits answers True/False only when it can prove it, otherwise None."""

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(COMPAT.parent))
        try:
            import openapi_compatibility as compat
        finally:
            sys.path.pop(0)
        cls.admits = staticmethod(compat.schema_admits)

    def test_types(self):
        self.assertTrue(self.admits({"type": "integer"}, 0))
        self.assertTrue(self.admits({"type": "number"}, 0))
        self.assertTrue(self.admits({"type": "integer"}, 2.0))
        self.assertFalse(self.admits({"type": "integer"}, 2.5))
        self.assertFalse(self.admits({"type": "integer"}, True))
        self.assertFalse(self.admits({"type": "integer"}, "0"))
        self.assertTrue(self.admits({"type": ["string", "null"]}, None))
        self.assertTrue(self.admits({"type": "string", "nullable": True}, None))
        self.assertTrue(self.admits({}, "anything"))

    def test_enum_const_and_bounds(self):
        self.assertTrue(self.admits({"enum": ["a", None]}, None))
        self.assertFalse(self.admits({"enum": [0]}, False))
        self.assertFalse(self.admits({"const": 1}, 2))
        self.assertTrue(self.admits({"minimum": 1, "maximum": 3}, 3))
        self.assertFalse(self.admits({"minimum": 1}, 0))
        self.assertFalse(self.admits({"minLength": 2}, "a"))
        self.assertFalse(self.admits({"maxLength": 1}, "ab"))
        self.assertTrue(self.admits({"pattern": "^[0-9]+$"}, "42"))
        self.assertFalse(self.admits({"pattern": "^[0-9]+$"}, "4x"))

    def test_unprovable_cases_are_none(self):
        for schema, value in (({"$ref": "#/components/schemas/X"}, 1), ({"allOf": [{}]}, 1),
                              ({"not": {}}, 1), ({"format": "date-time"}, "2020"),
                              ({"pattern": "("}, "a"), ({"minimum": "1"}, 1), ({"minLength": "1"}, "a"),
                              ({"multipleOf": 2}, 4), ({"type": ["string", 3]}, "a"), (True, 1),
                              ({"properties": {}}, {}), ({"minItems": 1}, [1])):
            with self.subTest(schema=schema):
                self.assertIsNone(self.admits(schema, value))


if __name__ == "__main__":
    unittest.main()
