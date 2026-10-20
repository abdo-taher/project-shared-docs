# API gap automation — GitHub only

Owner decision: **GitHub is the single source of truth.** This automation reads and writes only
`abdo-taher/project-shared-docs` (intake, published contracts, tooling) and `abdo-taher/capitalix`
(backend issues, branches, draft pull requests). It contains no GitLab client, no GitLab CI job, no
promotion or reconciliation logic. The earlier GitLab implementation (MR !9) was left exactly as it is.

## Flow

```
Consumer agent ──capitalix_gap.py submit──▶ shared-docs issue (public intake)
      │
      ▼  coordinator (gap_coordinator.py, manual workflow, off by default)
 validate (schema, secrets, published contract, actor) · fingerprint · dedupe · trust · triage
      │
      ▼
 capitalix issue  "[API gap <fp16>] …"   one per fingerprint, every consumer report linked
      │  `gap-dispatch::approved` added by a collaborator with write access
      │  (+ `gap-owner::approved` by the owner for sensitive areas)
      ▼
 dispatcher / worker (gap_dispatch.py, gap_worker.py) — on the operator's host, never in Actions
   reads the live task-coordinator + hotfix reservations (read-only), takes an exclusive lease on the module,
   runs the agent in the Docker sandbox, verifies independently (no network, no login), scans output for secrets
      │
      ▼
 branch gap/<issue>-<fp16>  ──▶  DRAFT pull request on integration/E01-FOUNDATION-SAAS ("Closes #<issue>")
      │  tests + human review + normal merge (never automatic)
      ▼
 published contract (released outside GitHub — see "Boundary") satisfies the evidence checks
      │
      ▼
 coordinator: CONTRACT_PUBLISHED → consumer notified → consumer upgrades its pin, runs tests, `confirm`
      │
      ▼
 RESOLVED (backend issue closed + this consumer confirmed; each consumer completes independently)
```

## What was reused unchanged

Request schema and validation (`tools/capitalix_gap_core.py`, now the **only** copy — the automation loads it),
consumer CLI, issue form, published-contract client with sha256/approval verification, trust model, output guard,
sandbox and independent verification, task-coordinator/hotfix reservation adapter, worker (flock, recovery, load
guard, rate limit), evidence vocabulary and negative control.

## What changed for GitHub only

| Area | Change |
|---|---|
| Backend tracking | `automation/gap/gap_github_backend.py`: the tracker interface the coordinator/dispatcher already used, implemented on GitHub Issues + Pull Requests of `abdo-taher/capitalix`. Label events and repository permissions come from GitHub identities, never from text. |
| Resolution proof | `detect_resolution`: an approved implementation **merged into the development branch**, its evidence file **at the merge commit**, the **currently published, verified contract** satisfying every check, and at least one check failing on the contract the consumer reported (no vacuous evidence). No pipeline/ancestry/GitLab lookups. |
| Coordinator host | `.github/workflows/api-gap-coordinator.yml`: `workflow_dispatch` only, `if: vars.API_GAP_AUTOMATION_ENABLED == 'true'`, read-only token permissions, its own environment and secrets, no agent, no merge. **No schedule exists.** |
| Tests in CI | `.github/workflows/api-gap-automation-tests.yml` (no secrets). Existing `contract-toolkit.yml` untouched. |
| Credentials | `API_GAP_GITHUB_TOKEN` (intake issues), `API_GAP_BACKEND_TOKEN` (backend issues/PRs read), `API_GAP_DISPATCH_TOKEN` (worker host only). Preflight checks them; the broad personal `gh` login is flagged. |
| Removed | GitLab client, GitLab forge, tree-promotion tool, promotion audit, GitLab CI jobs, production-pipeline evidence. |

## Publication

Publication is now GitHub-only in design and code ([GITHUB_PUBLICATION.md](GITHUB_PUBLICATION.md)): `contract-build`
(capitalix) → `contract-publish` (opens a PR) → the owner's review/merge → `contract-publication-verify`. It is
**implemented and tested but not cut over**: the legacy publisher still exists until its deploy key is removed, and no
GitHub publication has happened. Until then:

- a gap is `CONTRACT_PUBLISHED` only when the **currently published, digest-verified contract** satisfies the evidence
  checks and — for contracts published by the GitHub publisher — its build commit descends from the merge commit of the fix
  (`publication_proof: github-build-provenance`); the legacy contract keeps the weaker content-based proof;
- otherwise the state stays `IN_PROGRESS / MERGED_NOT_PUBLISHED` and is never reported as resolved.

## Safety properties (tested)

Manual-only workflow, flag off; issue content never authorizes execution; repository writers trusted, others need
`gap:triage-approved`; sensitive areas need the owner; exclusive module lease and write-area check against the live
coordinator and hotfix lane; no migrations, no `docs/api/openapi.json`, no workflow/automation paths in a gap change;
Docker sandbox with read-only root, dropped capabilities, no host credentials; secrets scan before any push.
The agent still holds its own model login and has outbound network access (see the earlier security note); use a
dedicated revocable token.

## Canary: `public.general.countries` (CAP-MOB-240, fingerprint `5065b06325c32767`)

| Item | Reference | State |
|---|---|---|
| intake issue | `abdo-taher/project-shared-docs#12` | open, `gap:in-progress` (set by the real coordinator) |
| backend issue | `abdo-taher/capitalix#5` | open, `gap::in-progress` |
| fix branch | `gap/5-5065b06325c32767` (commit `d76a26f`, base `287b2cc8`) | pushed |
| pull request | `abdo-taher/capitalix#6` (**Draft**, "Closes #5") | open, not merged |
| publication | published contract `2026.10.18-06d388692794` | does **not** contain the fix (3 of 4 checks fail on it) |

Provenance: the change was written by the real agent in an earlier sandboxed run and re-applied on the current
development head; it was **not** produced by a fresh dispatch, because dispatch needs `gap-dispatch::approved` from a
repository writer and that approval has not been given. Revalidation on `287b2cc8` in the sandbox: OpenAPI generated
(872 paths), evidence holds, PHPUnit 8 tests / 57 assertions OK; no conflict with live coordinator/hotfix reservations.
