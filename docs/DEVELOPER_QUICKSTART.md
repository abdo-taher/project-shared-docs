# Developer quickstart — use the Capitalix API contract

For frontend/mobile developers (React, Flutter, …). Ten minutes, no backend
checkout needed.

## Prerequisites

- Python 3.9+ (no packages).
- Read access to `abdo-taher/project-shared-docs`: either `gh auth login`, or
  a `GITHUB_TOKEN` that can read the repository.

## 1. Connect your project (once)

```sh
mkdir -p tool
gh api -H "Accept: application/vnd.github.raw+json" \
  repos/abdo-taher/project-shared-docs/contents/tools/capitalix_contract.py > tool/capitalix_contract.py
python3 tool/capitalix_contract.py init
```

`init` downloads the **current approved** version, checks its sha256 against
the published manifest, and writes `.capitalix-contract/`:

| File | Meaning |
|---|---|
| `openapi.json` | the exact approved contract bytes |
| `manifest.json` | version, digest, source commit, approval evidence |
| `contract.lock` | what is pinned and the digests that must match |

Commit `tool/capitalix_contract.py` and `.capitalix-contract/`. If you prefer
not to commit the 6 MB `openapi.json`, gitignore it and run
`python3 tool/capitalix_contract.py sync` after cloning (it restores and
verifies the pinned version).

Copy `docs/AI_AGENT_INSTRUCTIONS.md` into your project's `AGENTS.md` (or
`CLAUDE.md`) so your coding agent follows the same rules.

## 2. Daily commands

```sh
python3 tool/capitalix_contract.py status            # pinned version, integrity, newer versions?
python3 tool/capitalix_contract.py verify --remote   # digest + published manifest + source commit
python3 tool/capitalix_contract.py list owner sales  # compact operation index
python3 tool/capitalix_contract.py inspect customers --method POST owner
python3 tool/capitalix_contract.py check lib/        # every API path in code exists in the contract
```

`inspect` prints only the matching operations, with parameters, request body,
responses, auth (`security`) and permission (`access`) fully resolved — about
15 KB for a feature instead of the whole 6 MB contract.

## 3. Implement a feature (the workflow)

1. `inspect` the feature's operations; note the contract `version`.
2. Use the **canonical** paths (`/api/owner|accountant|admin|auth|public/...`).
   `/api/v1/*` are deprecated aliases.
3. Build requests from the schema: exact field names, enums, required fields.
   Responses are `{message, data}`; lists are `data.items` with `data.meta`
   (`current_page`, `last_page`, `total`); errors are
   `{message, errors, code, correlation_id, details}`.
4. Generate test fixtures from the contract, never by hand:
   `python3 tool/capitalix_contract.py sample owner.sales.customers.store --status 201`.
5. Record your client's requests/responses in tests and validate them:
   `python3 tool/capitalix_contract.py validate build/traffic.json`.
6. `check` your source tree. Commit; mention the contract version in the PR.

A complete, tested example of this workflow is
`examples/dart-owner-customers/` (Owner app Customers: list with pagination,
create, update, delete, 401/403/409/422 handling).

## 4. A newer contract was published

`status` lists newer versions with their compatibility summary. Update
deliberately, in its own change:

```sh
python3 tool/capitalix_contract.py update        # or --version <version>
```

It prints added/removed operations. Run your tests and `check`, then commit
the new `.capitalix-contract/`.

## 5. Something you need is missing

Do not invent it. Run the gap report and raise it with the backend:

```sh
python3 tool/capitalix_contract.py gap path/to/requirements.md --out gap.md
```

The owner-app report is in `api/requirements/GAP_REPORT.md`.

## Troubleshooting

| Message | Meaning / fix |
|---|---|
| `SOURCE UNREACHABLE` | no network or no read access; your pinned copy still works offline |
| `openapi.json does not match the digest in contract.lock` | the pinned file was edited or corrupted — `sync` restores it |
| `downloaded contract digest … does not match` | a published file was tampered with or truncated; do not use it, report it |
| `no operation matches` | the operation is not in the contract; don't fabricate it |
| `NOT IN CONTRACT` (check) | your code calls an undocumented path |
| `FAIL` (validate) | a request or response violates the contract; the line says where |
