# Developer quickstart — use the Capitalix API contract

For frontend/mobile developers (Flutter, React, Next.js, Vue, Angular, …).
Ten minutes, no backend checkout needed.

## Prerequisites

- Python 3.9+ (standard library only — nothing to install).
- `curl` (or any way to download one file).
- **No GitHub account, token or `gh` login**: `abdo-taher/project-shared-docs`
  is public, and the tool reads it anonymously over HTTPS.

Private mirror instead of the public repository? Then the tool needs read
access: set `GITHUB_TOKEN` (or `GH_TOKEN`), or log in with `gh auth login`.
The tool tries anonymous access first and uses a logged-in `gh` only when
anonymous access cannot see the file.

## 1. Connect your project (once)

```sh
mkdir -p tool
curl -fsSL -o tool/capitalix_contract.py \
  https://raw.githubusercontent.com/abdo-taher/project-shared-docs/main/tools/capitalix_contract.py
python3 tool/capitalix_contract.py init
```

Read `tool/capitalix_contract.py` before you commit it — it is a single,
dependency-free file. It never executes anything it downloads.

`init` downloads the **current approved** version and refuses to pin it unless
the contract's sha256 matches the published pointer and manifest, and the
approval evidence (`approval.json`) matches the manifest and approves exactly
these bytes. It writes `.capitalix-contract/`:

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

## Framework setup

The workflow is identical everywhere; only the source directory you `check`
differs. Commit `tool/` and `.capitalix-contract/` at the repository root.

| Stack | API code usually lives in | Check command |
|---|---|---|
| Flutter / Dart | `lib/` | `python3 tool/capitalix_contract.py check lib/` |
| React (Vite, CRA) | `src/` | `python3 tool/capitalix_contract.py check src/` |
| Next.js | `app/`, `src/`, `pages/` (those that exist) | `python3 tool/capitalix_contract.py check app/ src/` |
| Vue | `src/` (`.vue` files are not scanned by default) | `python3 tool/capitalix_contract.py check src/ --ext .vue,.ts,.js` |
| Angular | `src/app/` | `python3 tool/capitalix_contract.py check src/app/ --ext .ts` |

`check` looks for API path literals that start with `api/` or `/api/`. If your
client builds paths from a base such as `/api/owner` plus a relative path
(`'sales/customers'`), add `--prefix /api/owner` so relative literals are
checked too. Put endpoint paths in one constants file per feature (see
`examples/dart-owner-customers/lib/src/endpoints.dart`) so `check` sees them.

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

## Consumer CI (no secrets needed)

Run the same checks in CI. They fail on any integrity error and never move the
pin. Commit the tool so CI does not download code on every run.

GitHub Actions:

```yaml
contract:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - run: python3 tool/capitalix_contract.py sync            # only if openapi.json is gitignored
    - run: python3 tool/capitalix_contract.py verify --remote # pin == published, approval evidence intact
    - run: python3 tool/capitalix_contract.py check lib/      # your source directory
    - run: python3 tool/capitalix_contract.py status          # reports newer versions; never updates
```

GitLab CI:

```yaml
contract:
  image: python:3.12-alpine
  script:
    - python3 tool/capitalix_contract.py sync
    - python3 tool/capitalix_contract.py verify --remote
    - python3 tool/capitalix_contract.py check src/
```

Add `status --fail-if-outdated` only if you want CI to fail when a newer approved
version exists. Updating the pin stays a deliberate commit (`update`).

To refresh the committed tool itself, download it from a specific commit and
review the diff before committing:

```sh
curl -fsSL -o tool/capitalix_contract.py \
  https://raw.githubusercontent.com/abdo-taher/project-shared-docs/<commit-sha>/tools/capitalix_contract.py
git diff tool/capitalix_contract.py
```

## Troubleshooting

| Message | Meaning / fix |
|---|---|
| `SOURCE UNREACHABLE … timed out` / `rate limited` | network problem or GitHub throttling (the tool already retried); your pinned copy still works offline — retry later |
| `SOURCE UNREACHABLE … not found` | wrong `--version`, or a private repository: set `GITHUB_TOKEN` or run `gh auth login` |
| `HTTP 401 — the token … was rejected` | an invalid `GITHUB_TOKEN`/`GH_TOKEN` is set; unset it to use anonymous access to the public repository |
| `approval evidence does not match` / `does not approve this exact contract` | the published files are inconsistent or tampered with; do not use them, report it |
| `openapi.json does not match the digest in contract.lock` | the pinned file was edited or corrupted — `sync` restores it |
| `downloaded contract digest … does not match` | a published file was tampered with or truncated; do not use it, report it |
| `no operation matches` | the operation is not in the contract; don't fabricate it |
| `NOT IN CONTRACT` (check) | your code calls an undocumented path |
| `FAIL` (validate) | a request or response violates the contract; the line says where |
