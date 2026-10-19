# project-shared-docs

Shared API contracts and business documentation for Capitalix consumers.

| Start here | |
|---|---|
| What this is | [docs/PRODUCT_OVERVIEW.md](docs/PRODUCT_OVERVIEW.md) |
| Connect a frontend/mobile project | [docs/DEVELOPER_QUICKSTART.md](docs/DEVELOPER_QUICKSTART.md) |
| Rules for AI coding agents | [docs/AI_AGENT_INSTRUCTIONS.md](docs/AI_AGENT_INSTRUCTIONS.md) |
| Versions, pinning, breaking changes | [docs/CONTRACT_VERSIONING.md](docs/CONTRACT_VERSIONING.md) |
| Report a missing or wrong API | [docs/API_GAP_WORKFLOW.md](docs/API_GAP_WORKFLOW.md) |
| What was verified, and how | [docs/ACCEPTANCE_EVIDENCE.md](docs/ACCEPTANCE_EVIDENCE.md) |
| Proposed protection for `main` | [docs/BRANCH_PROTECTION_PLAN.md](docs/BRANCH_PROTECTION_PLAN.md) |
| Backend: generate, approve, publish | [docs/api-gap/GITHUB_PUBLICATION.md](docs/api-gap/GITHUB_PUBLICATION.md) (GitHub only) |
| API gap workflow, A to Z | [docs/api-gap/README.md](docs/api-gap/README.md) |

| Path | Content | Written by |
|---|---|---|
| `api/implemented/` | approved, versioned OpenAPI contracts (`current.json`, `index.json`, `versions/`) | `contract-publish` workflow pull requests only |
| `api/requirements/` | owner-app requirements mapping and gap report | pull requests |
| `api/BACKEND_API.md` | owner (Flutter) app requirements | Flutter developer |
| `business/` | business documentation | GitHub capitalix workflow |
| `tools/capitalix_contract.py` | consumer tool | pull requests |
| `tools/capitalix_gap.py`, `tools/capitalix_gap_core.py` | API gap reporting (core shared with the backend coordinator) | pull requests |
| `api/gaps/` | gap request schema (`capitalix.api-gap.v1`) | pull requests |
| GitHub Issues labelled `api-gap` | gap requests and their status | consumers (issues), the coordinator (status) |
| `examples/dart-owner-customers/` | tested reference consumer | pull requests |
