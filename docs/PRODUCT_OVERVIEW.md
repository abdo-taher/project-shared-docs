# Capitalix API Contract — product overview

## What it does

The Capitalix backend publishes one trusted, versioned API contract
(OpenAPI 3.1). Frontend and mobile developers — and their AI coding agents —
pin a version of it in their own project, look up only the operations a
feature needs, implement against them, and check their code and traffic
against the pinned contract.

## The problem it solves

Consumer apps were being built from a hand-written wish list
(`api/BACKEND_API.md`) while the backend shipped different paths, field names,
methods and response shapes. Agents guessed endpoints; mismatches surfaced
only at integration time. The contract makes the real API the single,
checkable reference, and the gap report shows exactly where the wish list and
the real API disagree.

## Components

| Component | Where | Responsibility |
|---|---|---|
| Generator + gates | GitHub `abdo-taher/capitalix` (`contract-build` workflow) | generate the contract from the development branch twice and require identical bytes; route-coverage gate; OpenAPI test suites; record exactly what was built |
| Approval | this repo (publication pull request) | the owner reviews and merges the pull request that carries the exact bytes; enforced by branch protection and `contract-publication-verify` |
| Publisher | this repo (`contract-publish` workflow, `tools/publish/`) | verifies the build against the GitHub API, classifies compatibility (breaking/unknown fail closed), opens a pull request with one new immutable version; the only writer of `api/implemented/` |
| Published contracts | this repo `api/implemented/` | `versions/<version>/`, `current.json`, `index.json` |
| Consumer tool | this repo `tools/capitalix_contract.py` | pin, verify, status/update, inspect, check, validate, sample, gap |
| Agent instructions | this repo `docs/AI_AGENT_INSTRUCTIONS.md` | the rules a coding agent follows |
| Reference consumer | this repo `examples/dart-owner-customers/` | the Owner app Customers feature, built and tested against the pinned contract and a real backend |
| Gap report | this repo `api/requirements/` | owner-app requirements vs. the published contract |

## Trust and versioning model

- The contract describes the **development branch** `integration/E01-FOUNDATION-SAAS` of `abdo-taher/capitalix` (the earlier version was built from the former GitLab production repository).
- A version is `YYYY.MM.DD-<first 12 hex of sha256>`; its bytes never change.
- Each version has a manifest: digest, source repository/commit, pipeline and
  job, approval evidence, baseline, compatibility summary.
- Consumers verify digests themselves (`verify --remote`). The owner's
  approval is the owner's review of the publication pull request on GitHub
  (v1 used an HMAC that only its publisher could check). Consumers verify the
  digest chain and the build run named in the manifest.
- Breaking or unclassifiable changes are blocked; see `CONTRACT_VERSIONING.md`.

## Supported workflows

- Pin, verify, update a contract in any project (Python 3.9+, no packages).
- Find relevant operations without loading the 6 MB contract (`inspect`).
- Check that code only calls documented paths (`check`).
- Validate recorded request/response traffic against the contract (`validate`).
- Generate contract-shaped test fixtures (`sample`).
- Requirements-to-contract gap report (`gap`).
- Works offline once pinned; works for agents without MCP.

## Not supported (yet)

- Generated SDKs/clients (not needed so far; add when a consumer measures the need).
- An MCP server (`inspect` already returns only the relevant operations).
- Consumer-side verification of the owner's signature (needs asymmetric signing).
- Automatic checks that a response's *values* are semantically right
  (`validate` checks shapes, types, enums and required fields).
- The Flutter app repository itself is not connected yet (not accessible
  when this was built); see `ACCEPTANCE_EVIDENCE.md`.
