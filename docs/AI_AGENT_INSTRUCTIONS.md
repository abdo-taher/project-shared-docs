# AI agent instructions — Capitalix API contract

Copy this section into the consumer project's `AGENTS.md` / `CLAUDE.md`.

## Capitalix API contract (mandatory for any API-dependent task)

The backend API is defined ONLY by the pinned contract in
`.capitalix-contract/` (`openapi.json`, `manifest.json`, `contract.lock`).
The tool is `tool/capitalix_contract.py` (Python 3, no packages).

Access: the contract repository is public. Do not ask for, create or export a
GitHub token, and do not run `gh auth login`, for read access. If a command
reports `SOURCE UNREACHABLE`, the pinned copy still works offline: continue with
it and report the network problem. Never bypass or edit around a failed
integrity check (`FAILED: …`) — stop and report it.

Before writing API code:

1. `python3 tool/capitalix_contract.py verify` — stop if it fails.
2. `python3 tool/capitalix_contract.py inspect <feature words> [--method M]`
   — read ONLY the operations you need. Do not load the whole `openapi.json`
   into context.
3. Note the contract `version` from the output; cite it in your summary/PR.

While implementing:

- Use the exact method and canonical path from `inspect`
  (`/api/owner|accountant|admin|auth|public/...`; never `/api/v1/*` aliases).
- Use the exact parameter and field names, enums, required fields, auth
  (`security`) and permission (`access`) from the schema.
- Responses: `{message, data}`; lists are `data.items` + `data.meta`
  (`current_page`, `last_page`, `total`); errors are
  `{message, errors{field:[...]}, code, correlation_id, details}` with
  401/403/404/409/422 as documented per operation.
- Reuse the project's existing HTTP client, models and error conventions.
- Build test fixtures with `sample <operationId> --status <code>`; never hand-write
  response shapes.
- Never invent an endpoint, parameter, field or enum value. If `inspect` finds
  nothing, or the contract cannot express what the task needs, STOP that part
  and report: what is missing, which requirement needs it, contract version.
- `api/BACKEND_API.md`-style requirement documents are wishes, not the API.
  Where they disagree with the contract, follow the contract and report the
  difference.

Before finishing:

1. `python3 tool/capitalix_contract.py check <source dir>` — no `NOT IN CONTRACT`.
2. Run the project's tests; if they record HTTP traffic, run
   `python3 tool/capitalix_contract.py validate <traffic.json>`.
3. Report the contract version used and any missing/mismatched operations.

Never during ordinary feature work:

- edit anything in `.capitalix-contract/`;
- run `update` or `init --force` (moving the pin is a separate, explicit task);
- fetch the "latest" contract from the network instead of the pin.

`python3 tool/capitalix_contract.py status` may be run to report whether a
newer approved version exists; report it, do not apply it.

### When the contract lacks what the task needs

1. Confirm with `inspect` that it is really absent or different.
2. Create a structured request — never a free-text guess:
   `python3 tool/capitalix_gap.py new --type <TYPE> --actor <actor> ...`
   (types and fields: `docs/DEVELOPER_QUICKSTART.md` section 5). For a missing
   operation use `--capability` and `--location`; never invent a path.
3. `python3 tool/capitalix_gap.py search <file>`; if it is already reported,
   cite that issue instead of filing again.
4. Submit only if your task or your user allows filing issues; otherwise leave
   the request file and report it. If `submit` says `NOT_SUBMITTED`, say so —
   never claim it was filed.
5. Evidence must be sanitized: no tokens, cookies, passwords, personal data.
6. Do not upgrade the pin to pick up a fix during unrelated work; `status
   <issue>` reports when a fix is published, and upgrading is its own task.
