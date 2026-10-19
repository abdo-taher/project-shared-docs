# API gap automation — GitHub operations guide

Architecture and rules: [GITHUB_ONLY.md](GITHUB_ONLY.md). This guide is what an operator needs day to day.
No secret value appears in this file; `<…>` are placeholders.

## 1. Components and where they run

| Component | Runs | Does | Never does |
|---|---|---|---|
| `tools/capitalix_gap.py` | consumer machine/CI | creates, validates, submits, tracks and confirms a gap | writes anything but its own issue/comment |
| `automation/gap/gap_coordinator.py` | GitHub Actions (`api-gap-coordinator`, manual) or an operator shell | validates intake, creates/links the backend issue, mirrors state, notifies | starts an agent, merges, publishes, writes contracts |
| `automation/gap/gap_dispatch.py` / `gap_worker.py` | operator host with Docker + the agent CLI | claims a module lease, runs the sandboxed agent, verifies independently, pushes `gap/<n>-<fp16>`, opens a **Draft** PR | merge, approve, publish; run on a hosted runner |

## 2. Lifecycle and states

`SUBMITTED → VALIDATING → (NEEDS_TRIAGE) → ACCEPTED → IN_PROGRESS → CONTRACT_PUBLISHED → CONSUMER_VERIFIED → RESOLVED`
(`DUPLICATE`, `REJECTED`, `BLOCKED` are side exits.)

| Fact the coordinator observes (GitHub / published contract) | State |
|---|---|
| valid request, trusted reporter | `ACCEPTED`, backend issue created once per fingerprint |
| open or draft PR referencing the backend issue, or `gap::in-progress` | `IN_PROGRESS` |
| PR **merged into `integration/E01-FOUNDATION-SAAS`** and its evidence file exists at the merge commit, but the published contract does not satisfy the checks | `IN_PROGRESS` / `MERGED_NOT_PUBLISHED` — **not resolved** |
| the same, and the current published, digest-verified contract satisfies every check while the reporter's version did not | `CONTRACT_PUBLISHED` |
| the consumer pinned that (or a newer) version, ran its tests and `confirm`ed | `CONSUMER_VERIFIED` |
| backend issue closed as well | `RESOLVED` (per consumer, independently) |

A patch, a branch or an opened PR never advances past `IN_PROGRESS`. Missing/invalid/vacuous evidence fails closed.

## 3. Credentials (logical roles)

GitHub does not allow creating fine-grained personal access tokens or Apps through an API available to this tooling;
**the account owner creates them in the UI**. Recommended: one GitHub App (installation tokens are short-lived) with the
permissions below; fine-grained PATs scoped to a single repository are the fallback.

