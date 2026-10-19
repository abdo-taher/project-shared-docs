# Proposal: GitHub-only publication of the official API contract

**Status: IMPLEMENTED (not yet cut over) — see [GITHUB_PUBLICATION.md](GITHUB_PUBLICATION.md).** This file is the
original proposal and is kept for the decisions it records. Differences in the build: provenance uses GitHub's run record
because artifact attestations are unavailable for private repositories on this plan.

## 1. Verified facts (from this repository and the GitHub API only)

- Authoritative artifact: `api/implemented/current.json` → `versions/<v>/openapi.json` (+ `manifest.json`,
  `approval.json`); the sha256 in the pointer/manifest is verified by every client and by the coordinator.
- The only version published is `2026.10.18-06d388692794`, commit `9b698bf` of this repository, authored by
  `capitalix-gitlab-ci`, whose manifest names **source `alalmiyalhura/capitalix@2429b7d2`**, a pipeline URL and a
  job URL on another system.
- The repository has one **read/write deploy key** titled "capitalix GitLab CI publisher (api/implemented)": that is how
  the publisher writes to `main`. `main` has **no branch protection**.
- The approval is an HMAC keyed by a secret held by that external system; consumers cannot verify it, only the digests.
- `docs/CONTRACT_VERSIONING.md` fixes the rules the publisher enforces (immutable versions, no-op on identical bytes,
  compatibility classes, signed approval manifest).

**Conclusion:** the existing publisher builds from a commit of a repository that is not the GitHub backend, so a fix
merged into `abdo-taher/capitalix` **cannot** reach the official contract through it, and the provenance of a published
contract cannot be tied to a GitHub commit. Nothing in this automation substitutes for or bypasses that process; fixes
stay `MERGED_NOT_PUBLISHED` until the owner decides how publication should work.

## 2. Smallest viable GitHub-only design

1. **Build (in `capitalix`)** — workflow `contract-publish.yml`, trigger `workflow_dispatch` (later optionally on a
   signed release tag), run on a ref of `integration/E01-FOUNDATION-SAAS`:
   composer install → `php artisan openapi:generate` → the repository's OpenAPI quality gates → sha256 → compatibility
   classification against the current published version (reuse `tools/capitalix_contract.py` logic, BREAKING/UNKNOWN need
   an explicit owner scope as today).
2. **Provenance** — `actions/attest-build-provenance` on `openapi.json`: a signed GitHub attestation binding the digest
   to repository, commit, workflow and run. The manifest's `source` becomes `{repository: abdo-taher/capitalix, commit,
   run_url, attestation}`; consumers/coordinator can check with `gh attestation verify` (no shared secret).
3. **Propose, never push** — the workflow opens a PR in `project-shared-docs` adding
   `api/implemented/versions/<v>/` and updating `current.json`/`index.json`. An App installation token limited to
   `project-shared-docs` with Contents + Pull requests write (minted in the job; key in an environment with a required
   reviewer) is the only credential.
4. **Approval** — the owner approves by reviewing and merging that PR; protect `main` (required review by CODEOWNERS,
   required checks `contract-toolkit`, deploy key removed or restricted to a non-`main` branch). `approval.json` v2
   records the merging reviewer and PR number instead of the external HMAC.
5. **Verification** — after merge, a shared-docs workflow re-verifies digests and the attestation, and fails the
   `main` check if `current.json` disagrees with the bytes. The coordinator then needs no change: it already treats the
   published contract content as the proof and can additionally require the attestation commit to descend from the merge
   commit of the fix (`provenance: attested`).
6. **Rollback** — versions are immutable; roll back by a PR reverting `current.json`/`index.json` to the previous version
   (clients that pinned the bad version keep their pin until they upgrade). Revoke the App key to stop publication.

## 3. Open owner decisions (why this is not built)

- Retire or freeze the GitLab publisher: two writers of `current.json` must never coexist.
- Accept a new approval format (merge-based) in place of the HMAC manifest, and update `CONTRACT_VERSIONING.md`.
- Resolve the development-branch gap already seen in the earlier dry-run: `openapi:quality` is not registered in
  development, so the quality gates cannot yet run there.

## 4. Acceptance criteria

- A dry-run on the current development head produces a candidate byte-identical to a second run (determinism).
- Re-publishing identical bytes is a no-op; an existing version directory is never rewritten.
- A tampered `openapi.json` fails the digest check; an unattested or foreign-repository attestation fails verification.
- The workflow cannot write to `main` of `project-shared-docs` directly (branch protection test).
- A fix PR merged on GitHub appears in a candidate; the coordinator moves the gap to `CONTRACT_PUBLISHED` only after the
  owner merges the publication PR and the checks hold, and only then.
- Revert of the publication PR returns `current.json` to the previous version and the coordinator returns the gap to
  `MERGED_NOT_PUBLISHED`.
