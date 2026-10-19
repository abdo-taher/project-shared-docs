# Branch protection plan for `main` (not yet enabled)

Status: **proposed**. Nothing below has been applied. Audit date 2026-10-19.

## Current state (audited)

| Item | Finding |
|---|---|
| Classic branch protection | none (`404 Branch not protected`) |
| Rulesets | none (repository and branch rules: 0) |
| Writers to `main` | (1) pull-request merges by the owner; (2) GitLab `alalmiyalhura/capitalix` `publish_shared_api_docs` — direct push with the SSH deploy key 166881222 (write), `api/implemented/` only; (3) GitHub `abdo-taher/capitalix` "Publish Shared Documentation" — direct push with its `SHARED_DOCS_TOKEN` secret (acts as the owner's user), `business/` only |
| How publishers push | `git pull --rebase origin main` then a normal `git push` — never a force push, never a branch deletion |
| CI checks on pull requests | `tool`, `reference-consumer` (workflow `contract-toolkit`, runs on every PR) |

## Goal

Block force pushes and deletion of `main`; require reviewed, green pull
requests for human changes; keep both automated publishers working with the
least privilege available.

## Rulesets

### Ruleset 1 — `main-integrity` (safe to enable first)

No bypass actors. Neither publisher force-pushes or deletes, so nothing breaks.

```sh
gh api -X POST repos/abdo-taher/project-shared-docs/rulesets --input - <<'EOF'
{
  "name": "main-integrity",
  "target": "branch",
  "enforcement": "active",
  "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
  "rules": [{"type": "deletion"}, {"type": "non_fast_forward"}],
  "bypass_actors": []
}
EOF
```

### Ruleset 2 — `main-reviewed-changes` (enable after step 3 below)

Require a pull request with the two checks; let only the publishers bypass.

```sh
gh api -X POST repos/abdo-taher/project-shared-docs/rulesets --input - <<'EOF'
{
  "name": "main-reviewed-changes",
  "target": "branch",
  "enforcement": "active",
  "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
  "rules": [
    {"type": "pull_request", "parameters": {
      "required_approving_review_count": 0,
      "dismiss_stale_reviews_on_push": true,
      "require_code_owner_review": false,
      "require_last_push_approval": false,
      "required_review_thread_resolution": true}},
    {"type": "required_status_checks", "parameters": {
      "strict_required_status_checks_policy": false,
      "required_status_checks": [{"context": "tool"}, {"context": "reference-consumer"}]}}
  ],
  "bypass_actors": [
    {"actor_type": "DeployKey", "bypass_mode": "always"}
  ]
}
EOF
```

`required_approving_review_count` is 0 because the repository has a single
maintainer; raise it when a second reviewer exists.

## How automated publishing keeps working

| Publisher | Under Ruleset 1 | Under Ruleset 2 |
|---|---|---|
| GitLab publish job (deploy key) | fast-forward push: allowed | bypasses as `DeployKey` |
| GitHub `capitalix` workflow (token) | fast-forward push: allowed | **would be blocked** — it pushes directly as a user, and only deploy keys bypass |
| Owner | merges PRs: allowed | merges green PRs; direct pushes blocked |

Therefore, before Ruleset 2:

3. **Move the GitHub `capitalix` publisher to its own deploy key** (least
   privilege, and it retires the account-wide token):
   `ssh-keygen -t ed25519 -N '' -f shared-docs-business`, then
   `gh repo deploy-key add shared-docs-business.pub --allow-write -R abdo-taher/project-shared-docs`,
   `gh secret set SHARED_DOCS_DEPLOY_KEY -R abdo-taher/capitalix < shared-docs-business`,
   and in its workflow replace `token: ${{ secrets.SHARED_DOCS_TOKEN }}` with
   `ssh-key: ${{ secrets.SHARED_DOCS_DEPLOY_KEY }}` on the shared-docs checkout.
   Then delete the `SHARED_DOCS_TOKEN` secret and revoke that token.

   Alternative without changing that workflow: add
   `{"actor_type": "RepositoryRole", "actor_id": 5, "bypass_mode": "always"}`
   (Admin) to Ruleset 2. That keeps it working but lets the owner's token and
   account bypass review as well — weaker.

## Order and verification

1. Enable Ruleset 1. Verify: `git push --force` to `main` is rejected; the next
   GitLab publication still succeeds.
2. Do step 3; verify one GitHub `capitalix` publication succeeds with the deploy key.
3. Enable Ruleset 2. Verify: a direct push from a user is rejected; a PR without
   green `tool`/`reference-consumer` cannot merge; the next GitLab publication
   succeeds (its job log shows `SHARED_API_DOCS_PUBLISHED` or `NO_CONTRACT_CHANGES`
   and `published contract OK`).

Rollback: `gh api -X DELETE repos/abdo-taher/project-shared-docs/rulesets/<id>`.
A blocked publication fails closed (no partial write) and can be re-run after
rollback.

## Limits

- Path-scoped push rules (e.g. GitLab may write only `api/implemented/`) need
  push rulesets, which this plan does not assume are available on the
  account's plan; the separation is enforced by each publisher's code instead.
- `DeployKey` bypass applies to every write deploy key on the repository: keep
  only the publishers' keys.
