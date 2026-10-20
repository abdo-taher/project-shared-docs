# API gap workflow — complete cycle, A to Z

How a frontend/mobile consumer reports a missing or wrong API behaviour, how it becomes a backend fix, how the fix
reaches the official contract, and how "resolved" is proven. Everything below is GitHub-only in design and code. The one remaining deployment step
(cutting over from the legacy publisher) is described in section 2 and GITHUB_PUBLICATION.md §6.

Audit date: 2026-10-20. Audited revisions: `project-shared-docs` `main` @ `43729f3`;
`capitalix` `integration/E01-FOUNDATION-SAAS` @ `f28429c8` (after PR #6). Nothing here contains a secret value.

---

## 1. Actors and repositories

| Role | Where | What it is |
|---|---|---|
| Consumer | any Flutter/React/… app or its AI agent | files and later confirms a gap using `tools/capitalix_gap.py` |
| Intake / contract repo | `abdo-taher/project-shared-docs` (public) | gap issues, published contracts (`api/implemented/`), consumer tooling, the automation (`automation/gap/`) |
| Backend repo | `abdo-taher/capitalix` (private) | Laravel source, backend tracking issues, fix branches and pull requests |
| Coordinator | GitHub Actions workflow `api-gap-coordinator` | validates, deduplicates, creates backend issues, mirrors state; **never** codes, merges or publishes |
| Dispatcher / worker | the operator's machine (Docker + the agent CLI) | runs the coding agent in a sandbox and opens a **Draft** PR; **never** merges or publishes |
| GitHub App `api-gap-automation` | installed on exactly the two repos | mints one-hour, single-repository tokens for the coordinator (bot login `api-gap-automation[bot]`) |
| Owner / writers | people | approve dispatch, review and merge, approve contract publication |

## 2. GitLab status — audited, not assumed

Audit date: 2026-10-20 (updated after the publication migration). Details: [GITHUB_PUBLICATION.md](GITHUB_PUBLICATION.md) §1.

**State of the code: every operational GitLab dependency has a GitHub replacement implemented and tested. State of the
deployment: not cut over, so GitLab is *not yet* completely out of the running system.** Both statements are true and are kept separate on purpose.

| Area | Finding |
|---|---|
| Gap automation (`automation/gap/`) | No GitLab client, URL, API call, token variable or CI job. Remaining hits are defensive only (token-format detector, `GITLAB_*` variables scrubbed from the agent's environment, `.gitlab-ci.yml` in the protected-paths list). |
| Workflows | GitHub Actions only: `api-gap-coordinator`, `api-gap-automation-tests`, `contract-toolkit`, **`contract-publish`**, **`contract-publication-verify`** (shared-docs) and **`contract-build`** (capitalix). |
| Backend repo | No GitLab file; the only other workflow syncs business docs. |
| Contract generation, gates, approval, publication | **Implemented on GitHub** (section 3, step 7). The legacy GitLab publisher is **still able to write** until the owner deletes its deploy key and disables its job (cutover step 4) — a destructive step that was not performed. |
| Historical records | Version `2026.10.18-06d388692794`, its manifest, `docs/ACCEPTANCE_EVIDENCE.md` and the pinned example name GitLab. Published versions are immutable, so this stays: history, not a dependency. |
| Consumer example | `docs/DEVELOPER_QUICKSTART.md` shows a "GitLab CI" snippet for consumers that use GitLab themselves. Not part of this system. |

Do not read "GitLab removed" as true until the cutover checklist is done and the first GitHub publication has succeeded.

Re-run the audit:

```sh
git grep -n -i "gitlab.com\|api/v4" -- automation .github tools/publish        # expect no output
git grep -n -i gitlab -- automation .github tools | grep -v tests/              # defensive hits + client legacy-format comment only
git grep -l -i gitlab -- api docs README.md AGENTS.md                           # history and the cutover documentation
gh api repos/abdo-taher/project-shared-docs/keys --jq '.[].title'              # the legacy publisher key must be gone after cutover

## 3. The lifecycle

```
 consumer ──(1)──▶ intake issue ──(2)──▶ coordinator ──(3)──▶ backend issue
                                                                 │ (4) writer adds gap-dispatch::approved
                                                                 ▼
 consumer ◀──(9)── coordinator ◀──(8)── contract ◀──(7)── merge ◀──(6)── Draft PR ◀──(5)── dispatcher + agent
   confirm            RESOLVED           published        review          (tests + evidence)
```

### Step 1 — Create the gap (consumer)

```sh
python3 tool/capitalix_contract.py init                       # pin the published contract (anonymous read)
python3 tool/capitalix_gap.py new --type CONTRACT_DOCUMENTATION_DEFECT --actor public \
    --feature "Public countries lookup" --project <app> --platform flutter \
    --capability CAP-MOB-240 --operation public.general.countries --method GET \
    --path /api/public/general/countries --location summary \
    --expected "…" --actual "…" --criterion "…" --out gap.json
python3 tool/capitalix_gap.py validate gap.json
python3 tool/capitalix_gap.py search gap.json                 # already reported?
python3 tool/capitalix_gap.py submit gap.json                 # creates the GitHub issue (needs a GitHub identity)
```

Gap types: `MISSING_OPERATION, REQUEST_MISMATCH, RESPONSE_MISMATCH, AUTH_MISMATCH, VALIDATION_MISMATCH,
PAGINATION_MISMATCH, BUSINESS_RULE_GAP, CONTRACT_DOCUMENTATION_DEFECT`. The request is validated locally against the pinned
contract (operation exists, actor namespace matches), scanned for secrets/personal data, and fingerprinted from
`actor + type + capability + operation + location` — independent of consumer and contract version.

### Step 2 — Intake validation (coordinator)

Run: Actions → `api-gap-coordinator` → *Run workflow* (`dry_run=true|false`, optional `issues="12 13"`). Manual only; no
schedule; refused unless repository variable `API_GAP_AUTOMATION_ENABLED=true`; an environment review by the owner is
required for every run.

Per issue the coordinator: parses (issue form or CLI JSON), validates strictly, checks the contract version and sha256
against the published index, checks the operation and actor, rejects secrets/PII and prompt-injection-looking text (sent to
triage), decides **trust from GitHub itself** (author's repository permission, label-event actors — never from text),
deduplicates (same consumer twice → `DUPLICATE`; different consumers share one backend issue), and labels the intake issue
with exactly one `gap:*` state label plus an in-place state comment and a history comment.

### Step 3 — Backend issue

One issue per fingerprint in `abdo-taher/capitalix`: title `[API gap <fp16>] …`, labels `api-gap`, `gap::accepted`,
`gap-type::…`, `gap-actor::…` (+ `gap-sensitive`), a hidden fingerprint marker, the validated request, and the consumer text
**fenced and indented as data, never instructions**. Re-runs find the existing issue; concurrent creations converge on the
oldest.

### Step 4 — Approval to dispatch (human)

`gap-dispatch::approved` must be added to the backend issue by a collaborator with **write** access (verified from the label
event's actor). Sensitive areas (money, auth, tenancy, integrations, …) additionally need `gap-owner::approved` by a login in
`policy.json → owner_usernames`. **The automation never applies these labels.** Without them nothing is dispatched.

### Step 5 — Implementation by the agent (operator host)

```sh
export API_GAP_DISPATCH_TOKEN=…   CAPITALIX_GAP_EXECUTOR_CMD='claude -p …'    # see OPERATIONS_GITHUB.md
python3 automation/gap/gap_dispatch.py probe            # can the sandboxed agent start?
python3 automation/gap/gap_dispatch.py list             # eligible issues and why others are not
python3 automation/gap/gap_dispatch.py run --issue <n> --forge github
python3 automation/gap/gap_worker.py run                # optional supervised polling worker
```

Gates before anything runs: issue open and not already in progress/published/resolved/blocked; approval labels as above;
the request still re-validates and matches its fingerprint (edits after validation are refused); no open PR linked; the live
**task coordinator and hotfix lane** are read (read-only) and the module gets an exclusive lease — a conflict with a sprint
task or hotfix refuses the dispatch; host load and rate limits.

Execution: a fresh shallow clone of `integration/E01-FOUNDATION-SAAS`; the agent runs in Docker (read-only root, all
capabilities dropped, no host credentials, resource caps, hard time limit) and may only write inside the reserved module,
`tests/` and `docs/api-gap/resolutions/`. Afterwards the dispatcher itself: refuses protected paths (CI, migrations,
`docs/api/openapi.json`, `automation/`…), requires the resolution evidence file, **re-runs generation + evidence + PHPUnit in a
second container with no network and no login**, scans every added line and commit message for secrets, then pushes branch
`gap/<issue>-<fp16>` (never forced) and opens a **Draft** PR whose body says what was and was not verified. It never merges.

Evidence file `docs/api-gap/resolutions/<fp16>.json` (schema `capitalix.api-gap-resolution.v1`): `fingerprint`,
`backend_issue`, `root_cause` (A missing endpoint · B exists but not in contract · C wrong behaviour · D wrong contract
inference), `summary`, `tests`, and machine-checkable `checks` (`operation_exists`, `field_present`, `field_required`,
`field_type`, `parameter_present`, `parameter_required`, `operation_has_summary`, `operation_description_contains`). **Negative
control:** at least one check must *fail* on the contract the consumer reported against, otherwise the evidence is rejected as
vacuous. Root causes E (consumer bug), F/G (business/auth decision) are triaged by labels, not coded.

### Step 6 — Review and merge (human)

Normal review of the Draft PR (body "Closes #<backend issue>"), normal gates, merge into
`integration/E01-FOUNDATION-SAAS` by a person. After this the coordinator reports `IN_PROGRESS / MERGED_NOT_PUBLISHED`.

### Step 7 — Contract publication (GitHub-only, owner-approved)

```
capitalix  : Actions → contract-build  (manual, development branch)  → artifact {openapi.json, build-record.json}
shared-docs: Actions → contract-publish (manual, flag + environment review) with build_run_id
             → verifies the build against the GitHub API → classifies changes → writes ONE new immutable version
             → opens PR  publish/<version>      (never pushes to main)
owner      : reviews compatibility.md / approval.json / manifest → approves + merges   (= the approval)
shared-docs: contract-publication-verify (PR and main): tree sound, earlier versions untouched, ≤ 1 new version,
             change reached main through an approved publish/* PR
```

What is verified: the build run (repository, workflow file, success, manual dispatch, branch, not a fork), that the commit is
on the development branch, that the bytes are exactly the recorded bytes, the compatibility class of every change
(**BREAKING and UNKNOWN fail closed**; an explicit owner decision is recorded in `approval.json`), immutability, no rollback,
no stale or duplicate version. Provenance in the manifest: repository, commit, build run URL and workflow. Where GitHub
artifact attestations become available for private repositories they can be added without changing the manifest.
Full design, credentials, cutover and rollback: [GITHUB_PUBLICATION.md](GITHUB_PUBLICATION.md).

### Step 8 — State derivation (coordinator, every run)

| Observed | State |
|---|---|
| valid, trusted | `ACCEPTED` |
| open/draft PR or `gap::in-progress` | `IN_PROGRESS` |
| PR merged into the development branch + evidence at the merge commit **and** still on the branch, but the published contract does not satisfy the checks — or, for a contract published by the GitHub publisher, its build commit does not contain the merge | `IN_PROGRESS / MERGED_NOT_PUBLISHED` |
| the same, and the **currently published, digest-verified** contract satisfies every check, ≥1 check fails on the reporter's version, and (GitHub-published contracts) the build commit descends from the merge commit | `CONTRACT_PUBLISHED` (consumers notified with exact upgrade steps) |
| consumer upgraded its pin, ran its tests, ran `confirm` | `CONSUMER_VERIFIED` |
| backend issue closed as well | `RESOLVED` (per consumer, independently) |

Fail-closed rules: evidence missing, invalid, vacuous, absent from the branch (e.g. reverted), a tampered contract, an
unreachable API, or untrusted input → the state does **not** advance. A patch, a branch or an open PR never exceeds
`IN_PROGRESS`; `MERGED_NOT_PUBLISHED` is never "resolved".

### Step 9 — Consumer verification

```sh
python3 tool/capitalix_gap.py status <issue>                                  # state, resolution version, pin includes it?
python3 tool/capitalix_contract.py update --version <published version>       # explicit upgrade — the pin never moves itself
# run your contract checks and integration tests, then:
python3 tool/capitalix_gap.py confirm <issue> --tests-passed
```

## 4. Worked example (real, 2026-10-19/20)

| Step | Evidence |
|---|---|
| 1–2 | `project-shared-docs#12` submitted; coordinator accepted it; fingerprint `5065b06325c32767` |
| 3 | backend issue `capitalix#5` created by the coordinator |
| 5 | fix (PHPDoc on `GeneralLookupController::countries()` + test + evidence) re-applied on `287b2cc8`: OpenAPI generated (872 paths), evidence holds, PHPUnit 8 tests/57 assertions OK, 3 of 4 checks fail on the published contract (negative control), no reservation conflict. Written by the real agent in an earlier sandbox run; **not** a fresh dispatch (approval label not given) |
| 6 | Draft `capitalix#6` → reviewed and merged by the owner (`f28429c8`) |
| 7 | **Not published**: published contract is still `2026.10.18-06d388692794` |
| 8 | Actions run `39326644607` (dry run): all steps green; #12 computes to `IN_PROGRESS / MERGED_NOT_PUBLISHED` |
| 9 | not applicable until step 7 happens |

## 5. Credentials (roles → realisation)

| Role | Realisation | Scope |
|---|---|---|
| `API_GAP_GITHUB_TOKEN` | App installation token minted per run | `project-shared-docs` only; Issues write, Metadata read |
| `API_GAP_BACKEND_TOKEN` | App installation token minted per run | `capitalix` only; Issues write, Pull requests read, Contents read, Metadata read |
| App key | secret `API_GAP_APP_PRIVATE_KEY`, variable `API_GAP_APP_CLIENT_ID` | environment `api-gap-coordinator` (owner review, `main` only) |
| `API_GAP_DISPATCH_TOKEN` | fine-grained PAT on the worker host | `capitalix` Issues write; env file mode 600, never in Actions |
| agent login | dedicated revocable token | worker host only |

Details, rotation and setup commands: `OPERATIONS_GITHUB.md` §3. The preflight (`gap_preflight.py`, run by the workflow)
verifies each token without printing it; it fails if the intake token can read the backend repository.

## 6. What is automatic vs. what needs a person

| Automatic (once enabled and approved per run) | Always a person |
|---|---|
| validation, dedup, trust checks, backend issue creation, label/comment mirroring, state derivation, notifications | enabling the flag, approving each workflow run (environment gate) |
| sandboxed implementation, independent verification, secret scan, Draft PR | `gap-dispatch::approved` / `gap-owner::approved`, reviewing and merging the PR |
| | contract publication and its approval; the consumer's upgrade and `confirm` |

## 7. Operate, test, recover, disable

```sh
python3 -m unittest discover -s automation/gap/tests     # 249 tests
python3 -m unittest discover -s tools/tests              # 54 tests
gh workflow run api-gap-coordinator.yml -R abdo-taher/project-shared-docs -f dry_run=true -f issues=12
gh variable set API_GAP_AUTOMATION_ENABLED --body false -R abdo-taher/project-shared-docs     # disable everything
```

Recovery: re-run the coordinator (idempotent); `--replay <n>` for a parked issue; `gap_dispatch.py recover` after a crash
(fails the dispatch visibly, releases the module lease, kills labelled containers, deletes the login copy); remove
`gap-dispatch::failed` to retry. Rollback: close the Draft PR; disable the flag; revoke the App key. Full guide:
`OPERATIONS_GITHUB.md`; design and boundary: `GITHUB_ONLY.md`.

## 8. Known limits

1. **Cutover not done.** The GitHub publisher exists and is tested but has published nothing; the legacy GitLab publisher can
   still write until its deploy key is deleted. Legacy contracts (only `2026.10.18-…`) keep the weaker content-based proof.
1b. **First GitHub publication is blocked by divergence:** the contract generated from the development head differs from the
   published one by 527 breaking / 137 unclassified changes, so `prepare` refuses (fail closed) until development is reconciled
   or the owner explicitly allows it.
2. A real-agent end-to-end dispatch has not yet been run on the GitHub flow (needs a fresh gap and the approval label).
3. `main` of `project-shared-docs` is not branch-protected, and the publisher's deploy key can write to it.
4. The agent keeps its own model login and outbound network inside the sandbox; use a dedicated revocable token.
