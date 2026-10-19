# API gap workflow — complete cycle, A to Z

How a frontend/mobile consumer reports a missing or wrong API behaviour, how it becomes a backend fix, how the fix
reaches the official contract, and how "resolved" is proven. Everything below is GitHub-only **except one step, which is
called out explicitly in section 2: publication of the official contract.**

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

**Question: is GitLab completely removed and are all operations GitHub-only?**
**Answer: for the gap automation, yes. For the whole system, no — one dependency remains and it is documented, not hidden.**

Evidence (re-run it yourself with the commands at the end of this section):

| Area | Finding |
|---|---|
| `automation/gap/` code (coordinator, adapter, dispatcher, worker, sandbox, preflight) | **No GitLab client, API call, URL, token variable or CI job.** Remaining string hits are defensive only: a GitLab-token *pattern* in the secret scanner, `GITLAB_*` env names that are *scrubbed* from the agent's environment, and `.gitlab-ci.yml` in the *protected-paths* list. |
| `.github/workflows/` | Only GitHub Actions (`api-gap-coordinator`, `api-gap-automation-tests`, `contract-toolkit`). Zero GitLab. |
| Backend repo `capitalix` | No GitLab file in the 7,298-file tree; its only workflow (`publish-shared-docs.yml`) is GitHub Actions and syncs business docs only. |
| Gap tracking (issues, labels, PRs, approvals, evidence) | GitHub Issues / Pull Requests / label events only. |
| Credentials | GitHub App key + GitHub tokens only. No GitLab variable exists. |
| **Official contract publication** | **Still GitLab.** `api/implemented/` is written only by the "capitalix GitLab CI publisher" through a deploy key; `versions/2026.10.18-06d388692794/manifest.json` names source `alalmiyalhura/capitalix@2429b7d2`, a GitLab pipeline and job, and an HMAC approval keyed by a GitLab token. `AGENTS.md` and `api/implemented/README.md` state that rule. |
| Documentation | Several docs describe that publisher (`README.md`, `AGENTS.md`, `docs/DEVELOPER_QUICKSTART.md`, `cycles/STATUS.md`, …). |

**Consequence.** A fix merged on GitHub reaches the official contract only if that external publisher takes it. The
automation does not contact, replace or bypass it. Until the owner approves and builds a GitHub publication path
(`GITHUB_PUBLICATION_PROPOSAL.md`), every merged fix stays `MERGED_NOT_PUBLISHED` and is **never** reported as resolved.

Re-run the audit:

```sh
git grep -n -i gitlab -- automation .github tools | grep -v tests/      # only defensive hits (see above)
git grep -n -i "gitlab.com\|api/v4" -- automation .github               # no URL, no API: expect no output
git grep -l -i gitlab -- api docs README.md AGENTS.md                   # the publication dependency
```

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

### Step 7 — Contract publication (**the GitLab-dependent step**)

Today: the external publisher builds a new versioned contract, the owner's HMAC approval is attached, and it writes
`api/implemented/versions/<v>/{openapi.json,manifest.json,approval.json}` and moves `current.json`. The automation observes
only the result. Verified independently by the automation: the published bytes match their sha256, and the content satisfies
the fix's checks. **Not** verifiable from GitHub: that the contract was built from the merged commit.
Planned alternative (not built, needs owner approval): `GITHUB_PUBLICATION_PROPOSAL.md`.

### Step 8 — State derivation (coordinator, every run)

| Observed | State |
|---|---|
| valid, trusted | `ACCEPTED` |
| open/draft PR or `gap::in-progress` | `IN_PROGRESS` |
| PR merged into the development branch + evidence at the merge commit **and** still on the branch, but published contract does not satisfy the checks | `IN_PROGRESS / MERGED_NOT_PUBLISHED` |
| the same, and the **currently published, digest-verified** contract satisfies every check, and ≥1 check fails on the reporter's version | `CONTRACT_PUBLISHED` (consumers notified with exact upgrade steps) |
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

1. Publication still depends on the external GitLab publisher (section 2); provenance of a published contract is not tied to a
   GitHub commit.
2. A real-agent end-to-end dispatch has not yet been run on the GitHub flow (needs a fresh gap and the approval label).
3. `main` of `project-shared-docs` is not branch-protected, and the publisher's deploy key can write to it.
4. The agent keeps its own model login and outbound network inside the sandbox; use a dedicated revocable token.
