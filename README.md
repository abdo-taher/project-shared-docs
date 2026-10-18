# project-shared-docs

Shared API contracts and business documentation for Capitalix consumers.

| Start here | |
|---|---|
| What this is | [docs/PRODUCT_OVERVIEW.md](docs/PRODUCT_OVERVIEW.md) |
| Connect a frontend/mobile project | [docs/DEVELOPER_QUICKSTART.md](docs/DEVELOPER_QUICKSTART.md) |
| Rules for AI coding agents | [docs/AI_AGENT_INSTRUCTIONS.md](docs/AI_AGENT_INSTRUCTIONS.md) |
| Versions, pinning, breaking changes | [docs/CONTRACT_VERSIONING.md](docs/CONTRACT_VERSIONING.md) |
| What was verified, and how | [docs/ACCEPTANCE_EVIDENCE.md](docs/ACCEPTANCE_EVIDENCE.md) |
| Backend: generate, approve, publish | GitLab `alalmiyalhura/capitalix` `docs/api-contract/BACKEND_PUBLISHING_GUIDE.md` |

| Path | Content | Written by |
|---|---|---|
| `api/implemented/` | approved, versioned OpenAPI contracts (`current.json`, `index.json`, `versions/`) | GitLab capitalix publish job only |
| `api/requirements/` | owner-app requirements mapping and gap report | pull requests |
| `api/BACKEND_API.md` | owner (Flutter) app requirements | Flutter developer |
| `business/` | business documentation | GitHub capitalix workflow |
| `tools/capitalix_contract.py` | consumer tool | pull requests |
| `examples/dart-owner-customers/` | tested reference consumer | pull requests |
