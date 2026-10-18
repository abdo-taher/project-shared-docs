# Acceptance evidence — Capitalix API contract product

Recorded 2026-10-19. Each criterion lists the evidence it rests on. Statuses:
**VERIFIED** (observed), **IMPLEMENTED, NOT VERIFIED**, **BLOCKED (external)**.

## Published contract

| | |
|---|---|
| Version | `2026.10.18-06d388692794` |
| sha256 | `06d3886927947b77daad9c38c677bee4beb0b6f39ff8f0b8ad8c5d1bc257578c` |
| Operations | 1028 (872 paths) |
| Source | GitLab `alalmiyalhura/capitalix@2429b7d2b41d7c6e0849b5645ea06d4463751d86` (merge of MR !6) |
| Pipeline / jobs | [2960973893](https://gitlab.com/alalmiyalhura/capitalix/-/pipelines/2960973893): approval job 17269343587, publish job 17269343590 |
| Approval | `Abdulrahman Taher <abdotaher2025@gmail.com>`, `MR-!6@job-17269041645`, initial publication |
| Published at | this repo `api/implemented/versions/2026.10.18-06d388692794/`, commit `9b698bfa` |

## Criteria

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Source-of-truth and promotion documented | VERIFIED | GitLab `docs/api-contract/BACKEND_PUBLISHING_GUIDE.md`; dev clone tracks GitLab `main` as `refs/prod/main` |
| 2 | v4 pipeline verified in real CI | VERIFIED | MR !6 pipeline 2960957859 all green (image, validation 97 s, phpunit 65 s, drift, approval check); main 2960973893 all green incl. approval + publish |
| 3 | Security-critical settings verified | VERIFIED | API read-back: publication credential is `SHARED_DOCS_DEPLOY_KEY`, an SSH deploy key (GitHub id 166881222) that can write to this repository only, protected+masked, scope `shared-api-docs`, GitHub host key pinned; the account-wide `SHARED_DOCS_TOKEN` was deleted from GitLab; approval key/approver protected, scope `openapi-contract-approval`; `only_allow_merge_if_pipeline_succeeds=true`; pipeline variables need Maintainer |
| 4 | Deterministic, environment-independent generation | VERIFIED | CI candidate sha256 = local sha256 = `06d38869…` (MR jobs 17269022598, 17269041645); determinism gate true; root causes fixed: APP_NAME/SESSION_COOKIE leak from `.env`, missing bcmath/intl |
| 5 | Compatibility and quality gates pass | VERIFIED | initial publication: 0 changes vs. itself; quality 861/39, 0 regressions (ratchet tightened 875→873→861, no fingerprint increased) |
| 6 | Negative cases fail closed | VERIFIED | real CI: MR pipelines 2960917817 / 2960920633 failed `openapi_contract_approval_check` with "approval file … is missing"; 2960917817 failed `api_contract_drift` on undocumented API change. Unit tests (93 CI-script tests): invalid/stale/nondeterministic/uncovered, breaking, unknown, quality regression, absent approval, other-digest approval, replayed/edited signature, initial-mode reuse after history, shallow history, unapproved bytes, stale publication, rollback, version rewrite |
| 7 | Real approved contract published | VERIFIED | see table above |
| 8 | Immutable identity, digest, source revision | VERIFIED | `manifest.json` (sha256, source commit, pipeline/job, approval); publisher refuses rewrite/rollback (tests) |
| 9 | Retrievable and verifiable via consumer path | VERIFIED | fresh empty project: tool downloaded from GitHub, `init` → `verify --remote` → `status` all exit 0; publish job re-verified via contents API ("published contract OK") |
| 10 | Reproducible pinning | VERIFIED | `contract.lock` (version, sha256, manifest sha256, source commit); `sync` restores and verifies; workflow restores the pin on every run |
| 11 | Inspect only relevant operations | VERIFIED | `inspect customers --method POST owner` → 15.6 KB vs. 6.2 MB contract |
| 12 | Agent instructions tested in a real workflow | VERIFIED (by this agent) | the reference consumer was implemented by following `AI_AGENT_INSTRUCTIONS.md` (inspect → implement → sample fixtures → check → validate); not yet exercised by an independent agent in the Flutter repo |
| 13 | Representative feature against the pinned contract | VERIFIED | `examples/dart-owner-customers`: Customers list (paginated) / create / update / delete, 401/409/422; Dart 14/14 (11 unit + 3 real backend); `dart analyze --fatal-infos` clean |
| 14 | Backend, tooling, consumer tests pass | VERIFIED | PHPUnit 19/19 (CI + local); CI scripts 93/93; consumer tool 13/13; Dart 14/14; recorded traffic: mock 9/9, **real backend 7/7** conform to the published contract |
| 15 | Requirements-to-contract gap report | VERIFIED | `api/requirements/GAP_REPORT.md` for 161 owner-app endpoints: 5 live-verified, 1 reviewed, 150 bound by the backend conformance suite (30 with a required-field mismatch, 53 with undocumented fields), 4 not bound, 1 missing |
| 16 | Developer documentation | VERIFIED | `docs/` (overview, quickstart, agent instructions, versioning, this file); backend guide in GitLab |
| 17 | Reproducible publication and update | VERIFIED (publication); IMPLEMENTED, NOT VERIFIED (a second, changed version) | first version published by CI; `update` covered by tests only — no second contract version exists yet |
| 18 | End-to-end evidence recorded | VERIFIED | this file |
| 19 | Unchanged approved contract and scoped credential in real CI | VERIFIED | main pipeline 2961016622: approval job 17269620821 "unchanged since approval"; publish job 17269620824 cloned over SSH with the deploy key, `NO_CONTRACT_CHANGES`, re-verification OK |

## Real-backend verification

The backend exercised live was production code identical to `2429b7d2`
(`app/`, `routes/`, `config/`, `database/`, `bootstrap/`, `composer.lock`
compared file by file), on a disposable SQLite database seeded with the
repository's own `CapitalixUserSeeder`, never a shared environment. Recorded
exchanges (login, create, update, list, delete, 422, 401) were validated with
`capitalix_contract.py validate`: 7/7 conform.

The live traffic found five contract defects; all were fixed in the generator
or made explicit before publication (GitLab commit `c101094`): list envelope
(`data.items` + `data.meta`, 145 operations), envelope nested in an `anyOf`
alternative (login), unsatisfiable `data: null` (deletes), nullable
`mobile`/`phone`, boolean `has_subscription`.

## Known limitations

- **Flutter app repository not accessible** (not found in any account
  available to this work). The integration was proven with a Dart reference
  consumer instead; connecting the real app is open.
- **The former account-wide GitHub token** is no longer used by GitLab and was
  deleted there; revoking it in GitHub is an owner action, after checking
  whether the GitHub `capitalix` "Publish Shared Documentation" workflow uses
  the same token as its own `SHARED_DOCS_TOKEN` secret.
- **Consumers cannot verify the owner's signature** (HMAC, symmetric). They
  verify digests and provenance; the signature is verified by the protected
  GitLab job.
- **Contract `required` lists** for 31 owner-app endpoints (30 bound + login)
  disagree with what the backend's own conformance suite sends (e.g. login requires `login`,
  `device_name`; the app sends `phone`). One case was observed live; the rest
  are reported, not fixed.
- **Shared-docs `main` cannot be branch-protected** on the current GitHub plan;
  integrity rests on immutable versions + digests in consumer locks.
- **Development repository**: the generator fix was merged into
  `integration/E01-FOUNDATION-SAAS` as `287b2cc8` (abdo-taher/capitalix#4)
  after generating development's contract with it (872 paths, list envelope
  documented). Development has no automated test run for it; promotion to
  production is still gated by the consistency and compatibility checks.
- The GitLab `AGENTS.md` (synced from development) still references
  documents that only exist in the development repository.

## Follow-up verification

| Run | Result |
|---|---|
| MR !7 pipeline 2960981784 | green with no new approval: approval check "unchanged since approval" |
| MR !7 merge | GitLab wrote merge commit `e885843` but reported "An error occurred while merging"; the MR was closed with a note, its change ran in the next main pipeline |
| MR !8 (deploy key) pipeline 2961009281 | green |
| main pipeline 2961016622 (`ffff625d`) | all green: signature verified for the unchanged contract; publish via deploy key; no-op; published copy re-verified |
| Deploy key write access | `git push --dry-run` authorised before use (no ref created) |
