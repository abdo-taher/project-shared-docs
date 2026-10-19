"""Sensitivity classification shared by the coordinator and the dispatcher.

A gap is sensitive when it touches accounting, authentication, authorization,
permissions, billing, payments, payroll, tax, financial integrations, data
import/export, or organization/tenant boundaries (owner decision 2026-10-19).
Sensitive gaps need the owner's approval before any backend implementation is
dispatched.

Classification can only make the process stricter, so it also looks at
consumer-written text (feature, location): a submitter cannot lower
sensitivity by wording, only raise it.
"""

from __future__ import annotations

import re


def _blob(request: dict) -> str:
    operation = request.get("operation") or {}
    proposed = request.get("proposed") or {}
    parts = [request.get("capability_id"), request.get("location"), request.get("feature"),
             operation.get("operation_id"), operation.get("path"), proposed.get("path")]
    return " ".join(p for p in parts if isinstance(p, str)).lower()


def sensitivity_reasons(policy: dict, request: dict, labels: set[str] | None = None) -> list[str]:
    """Why the gap is sensitive (empty list = not sensitive)."""
    reasons = []
    if labels and "gap-sensitive" in labels:
        reasons.append("labelled gap-sensitive by a maintainer")
    if request.get("gap_type") in policy.get("sensitive_gap_types", []):
        reasons.append(f"gap type {request['gap_type']}")
    capability = request.get("capability_id") or ""
    for prefix in policy.get("sensitive_capability_prefixes", []):
        if capability.startswith(prefix + "-"):
            reasons.append(f"capability {prefix}")
            break
    operation_id = (request.get("operation") or {}).get("operation_id") or ""
    for prefix in policy.get("sensitive_operation_prefixes", []):
        if operation_id.startswith(prefix):
            reasons.append(f"operation namespace {prefix}")
            break
    blob = _blob(request)
    hits = sorted({k for k in policy.get("sensitive_keywords", [])
                   if re.search(r"(?<![a-z0-9])" + re.escape(k), blob)})
    if hits:
        reasons.append("keywords: " + ", ".join(hits[:6]))
    return reasons


def is_sensitive(policy: dict, request: dict, labels: set[str] | None = None) -> bool:
    return bool(sensitivity_reasons(policy, request, labels))