| Name (secret) | Purpose | Repository scope | Minimum permissions | Lives in |
|---|---|---|---|---|
| `API_GAP_GITHUB_TOKEN` | coordinator reads/writes intake issues | `abdo-taher/project-shared-docs` only | Issues: read/write, Metadata: read | shared-docs → Environment `api-gap-coordinator` → secret |
| `API_GAP_BACKEND_TOKEN` | coordinator reads/writes backend tracking issues, reads PRs and evidence files | `abdo-taher/capitalix` only | Issues: read/write, Pull requests: read, Contents: read, Metadata: read | same environment secret |
| `API_GAP_DISPATCH_TOKEN` | worker labels/comments the backend issue | `abdo-taher/capitalix` only | Issues: read/write, Metadata: read | worker host env file (`~/.config/capitalix-gap/worker.env`, mode 600) — never in Actions |
| agent credential | the coding agent's own model login | n/a | dedicated revocable token (`claude setup-token`) | worker env file (`API_GAP_AGENT_CLAUDE_CODE_OAUTH_TOKEN`) |
| (operator's git/gh login) | pushes `gap/*` branches, opens the Draft PR | `abdo-taher/capitalix` | Contents: write, Pull requests: write — prefer a push-only deploy key/App | operator host |

The two coordinator tokens must be **separate** (preflight fails if the intake token can read the backend repository).

Set secrets without leaking them (reads from a prompt, not from argv or history):

```sh
gh secret set API_GAP_GITHUB_TOKEN  --env api-gap-coordinator -R abdo-taher/project-shared-docs   # paste at the prompt
gh secret set API_GAP_BACKEND_TOKEN --env api-gap-coordinator -R abdo-taher/project-shared-docs
install -m 600 /dev/null ~/.config/capitalix-gap/worker.env   # then edit; never `echo TOKEN=… >>`
```

Verify (prints PASS/WARN/FAIL per check, never a value): run the workflow with the flag on (below) or locally
`API_GAP_GITHUB_TOKEN=… API_GAP_BACKEND_TOKEN=… python3 automation/gap/gap_preflight.py`.
Rotate: create the new credential, update the secret, run the preflight, revoke the old one. Fine-grained PATs: ≤ 90
days. Revoke any token that was pasted in a chat or log immediately.

## 4. Enabling, running, disabling

State today: environment `api-gap-coordinator` exists (required reviewer = owner, deploy branch `main`), variable
`API_GAP_AUTOMATION_ENABLED=false`, **no secrets**, no schedule.

```sh
# enable a manual run (after secrets exist and the preflight passed)
gh variable set API_GAP_AUTOMATION_ENABLED --body true  -R abdo-taher/project-shared-docs
gh workflow run api-gap-coordinator.yml -R abdo-taher/project-shared-docs -f dry_run=true -f issues="12"
# disable immediately
gh variable set API_GAP_AUTOMATION_ENABLED --body false -R abdo-taher/project-shared-docs
```

A scheduled or unattended run is deliberately not provided: it needs a reviewed change adding a `schedule:` trigger.
Worker: `python3 automation/gap/gap_worker.py run` under a supervised user unit; stop with the unit or `SIGTERM`
(running dispatches are failed visibly, containers killed, login copy removed). `gap_worker.py health` reports state.

## 5. Approvals (never automatic)

- `gap-dispatch::approved` on the backend issue: must be added by a collaborator with **write** access; it is verified
  from the label event's actor, never from text. Sensitive gaps (money, auth, tenancy, integrations, …) also need
  `gap-owner::approved` by an owner login in `policy.json`. The automation never applies these labels.
- Merging a gap PR, publishing a contract and the owner's contract approval stay manual.

## 6. Tests

```sh
python3 -m unittest discover -s automation/gap/tests     # 242 tests; Docker-backed ones skip without the image
python3 -m unittest discover -s tools/tests              # consumer tooling + shared conformance corpus
docker run --rm -v "$PWD:/repo" -w /repo rhysd/actionlint:1.7.7 .github/workflows/api-gap-*.yml
docker build -f automation/gap/image/gap-agent.Dockerfile -t capitalix-gap-agent:2 automation/gap/image   # sandbox image
```

## 7. Canary and evidence

Create: `capitalix_gap.py new … && capitalix_gap.py submit <file>`; then run the coordinator for that issue. Inspect:
the coordinator's state comment on the intake issue, the backend issue's labels/comments, the PR body (validation
results), the workflow run summary (`gap-report.md`). Evidence file: `docs/api-gap/resolutions/<fp16>.json`.
Negative control: `python3 automation/gap/check_resolutions.py --contract <published openapi.json> --expect-failure`.

## 8. Recovery

| Symptom | Action |
|---|---|
| coordinator run interrupted | re-run: it is idempotent (one backend issue per fingerprint; state comments edited in place) |
| issue parked `BLOCKED/PERMANENT_FAILURE` | fix the cause, re-run with `--replay <n>` |
| dispatcher crashed | `gap_dispatch.py recover` (also at worker start): fails the dispatch visibly, releases the lease, kills labelled containers, deletes the login copy |
| `gap-dispatch::failed` label | a writer removes it (or `--retry`) after reading the failure note |
| wrong/duplicate backend issue | close one; the coordinator converges on the oldest per fingerprint |

## 9. Publication — how it is verified, and the limit

Authoritative artifact: `api/implemented/current.json` → `versions/<v>/openapi.json` in `project-shared-docs`, whose
sha256 is pinned in the manifest and re-verified by every client and by the coordinator. The manifest records a source
commit, approval id and pipeline URLs from the **release system outside GitHub**; that system is not contacted or
changed here, and approvals are HMAC-signed with a key consumers cannot check. Therefore:

- *Verified independently by this automation:* digest integrity of the published bytes, and that the published contract
  satisfies the fix's evidence checks (and did not before).
- *Not verifiable from GitHub:* that the published contract was built from the merged GitHub commit.
  A fix merged on GitHub reaches the published contract only if the external release process takes it. If it does not,
  the state stays `MERGED_NOT_PUBLISHED` indefinitely — by design. A GitHub-only release path would be a separate,
  owner-approved project.
