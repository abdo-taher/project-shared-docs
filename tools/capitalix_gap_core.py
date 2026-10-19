"""capitalix.api-gap.v1 — the API gap request: validation, sanitization, fingerprint, issue text.

Stdlib only. This file is shared by the consumer CLI
(tools/capitalix_gap.py), the GitHub automation (automation/gap/),
and the backend coordinator
(alalmiyalhura/capitalix: scripts/gap/gap_core.py).

All implementations must conform to the same fixtures
(fingerprints and verdicts) so their behavior cannot drift silently.

Everything in a request is untrusted input. Nothing here executes, evaluates or
interpolates request content: it is parsed as JSON (or as fixed issue-form
sections), checked against a closed schema, and scanned for secrets and
personal data before anyone else sees it.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone

SCHEMA_VERSION = "capitalix.api-gap.v1"
CORE_VERSION = "1.0.0"
BODY_MARKER = "<!-- capitalix-api-gap:v1 -->"
MAX_BODY_BYTES = 65536
MAX_REQUEST_BYTES = 32768

GAP_TYPES = (
    "MISSING_OPERATION",
    "REQUEST_MISMATCH",
    "RESPONSE_MISMATCH",
    "AUTH_MISMATCH",
    "VALIDATION_MISMATCH",
    "PAGINATION_MISMATCH",
    "BUSINESS_RULE_GAP",
    "CONTRACT_DOCUMENTATION_DEFECT",
)
# Types that describe an operation the published contract already contains.
OPERATION_TYPES = {"REQUEST_MISMATCH", "RESPONSE_MISMATCH", "AUTH_MISMATCH", "VALIDATION_MISMATCH",
                   "PAGINATION_MISMATCH", "CONTRACT_DOCUMENTATION_DEFECT"}
# Types whose deduplication identity needs the field/schema location.
LOCATION_TYPES = {"MISSING_OPERATION", "REQUEST_MISMATCH", "RESPONSE_MISMATCH", "VALIDATION_MISMATCH",
                  "PAGINATION_MISMATCH", "CONTRACT_DOCUMENTATION_DEFECT"}
ACTORS = ("owner", "accountant", "admin", "auth", "public")
PLATFORMS = ("flutter", "react", "nextjs", "vue", "angular", "web", "ios", "android", "other")
SEVERITIES = ("low", "medium", "high", "critical")
METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE")
EVIDENCE_KINDS = ("request", "response", "log", "note")

TOP_LEVEL = {"schema_version", "request_id", "consumer", "feature", "actor", "capability_id",
             "gap_type", "operation", "proposed", "location", "contract", "expected", "actual",
             "evidence", "requirements", "acceptance_criteria", "severity", "submitted_at"}
REQUIRED = ("schema_version", "request_id", "consumer", "feature", "actor", "gap_type", "contract",
            "expected", "actual", "acceptance_criteria", "submitted_at")

RE_REQUEST_ID = re.compile(r"[a-z0-9][a-z0-9-]{7,63}")
RE_PROJECT = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/-]{0,99}")
RE_CAPABILITY = re.compile(r"CAP-[A-Z]{2,6}-\d{3}")
RE_OPERATION_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,199}")
RE_PATH = re.compile(r"/api/[A-Za-z0-9_{}./-]{1,300}")
RE_LOCATION = re.compile(r"[A-Za-z0-9_.\[\]{}:/-]{1,200}")
RE_VERSION = re.compile(r"\d{4}\.\d{2}\.\d{2}-[0-9a-f]{12}")
RE_SHA256 = re.compile(r"[0-9a-f]{64}")
RE_TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")

LIMITS = {"feature": (3, 120), "expected": (10, 4000), "actual": (3, 4000)}
MAX_EVIDENCE, MAX_EVIDENCE_CHARS = 5, 8000
MAX_LIST, MAX_CRITERION_CHARS, MAX_REFERENCE_CHARS = 20, 500, 200

# --------------------------------------------------------------------------- sensitive content

_PLACEHOLDER = r"(?!<|\*|\[|\{\{|redacted|REDACTED|xxx|XXX|\.\.\.|null\b|none\b|example)"
SENSITIVE_PATTERNS = (
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})")),
    ("GitLab token", re.compile(r"\bgl(?:pat|dt|rt|cbt|ptt|ft|soat)-[A-Za-z0-9_-]{16,}")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    ("API secret key", re.compile(r"\bsk-(?:ant-|live_|test_)?[A-Za-z0-9_-]{20,}")),
    ("JSON web token", re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}")),
    # A credential value contains a digit; prose such as "Bearer authentication" does not.
    ("authorization credential", re.compile(
        r"(?i)(?:\bauthorization\b[\"']?\s*[:=]\s*[\"']?(?:bearer\s+|basic\s+|token\s+)?|\bbearer\s+)"
        + _PLACEHOLDER + r"(?=[A-Za-z0-9._~+/=|-]*\d)[A-Za-z0-9._~+/=|-]{12,}")),
    ("cookie", re.compile(r"(?i)\b(?:set-)?cookie\s*[\"']?\s*[:=]\s*[\"']?" + _PLACEHOLDER
                          + r"[^\s;=\"']+=[^\s;\"']{8,}")),
    ("secret value", re.compile(
        r"(?i)[\"']?\b(?:password|passwd|pwd|secret|api[_-]?key|access[_-]?token|refresh[_-]?token|"
        r"client[_-]?secret|private[_-]?key|otp|pin[_-]?code)\b[\"']?\s*[:=]\s*[\"']?" + _PLACEHOLDER
        + r"[^\s\"',}]{4,}")),
    ("IBAN", re.compile(r"\b[A-Z]{2}\d{2}(?:\s?[A-Z0-9]{4}){3,7}(?:\s?[A-Z0-9]{1,4})?\b")),
    ("phone number", re.compile(r"(?<![\d.])(?:\+|00)?966\s?5\d{8}(?!\d)|(?<![\d.])05\d{8}(?!\d)"
                                r"|(?<![\w.])\+\d{10,14}(?!\d)")),
)
_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+)")
_SAFE_EMAIL_DOMAINS = re.compile(r"(?i)(?:^|\.)(?:example\.(?:com|org|net)|example|test|invalid|localhost)$")
_DIGITS = re.compile(r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)")
_SUSPICIOUS = re.compile(
    r"(?i)ignore (?:all |any )?(?:previous|prior|above) instructions|disregard (?:the|your) (?:rules|instructions)"
    r"|you are now|system prompt|\bcurl\b[^\n|]*\|\s*(?:ba|z)?sh\b|\bwget\b[^\n|]*\|\s*(?:ba|z)?sh\b"
    r"|\brm\s+-rf\b|<script\b|\$\(|`[^`\n]*\b(?:sh|bash|python3?|php|eval)\b[^`\n]*`|```(?:sh|bash|shell|zsh)\b"
    r"|\bexport\s+[A-Z_]+=|\bsudo\b|base64\s+-d|/etc/passwd|\.ssh/")


def _luhn(digits: str) -> bool:
    total, parity = 0, len(digits) % 2
    for i, ch in enumerate(digits):
        d = int(ch)
        if i % 2 == parity:
            d = d * 2 - 9 if d > 4 else d * 2
        total += d
    return total % 10 == 0


def sensitive_findings(text: str) -> list[str]:
    """Kinds of secrets/personal data found in text. Never returns the matched values."""
    found = [name for name, pattern in SENSITIVE_PATTERNS if pattern.search(text)]
    if any(not _SAFE_EMAIL_DOMAINS.search(m.group(1)) for m in _EMAIL.finditer(text)):
        found.append("email address")
    for match in _DIGITS.finditer(text):
        digits = re.sub(r"\D", "", match.group(0))
        # Card numbers start with 3-6 (millisecond timestamps start with 1).
        if 13 <= len(digits) <= 19 and digits[0] in "3456" and _luhn(digits) and len(set(digits)) > 2:
            found.append("payment card number")
            break
    return found


def suspicious_instructions(text: str) -> bool:
    """Heuristic: text that tries to instruct an agent or run commands (forces human triage)."""
    return bool(_SUSPICIOUS.search(text))


def free_text(request: dict) -> list[tuple[str, str]]:
    """(field, text) for every free-text value in a request."""
    out = [(f, request[f]) for f in ("feature", "expected", "actual", "location") if isinstance(request.get(f), str)]
    for i, item in enumerate(request.get("evidence") or []):
        if isinstance(item, dict) and isinstance(item.get("content"), str):
            out.append((f"evidence[{i}]", item["content"]))
    for key in ("acceptance_criteria", "requirements"):
        for i, item in enumerate(request.get(key) or []):
            if isinstance(item, str):
                out.append((f"{key}[{i}]", item))
    consumer = request.get("consumer")
    if isinstance(consumer, dict) and isinstance(consumer.get("project"), str):
        out.append(("consumer.project", consumer["project"]))
    return out


# --------------------------------------------------------------------------- validation

def _str(errors: list, value, field: str, pattern: re.Pattern | None = None,
         limits: tuple[int, int] | None = None, choices=None) -> None:
    if not isinstance(value, str):
        errors.append(f"{field}: must be a string")
        return
    if limits and not limits[0] <= len(value.strip()) <= limits[1]:
        errors.append(f"{field}: length must be {limits[0]}..{limits[1]} characters")
    if pattern and not pattern.fullmatch(value):
        errors.append(f"{field}: invalid format")
    if choices and value not in choices:
        errors.append(f"{field}: must be one of {', '.join(choices)}")


def _str_list(errors: list, value, field: str, max_chars: int, required: bool) -> None:
    if not isinstance(value, list) or not all(isinstance(v, str) and v.strip() for v in value):
        errors.append(f"{field}: must be a list of non-empty strings")
        return
    if required and not value:
        errors.append(f"{field}: at least one entry is required")
    if len(value) > MAX_LIST:
        errors.append(f"{field}: at most {MAX_LIST} entries")
    if any(len(v) > max_chars for v in value):
        errors.append(f"{field}: each entry at most {max_chars} characters")


def validate(request) -> list[str]:
    """Schema errors (empty list = valid). Messages never quote submitted values."""
    if not isinstance(request, dict):
        return ["request: must be a JSON object"]
    if request.get("schema_version") != SCHEMA_VERSION:
        return [f"schema_version: unsupported (expected {SCHEMA_VERSION})"]
    errors: list[str] = []
    unknown = sorted(set(request) - TOP_LEVEL)
    if unknown:
        errors.append("unknown fields: " + ", ".join(k[:40] for k in unknown[:10]))
    for field in REQUIRED:
        if field not in request or request[field] in (None, "", [], {}):
            errors.append(f"{field}: required")
    if len(json.dumps(request, ensure_ascii=False).encode()) > MAX_REQUEST_BYTES:
        errors.append(f"request: larger than {MAX_REQUEST_BYTES} bytes")
    if errors:
        return errors

    _str(errors, request["request_id"], "request_id", RE_REQUEST_ID)
    consumer = request["consumer"]
    if not isinstance(consumer, dict) or set(consumer) - {"project", "platform"}:
        errors.append("consumer: must be {project, platform}")
    else:
        _str(errors, consumer.get("project"), "consumer.project", RE_PROJECT)
        _str(errors, consumer.get("platform"), "consumer.platform", choices=PLATFORMS)
    _str(errors, request["feature"], "feature", limits=LIMITS["feature"])
    _str(errors, request["actor"], "actor", choices=ACTORS)
    gap_type = request["gap_type"]
    _str(errors, gap_type, "gap_type", choices=GAP_TYPES)
    for field in ("expected", "actual"):
        _str(errors, request[field], field, limits=LIMITS[field])
    _str(errors, request["submitted_at"], "submitted_at", RE_TIMESTAMP)
    if isinstance(request["submitted_at"], str) and RE_TIMESTAMP.fullmatch(request["submitted_at"]):
        try:
            datetime.strptime(request["submitted_at"], "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            errors.append("submitted_at: not a valid UTC timestamp")

    contract = request["contract"]
    if not isinstance(contract, dict) or set(contract) != {"version", "sha256"}:
        errors.append("contract: must be {version, sha256}")
    else:
        _str(errors, contract["version"], "contract.version", RE_VERSION)
        _str(errors, contract["sha256"], "contract.sha256", RE_SHA256)

    capability = request.get("capability_id")
    if capability is not None:
        _str(errors, capability, "capability_id", RE_CAPABILITY)
    operation = request.get("operation")
    if operation is not None:
        _operation(errors, operation, "operation", allow_id=True)
    proposed = request.get("proposed")
    if proposed is not None:
        _operation(errors, proposed, "proposed", allow_id=False)
    location = request.get("location")
    if location is not None:
        _str(errors, location, "location", RE_LOCATION)

    if gap_type in OPERATION_TYPES and not operation:
        errors.append(f"operation: required for {gap_type} (the existing operation it concerns)")
    if gap_type == "MISSING_OPERATION":
        if operation:
            errors.append("operation: not allowed for MISSING_OPERATION (use capability_id, location "
                          "and optionally proposed)")
        if not capability:
            errors.append("capability_id: required for MISSING_OPERATION (never invent an endpoint path)")
    elif proposed:
        errors.append("proposed: only allowed for MISSING_OPERATION")
    if gap_type == "BUSINESS_RULE_GAP" and not capability:
        errors.append("capability_id: required for BUSINESS_RULE_GAP")
    if gap_type in LOCATION_TYPES and not location:
        errors.append(f"location: required for {gap_type} (field or schema location, or the missing action)")

    evidence = request.get("evidence", [])
    if not isinstance(evidence, list) or len(evidence) > MAX_EVIDENCE:
        errors.append(f"evidence: must be a list of at most {MAX_EVIDENCE} items")
    else:
        for i, item in enumerate(evidence):
            if not isinstance(item, dict) or set(item) != {"kind", "content"}:
                errors.append(f"evidence[{i}]: must be {{kind, content}}")
                continue
            _str(errors, item["kind"], f"evidence[{i}].kind", choices=EVIDENCE_KINDS)
            _str(errors, item["content"], f"evidence[{i}].content", limits=(1, MAX_EVIDENCE_CHARS))
    _str_list(errors, request["acceptance_criteria"], "acceptance_criteria", MAX_CRITERION_CHARS, True)
    if "requirements" in request:
        _str_list(errors, request["requirements"], "requirements", MAX_REFERENCE_CHARS, False)
    if "severity" in request:
        _str(errors, request["severity"], "severity", choices=SEVERITIES)

    if not errors:
        for field, text in free_text(request):
            kinds = sensitive_findings(text)
            if kinds:
                errors.append(f"{field}: contains sensitive data ({', '.join(sorted(set(kinds)))}) — "
                              "replace it with <redacted>")
    return errors


def _operation(errors: list, value, field: str, allow_id: bool) -> None:
    keys = {"operation_id", "method", "path"} if allow_id else {"method", "path"}
    if not isinstance(value, dict) or not value or set(value) - keys:
        errors.append(f"{field}: must be an object with " + ", ".join(sorted(keys)))
        return
    if "operation_id" in value:
        _str(errors, value["operation_id"], f"{field}.operation_id", RE_OPERATION_ID)
    if "method" in value:
        _str(errors, value["method"], f"{field}.method", choices=METHODS)
    if "path" in value:
        _str(errors, value["path"], f"{field}.path", RE_PATH)
    if allow_id and "operation_id" not in value and not ("method" in value and "path" in value):
        errors.append(f"{field}: needs operation_id, or method and path")


def is_sensitive_evidence_error(error: str) -> bool:
    return "contains sensitive data" in error


# --------------------------------------------------------------------------- fingerprint

def normalize_path(path: str) -> str:
    return re.sub(r"\{[^}]+\}", "{}", "/" + path.strip().strip("/")).lower()


def normalize_location(location: str) -> str:
    text = location.strip().lower().replace("/", ".")
    text = re.sub(r"\[\d*\]", "[]", text)
    text = re.sub(r"^\$?\.+", "", text)
    return re.sub(r"\.+", ".", text).strip(".")


def operation_key(request: dict) -> str:
    """Canonical operation identity; empty for MISSING_OPERATION (proposed paths are suggestions)."""
    if request.get("gap_type") == "MISSING_OPERATION":
        return ""
    operation = request.get("operation") or {}
    if operation.get("operation_id"):
        return operation["operation_id"].strip().lower()
    if operation.get("method") and operation.get("path"):
        return f"{operation['method'].upper()} {normalize_path(operation['path'])}"
    return ""


def fingerprint(request: dict) -> str:
    """Deterministic identity of the underlying gap, independent of consumer and contract version."""
    identity = {
        "v": 1,
        "actor": request["actor"],
        "type": request["gap_type"],
        "capability": (request.get("capability_id") or "").upper(),
        "operation": operation_key(request),
        "location": normalize_location(request.get("location") or ""),
    }
    return hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


# --------------------------------------------------------------------------- issue text

ISSUE_FORM_FIELDS = {
    # issue-form label -> request field (see .github/ISSUE_TEMPLATE/api-gap.yml)
    "Gap type": "gap_type",
    "Actor": "actor",
    "Consumer project": "consumer.project",
    "Consumer platform": "consumer.platform",
    "Feature": "feature",
    "Capability identifier": "capability_id",
    "Operation ID": "operation.operation_id",
    "HTTP method": "operation.method",
    "API path": "operation.path",
    "Field or schema location": "location",
    "Contract version": "contract.version",
    "Contract SHA256": "contract.sha256",
    "Expected behavior": "expected",
    "Actual behavior": "actual",
    "Reproduction evidence": "evidence",
    "Requirement references": "requirements",
    "Acceptance criteria": "acceptance_criteria",
    "Severity suggestion": "severity",
}
_NO_RESPONSE = {"", "_no response_", "none", "not applicable", "n/a"}


def _strip_fence(text: str) -> str:
    match = re.fullmatch(r"```[A-Za-z]*\n(.*?)\n?```", text.strip(), re.S)
    return match.group(1) if match else text.strip()


def parse_issue_body(body: str, issue_number: int, created_at: str) -> tuple[dict | None, list[str]]:
    """Extract the request from an issue body: the CLI's JSON block, or the issue-form sections."""
    if not isinstance(body, str) or not body.strip():
        return None, ["issue body is empty"]
    if len(body.encode()) > MAX_BODY_BYTES:
        return None, [f"issue body is larger than {MAX_BODY_BYTES} bytes"]
    blocks = []
    for block in re.findall(r"```json\s*\n(.*?)\n```", body, re.S):
        try:
            value = json.loads(block)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and "schema_version" in value:
            blocks.append(value)
    if len(blocks) > 1:
        return None, ["the issue contains more than one machine-readable request"]
    if blocks:
        return blocks[0], []
    sections = {}
    for match in re.finditer(r"^### (.+?)\s*\n(.*?)(?=^### |\Z)", body, re.S | re.M):
        sections[match.group(1).strip()] = match.group(2).strip()
    if "Gap type" not in sections:
        return None, ["no machine-readable request and no API gap issue-form sections"]
    request: dict = {"schema_version": SCHEMA_VERSION, "request_id": f"gh-issue-{issue_number}",
                     "submitted_at": created_at}
    for label, field in ISSUE_FORM_FIELDS.items():
        raw = _strip_fence(sections.get(label, ""))
        if raw.lower() in _NO_RESPONSE:
            continue
        if field in ("requirements", "acceptance_criteria"):
            value = [re.sub(r"^\s*(?:[-*]|\d+[.)])\s*", "", line).strip() for line in raw.splitlines()]
            request[field] = [v for v in value if v]
        elif field == "evidence":
            request["evidence"] = [{"kind": "note", "content": raw}]
        elif "." in field:
            outer, inner = field.split(".")
            request.setdefault(outer, {})[inner] = raw.upper() if inner == "method" else raw
        else:
            request[field] = raw
    if request.get("gap_type") == "MISSING_OPERATION" and "operation" in request:
        operation = request.pop("operation")
        operation.pop("operation_id", None)
        if operation:
            request["proposed"] = operation
    return request, []


