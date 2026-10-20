# GitHub-only publication of the official API contract

Implements [GITHUB_PUBLICATION_PROPOSAL.md](GITHUB_PUBLICATION_PROPOSAL.md). **Status: implemented and tested, not yet
cut over.** Nothing has been published by it, the old publisher has not been disabled, and no official contract was
changed. The cutover (section 6) is the owner's decision and several of its steps are destructive.

## 1. Remaining GitLab dependencies, audited before the change

| # | Dependency | Where | After this change |
|---|---|---|---|
| 1 | The publisher job `publish_shared_api_docs` writing `api/implemented/` with an SSH deploy key | external GitLab CI + a read/write deploy key on this repo | replaced by workflow `contract-publish` (pull request, no direct push). **Old writer stays possible until the deploy key is deleted (cutover step 4).** |
| 2 | Contract generation + gates (`scripts/ci/`, `.gitlab-ci.yml`) building from the GitLab production repository | external | replaced by `contract-build` in `abdo-taher/capitalix` (development branch) |
| 3 | Approval: HMAC keyed by a GitLab CI token, checkable only by that job | manifest/approval v1 | approval v2: the owner's review of the publication PR on GitHub (client updated to accept both) |
| 4 | Provenance: manifest names a GitLab pipeline/job | manifest v1 | manifest v2 names the GitHub repository, commit, build run and workflow; verified against the GitHub API |
| 5 | Rule "written ONLY by the GitLab publish job" | `AGENTS.md`, `README.md`, `api/implemented/README.md`, `docs/PRODUCT_OVERVIEW.md`, `cycles/STATUS.md`, `docs/BRANCH_PROTECTION_PLAN.md` | rewritten for the GitHub publisher |
| 6 | Historical data: version `2026.10.18-06d388692794` (manifest, `docs/ACCEPTANCE_EVIDENCE.md`, the pinned example) names GitLab | immutable records | **kept on purpose**: rewriting a published version is forbidden. It is history, not an operational dependency |
| 7 | Consumer-side example "GitLab CI" snippet in `docs/DEVELOPER_QUICKSTART.md` | an example for consumers who use GitLab themselves | unchanged (not part of this system) |

## 2. Architecture as built

```
 capitalix  (development branch)                       project-shared-docs
 ┌────────────────────────────┐                        ┌────────────────────────────────────────────┐
 │ contract-build  (manual)   │   run id (owner)       │ contract-publish (manual, flag, env review) │
 │  generate ×2, identical    │ ─────────────────────▶ │  1 verify run via GitHub API                │
 │  route-coverage gate       │                        │  2 download + check bytes == recorded bytes │
 │  OpenAPI test suites       │                        │  3 compatibility vs current (fail closed)   │
 │  upload {openapi.json,     │                        │  4 write ONE new immutable version          │
 │          build-record.json}│                        │  5 verify tree + immutability vs main       │
 └────────────────────────────┘                        │  6 push publish/<version>, open PR          │
                                                       └───────────────────┬────────────────────────┘
                                                                           │ owner reviews + merges (= approval)
                                                       ┌───────────────────▼────────────────────────┐
                                                       │ contract-publication-verify (PR and main)   │
                                                       │  tree sound · earlier versions untouched ·  │
                                                       │  ≤1 new version · merged via approved       │
                                                       │  publish/* PR (detects direct pushes)       │
                                                       └─────────────────────────────────────────────┘
```

### Provenance (what is verified, and how)

Artifact attestations are **not available** for private repositories on this plan, so the provenance is GitHub's own
record of the run, read through its API by the publisher with a read-only, one-hour App token:

- the run belongs to `abdo-taher/capitalix`, workflow file `.github/workflows/contract-build.yml`, `completed/success`,
  event `workflow_dispatch`, built from branch `integration/E01-FOUNDATION-SAAS` and not from a fork;
- its commit is on that branch (compare API: `ahead`/`identical`);
- exactly one live `contract-build` artifact exists; it contains exactly `openapi.json` and `build-record.json`;
- the record's repository, commit and run id equal GitHub's; its sha256 and size equal the bytes (everything the
  artifact claims is checked against GitHub, nothing is believed);
- the commit date comes from the API, not from the record. The version id is `<commit date>-<sha256[:12]>`.

Upgrade path: where attestations become available, add `actions/attest-build-provenance` to `contract-build` and
`gh attestation verify` to `fetch-build`; the manifest already has the fields.

### Gates preserved from the old process

| Gate | Now |
|---|---|
| deterministic generation | generate twice, `cmp` |
| route coverage / validity | `openapi:coverage`, OpenAPI feature + unit test suites |
| compatibility classification | the same classifier (`tools/publish/openapi_compatibility.py`, 14 tests); **BREAKING and UNKNOWN fail closed** unless the owner sets `allow_breaking` / `allow_unknown` and a scope, which is recorded in `approval.json` and re-checked by `verify` |
| immutable versions, no rollback, no stale publication, no duplicates | `prepare` refuses them |
| approval of the exact bytes | `approval.json` pins the sha256; owner's PR review |
| one authoritative publisher | only `contract-publish` runs `prepare`; `verify-merge` flags any other writer on `main` |

Not carried over: the owner HMAC signature (no shared secret exists on GitHub; replaced by the PR review) and the
quality-baseline score gate (`openapi:quality` is not registered in the development branch — see section 7).

## 3. Roles, credentials, configuration

