import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "capitalix_contract.py"

CONTRACT_V1 = {
    "openapi": "3.1.0",
    "info": {"title": "t", "version": "1"},
    "paths": {
        "/api/owner/sales/customers": {"post": {
            "operationId": "owner.sales.customers.store", "tags": ["Owner / Sales"],
            "security": [{"sanctumBearer": []}],
            "requestBody": {"required": True, "content": {"application/json": {
                "schema": {"$ref": "#/components/schemas/CreateCustomer"}}}},
            "responses": {"201": {"description": "ok", "content": {"application/json": {
                "schema": {"type": "object", "required": ["data"],
                           "properties": {"data": {"$ref": "#/components/schemas/Customer"}}}}}}}}},
        "/api/owner/sales/customers/{id}": {"get": {
            "operationId": "owner.sales.customers.show",
            "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "responses": {"200": {"description": "ok"}}}},
        "/api/owner/sales/customer-balances": {"get": {
            "operationId": "owner.sales.customer-balances",
            "parameters": [{"name": "page", "in": "query", "schema": {"type": ["integer", "null"], "minimum": 1}},
                           {"name": "name", "in": "query", "schema": {"type": ["string", "null"]}}],
            "responses": {"200": {"description": "ok"}}}},
        "/api/v1/customers": {"post": {
            "operationId": "alias.api.v1.customers.store", "deprecated": True,
            "x-canonical-replacement": ["POST /api/owner/sales/customers"],
            "requestBody": {"required": True, "content": {"application/json": {
                "schema": {"$ref": "#/components/schemas/CreateCustomer"}}}},
            "responses": {"201": {"description": "ok"}}}},
    },
    "components": {"schemas": {
        "CreateCustomer": {"type": "object", "required": ["name", "type"], "properties": {
            "name": {"type": "string", "maxLength": 10},
            "type": {"type": "string", "enum": ["INDIVIDUAL", "ORGANIZATION"]},
            "mobile": {"type": ["string", "null"]}}},
        "Customer": {"type": "object", "required": ["id", "name"], "properties": {
            "id": {"type": "string"}, "name": {"type": "string"}}},
    }},
}


def publish(root: Path, version: str, document: dict, date: str, commit: str):
    data = (json.dumps(document, indent=1) + "\n").encode()
    digest = hashlib.sha256(data).hexdigest()
    implemented = root / "api/implemented"
    vdir = implemented / "versions" / version
    vdir.mkdir(parents=True, exist_ok=True)
    (vdir / "openapi.json").write_bytes(data)
    approval = (json.dumps({"decision": "APPROVED", "approved_artifact_sha256": digest,
                            "approved_by": "Owner", "trusted_approval_id": "MR-!1",
                            "trusted_approval_signature": "ab" * 32}) + "\n").encode()
    (vdir / "approval.json").write_bytes(approval)
    approval_digest = hashlib.sha256(approval).hexdigest()
    manifest = {"schema": "capitalix-contract-manifest/1", "version": version, "sha256": digest,
                "operations": 4, "source": {"repository": "g/capitalix", "commit": commit},
                "approval": {"approved_by": "Owner", "trusted_approval_id": "MR-!1",
                             "approval_manifest_sha256": approval_digest},
                "files": {"openapi.json": digest, "approval.json": approval_digest},
                "compatibility": {"BREAKING": 0, "UNKNOWN": 0, "NON_BREAKING": 1}}
    (vdir / "manifest.json").write_text(json.dumps(manifest))
    index_path = implemented / "index.json"
    index = json.loads(index_path.read_text()) if index_path.exists() else {"versions": []}
    index["versions"].append({"version": version, "sha256": digest, "source_commit": commit,
                              "source_commit_date": date, "compatibility": manifest["compatibility"]})
    index_path.write_text(json.dumps(index))
    (implemented / "current.json").write_text(json.dumps({"version": version, "sha256": digest,
                                                          "source_commit_date": date}))
    return digest


class CapitalixContractToolTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.shared = base / "shared"
        self.project = base / "project"
        self.project.mkdir()
        self.digest = publish(self.shared, "2026.10.19-aaaa", CONTRACT_V1, "2026-10-19T00:00:00Z", "c1")
        self.source = f"file:{self.shared}"

    def tearDown(self):
        self.tmp.cleanup()

    def run_tool(self, *args):
        return subprocess.run([sys.executable, str(TOOL), *args], cwd=self.project,
                              text=True, capture_output=True)

    def pin(self):
        result = self.run_tool("init", "--source", self.source)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads((self.project / ".capitalix-contract/contract.lock").read_text())

    def test_init_pins_version_digest_and_source(self):
        lock = self.pin()
        self.assertEqual(lock["version"], "2026.10.19-aaaa")
        self.assertEqual(lock["sha256"], self.digest)
        self.assertEqual(lock["source_commit"], "c1")
        self.assertEqual(self.run_tool("verify").returncode, 0)

    def test_init_refuses_contract_that_does_not_match_published_digest(self):
        target = self.shared / "api/implemented/versions/2026.10.19-aaaa/openapi.json"
        target.write_text(target.read_text().replace("customers", "clients"))
        result = self.run_tool("init", "--source", self.source)
        self.assertEqual(result.returncode, 1)
        self.assertIn("does not match the published digest", result.stderr)

    def test_verify_detects_edited_pinned_contract(self):
        self.pin()
        pinned = self.project / ".capitalix-contract/openapi.json"
        pinned.write_text(pinned.read_text() + " ")
        result = self.run_tool("verify")
        self.assertEqual(result.returncode, 1)
        self.assertIn("never edit the pinned contract", result.stderr)

    def test_status_reports_newer_version_without_changing_the_pin(self):
        self.pin()
        newer = json.loads(json.dumps(CONTRACT_V1))
        newer["paths"]["/api/owner/new"] = {"get": {"operationId": "new", "responses": {"200": {"description": "ok"}}}}
        publish(self.shared, "2026.10.20-bbbb", newer, "2026-10-20T00:00:00Z", "c2")
        result = self.run_tool("status", "--fail-if-outdated")
        self.assertEqual(result.returncode, 1)
        self.assertIn("2026.10.20-bbbb", result.stdout)
        lock = json.loads((self.project / ".capitalix-contract/contract.lock").read_text())
        self.assertEqual(lock["version"], "2026.10.19-aaaa", "status must never move the pin")

    def test_status_works_offline(self):
        self.pin()
        lock_path = self.project / ".capitalix-contract/contract.lock"
        lock = json.loads(lock_path.read_text())
        lock["source"] = "file:/nonexistent/shared-docs"
        lock_path.write_text(json.dumps(lock))
        result = self.run_tool("status")
        self.assertEqual(result.returncode, 0)
        self.assertIn("unreachable", result.stdout)

    def test_update_moves_pin_explicitly_and_reports_changes(self):
        self.pin()
        newer = json.loads(json.dumps(CONTRACT_V1))
        del newer["paths"]["/api/owner/sales/customers/{id}"]
        publish(self.shared, "2026.10.20-bbbb", newer, "2026-10-20T00:00:00Z", "c2")
        result = self.run_tool("update")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("REMOVED GET /api/owner/sales/customers/{id}", result.stdout)
        self.assertEqual(json.loads((self.project / ".capitalix-contract/contract.lock").read_text())["version"],
                         "2026.10.20-bbbb")

    def test_inspect_returns_only_matching_operations_with_resolved_schemas(self):
        self.pin()
        result = self.run_tool("inspect", "customers", "--method", "POST", "owner")
        self.assertEqual(result.returncode, 0, result.stderr)
        out = json.loads(result.stdout)
        self.assertEqual([op["operationId"] for op in out["operations"]], ["owner.sales.customers.store"])
        schema = out["operations"][0]["requestBody"]["content"]["application/json"]["schema"]
        self.assertEqual(schema["required"], ["name", "type"])
        self.assertEqual(out["contract"]["sha256"], self.digest)

    def test_inspect_unknown_operation_fails_and_says_not_to_invent(self):
        self.pin()
        result = self.run_tool("inspect", "loyalty-points")
        self.assertEqual(result.returncode, 1)
        self.assertIn("do not invent", result.stderr)

    def test_check_flags_paths_missing_from_contract(self):
        self.pin()
        lib = self.project / "lib"
        lib.mkdir()
        (lib / "api.dart").write_text(
            "const a = '/api/owner/sales/customers';\n"
            "String b(String id) => '/api/owner/sales/customers/$id';\n"
            "const c = '/api/owner/sales/loyalty';\nconst d = 'assets/img/logo.png';\n")
        result = self.run_tool("check", "lib")
        self.assertEqual(result.returncode, 1)
        self.assertIn("2 API path literal(s) match", result.stdout)
        self.assertIn("/api/owner/sales/loyalty", result.stdout)
        self.assertNotIn("logo.png", result.stdout)

    def test_validate_accepts_conforming_traffic_and_rejects_violations(self):
        self.pin()
        traffic = self.project / "traffic.json"
        traffic.write_text(json.dumps([
            {"method": "POST", "path": "/api/owner/sales/customers",
             "body": {"name": "Ali", "type": "INDIVIDUAL"}, "status": 201,
             "response": {"data": {"id": "c1", "name": "Ali"}}},
            {"method": "GET", "path": "/api/owner/sales/customer-balances", "query": {"page": "2"}, "status": 200},
        ]))
        self.assertEqual(self.run_tool("validate", str(traffic)).returncode, 0)
        traffic.write_text(json.dumps([
            {"method": "POST", "path": "/api/owner/sales/customers",
             "body": {"name": "a very long name", "type": "business", "vat_number": "1"}, "status": 201,
             "response": {"data": {"id": 7}}},
            {"method": "GET", "path": "/api/owner/sales/customer-balances", "query": {"status": "x"}, "status": 418},
            {"method": "GET", "path": "/api/owner/sales/loyalty", "status": 200},
        ]))
        result = self.run_tool("validate", str(traffic))
        self.assertEqual(result.returncode, 1)
        for expected in ("longer than 10", "'business' is not one of", "missing required property `name`",
                         "query parameter `status` is not in the contract", "status 418 is not in the contract",
                         "no such operation"):
            self.assertIn(expected, result.stdout)

    def test_sync_restores_pinned_files_from_lock(self):
        self.pin()
        (self.project / ".capitalix-contract/openapi.json").unlink()
        result = self.run_tool("sync")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.run_tool("verify").returncode, 0)

    def test_gap_report_statuses_are_honest(self):
        self.pin()
        requirements = self.project / "REQ.md"
        requirements.write_text(
            "## 24. Customers\n\n"
            "| # | Name | Method | Suggested path | Params / body | Response |\n|---|---|---|---|---|---|\n"
            "| 1 | `customerCreate` | POST | `customers` | `name, type` | x |\n"
            "| 2 | `customerUpdate` | POST | `customers/{id}` | 24.1 | x |\n"
            "| 3 | `customerList` | GET | `sales/customer-balances` | `page`, `status` | x |\n"
            "| 4 | `loyalty` | GET | `loyalty` | – | x |\n"
            "| 5 | `customerCreate2` | POST | `customers` | `name` | x |\n")
        result = self.run_tool("gap", str(requirements), "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = {r["name"]: r for r in json.loads(result.stdout)["results"]}
        self.assertEqual(rows["customerCreate"]["status"], "PATH_AND_PARAMS_MATCH")
        self.assertIn("/api/owner/sales/customers", rows["customerCreate"]["operation"],
                      "deprecated alias must resolve to the canonical route")
        self.assertEqual(rows["customerUpdate"]["status"], "CANDIDATE_NEEDS_REVIEW")
        self.assertIn("other methods exist", rows["customerUpdate"]["notes"][0])
        self.assertIn("GET /api/owner/sales/customers/{id}", rows["customerUpdate"]["notes"][0])
        self.assertEqual(rows["customerList"]["status"], "PARAMS_DIFFER")
        self.assertEqual(rows["loyalty"]["status"], "MISSING")
        self.assertEqual(rows["customerCreate2"]["status"], "PARAMS_DIFFER",
                         "a required contract field the requirement omits is a difference")


    def test_gap_uses_backend_bindings_and_reviewed_map_precedence(self):
        self.pin()
        requirements = self.project / "REQ.md"
        requirements.write_text(
            "## 1. X\n\n| # | Name | Method | Suggested path | Body | Response |\n|---|---|---|---|---|---|\n"
            "| 1 | `customerCreate` | POST | `clients` | `name` | x |\n"
            "| 2 | `ghost` | GET | `ghost` | – | x |\n"
            "| 3 | `unbound` | GET | `nothing` | – | x |\n"
            "| 4 | `reviewed` | GET | `whatever` | – | x |\n")
        bindings = self.project / "bindings.json"
        bindings.write_text(json.dumps({"source": {}, "bindings": {
            "customerCreate": {"route": "POST api/owner/sales/customers", "body": {"name": "a", "phone": "5"}},
            "ghost": {"route": "GET api/owner/ghost"},
            "unbound": None,
            "reviewed": {"route": "GET api/owner/ghost"}}}))
        mapping = self.project / "map.json"
        mapping.write_text(json.dumps({"requirements": {"reviewed": {
            "status": "MAPPED_VERIFIED_LIVE", "operationId": "owner.sales.customers.show", "notes": ["n"]}}}))
        result = self.run_tool("gap", str(requirements), "--json", "--bindings", str(bindings), "--map", str(mapping))
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = {r["name"]: r for r in json.loads(result.stdout)["results"]}
        self.assertEqual(rows["customerCreate"]["status"], "MAPPED_BY_BACKEND_BINDING")
        notes = " ".join(rows["customerCreate"]["notes"])
        self.assertIn("phone", notes)
        self.assertIn("does not send: type", notes, "required `type` is not sent by the binding")
        self.assertEqual(rows["ghost"]["status"], "BOUND_BUT_NOT_IN_CONTRACT")
        self.assertEqual(rows["unbound"]["status"], "NOT_BOUND_BY_BACKEND")
        self.assertEqual(rows["reviewed"]["status"], "MAPPED_VERIFIED_LIVE")
        self.assertIn("owner.sales.customers.show", rows["reviewed"]["operation"])


if __name__ == "__main__":
    unittest.main()