def _quote(text: str) -> str:
    return "\n".join("> " + line for line in text.replace("\r", "").splitlines()) or "> "


def render_issue(request: dict) -> tuple[str, str]:
    """Issue title and body for a validated request (the JSON block is authoritative)."""
    fp = fingerprint(request)
    operation = request.get("operation") or {}
    target = operation.get("operation_id") or " ".join(filter(None, [operation.get("method"),
                                                                       operation.get("path")]))
    title = (f"[API gap] {request['feature'].strip()[:80]} — {request['gap_type']} "
             f"({request['actor']})")
    lines = [
        BODY_MARKER,
        f"**API gap** · `{request['gap_type']}` · actor `{request['actor']}`"
        + (f" · `{target}`" if target else "")
        + (f" · `{request['capability_id']}`" if request.get("capability_id") else ""),
        "",
        f"- **Feature:** {request['feature'].strip()}",
        f"- **Consumer:** `{request['consumer']['project']}` ({request['consumer']['platform']})",
        f"- **Contract:** `{request['contract']['version']}`",
        f"- **Fingerprint:** `{fp[:16]}` (recomputed by the coordinator; not trusted from this text)",
    ]
    if request.get("location"):
        lines.append(f"- **Location:** `{request['location']}`")
    if request.get("severity"):
        lines.append(f"- **Severity (suggestion only):** {request['severity']}")
    lines += ["", "### Expected", _quote(request["expected"]), "", "### Actual", _quote(request["actual"]),
              "", "### Acceptance criteria", *[f"- {c}" for c in request["acceptance_criteria"]]]
    if request.get("requirements"):
        lines += ["", "### Requirement references", *[f"- {r}" for r in request["requirements"]]]
    lines += ["", "<details><summary>Machine-readable request (authoritative)</summary>", "",
              "```json", json.dumps(request, indent=2, ensure_ascii=False), "```", "", "</details>", ""]
    return title, "\n".join(lines)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