| Item | Value |
|---|---|
| Repository variable | `API_CONTRACT_PUBLICATION_ENABLED` (absent = disabled) |
| Environment | `contract-publisher` on `project-shared-docs`: required reviewer = owner, deployments from `main` only |
| Secret | `API_GAP_APP_PRIVATE_KEY` (already used by the coordinator; same GitHub App) |
| Tokens (minted per run, 1 h) | shared-docs: Contents write + Pull requests write (branch + PR; cannot merge); capitalix: Actions read + Contents read |
| App permission ceiling to add | **Actions: read** (needed to read the build run/artifact) and **Contents: write + Pull requests: write on project-shared-docs** — the App currently has issues/pull requests/contents *read* |
| Backend | the `contract-build` workflow is added to `abdo-taher/capitalix` by the accompanying PR (reference copy: `docs/api-gap/backend/contract-build.yml`) |

## 4. Operating it

### One command

```sh
python3 tools/publish/capitalix_release.py                      # build, publish PR, wait for the merge
python3 tools/publish/capitalix_release.py --build-run-id 123   # reuse an existing build
python3 tools/publish/capitalix_release.py --allow-unknown --scope "why"   # owner decisions, recorded in approval.json
```

It runs the steps below through your own `gh` login, prints a link whenever a person has to act (approve the
`contract-publisher` deployment; review and merge the publication PR) and keeps waiting. It never approves or merges,
switches `API_CONTRACT_PUBLICATION_ENABLED` on only for the run and restores the previous value on exit, and prints the
reason from the run log if a gate refuses (exit 3). Exit codes: 0 published, 2 `gh` error, 3 a workflow failed or refused,
4 timeout, 5 PR closed unmerged. Tests: `tools/tests/test_capitalix_release.py`.

The manual steps it automates:

```sh
# 1. in capitalix: Actions → contract-build → Run workflow on integration/E01-FOUNDATION-SAAS; note the run id
gh workflow run contract-build.yml -R abdo-taher/capitalix --ref integration/E01-FOUNDATION-SAAS
# 2. in shared-docs (after enabling; the owner approves the environment deployment):
gh variable set API_CONTRACT_PUBLICATION_ENABLED --body true -R abdo-taher/project-shared-docs
gh workflow run contract-publish.yml -R abdo-taher/project-shared-docs -f build_run_id=<run id>
# 3. review the PR "docs(api): publish contract <version>" — compatibility.md, approval.json, manifest — and merge it
# 4. disable again
gh variable set API_CONTRACT_PUBLICATION_ENABLED --body false -R abdo-taher/project-shared-docs
```

After the merge the coordinator needs no change: for a contract whose manifest names `abdo-taher/capitalix` it requires
that the build commit **descends from the merge commit of the fix** (`publication_proof: github-build-provenance`);
for legacy contracts it keeps the content-based proof.

## 5. Rollback

- Before merge: close the PR and delete `publish/<version>`; nothing was published.
- After merge: versions are immutable, so roll back by a pull request that sets `current.json` and the newest `index.json`
  entry back to the previous version *and* keeps the bad version directory (a `verify` rule forbids deletion); clients that
  pinned the bad version keep their pin until they `update`. The coordinator then returns affected gaps to
  `MERGED_NOT_PUBLISHED` on its next run. Disabling: unset the variable; revoke the App key to stop all publication.

## 6. Cutover checklist (owner; destructive steps marked ⚠)

1. Merge this PR and the capitalix PR (`contract-build`).
2. Raise the GitHub App permissions (section 3), create environment `contract-publisher`, set the variable only when ready.
3. Protect `main` of `project-shared-docs`: pull request required, 1 approval from a writer other than the author,
   required check `contract-publication-verify / verify` (and `tool`, `reference-consumer`).
4. ⚠ Remove the legacy publisher: delete the deploy key "capitalix GitLab CI publisher (api/implemented)" and disable the
   GitLab `publish_shared_api_docs` job. Until the key is deleted, a second writer can still push to `main`; the
   post-merge check reports it but cannot prevent it.
5. Do the first publication (section 4). The first GitHub-built contract will differ a lot from the published one (section 7).

## 7. Real evidence and the blocker it exposed

- All tests use temporary directories and fake or local servers. **No official contract was published or modified.**
- Dry-run on the real data in a temporary copy: the published tree verifies (`verify` → sound). The contract generated
  from the current development head (872 paths) versus the published `2026.10.18-06d388692794`:
  **527 breaking, 137 unclassified, 52 non-breaking, 10 documentation-only**; `prepare` correctly **refused** (fail closed).
  The development branch simply does not match the production contract that was published (response envelopes, nullability,
  schema shapes — the known production fixes not yet in development).
- With only the documentation change of the canary applied to the published contract, `prepare` produced a sound version
  (`2 documentation-only`), `verify` passed and the real consumer client `resolve_version` accepted it.
- Consequence: **the first GitHub publication cannot happen until development is reconciled with the published contract**
  (or the owner knowingly allows a breaking publication). This is the main remaining blocker.

## 8. Tests

```sh
python3 -m unittest discover -s tools/tests          # publisher (24), classifier (14), workflows (8), client, gap CLI
python3 -m unittest discover -s automation/gap/tests # coordinator + adapter incl. provenance-aware resolution
docker run --rm -v "$PWD:/repo" -w /repo rhysd/actionlint:1.7.7 .github/workflows/*.yml docs/api-gap/backend/contract-build.yml
```
