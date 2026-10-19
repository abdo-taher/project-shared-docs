# API gap requests

`capitalix.api-gap.v1.schema.json` describes the structured request a consumer
files when the approved contract is missing an operation or does not match what
the app needs. Create requests with `tools/capitalix_gap.py new` (it fills the
contract version, sha256 and canonical operation from your pin) and file them
with `submit`, or use the "API gap" issue form.

Requests are GitHub issues in this repository — never edits to
`api/implemented/`. The backend coordinator validates them with the same code
(`tools/capitalix_gap_core.py`), deduplicates them by fingerprint and links them
to backend work. See [docs/API_GAP_WORKFLOW.md](../../docs/API_GAP_WORKFLOW.md).
