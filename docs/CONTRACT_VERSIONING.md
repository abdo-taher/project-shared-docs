# Contract versioning

## Identity

- Version id: `YYYY.MM.DD-<sha256[:12]>` — the UTC date of the source commit
  and the first 12 hex characters of the contract's sha256.
- The full sha256 is the identity; the id is a readable handle for it.
- `api/implemented/versions/<version>/` is immutable: never rewritten or
  deleted. The publisher refuses to rewrite an existing version directory.
- `current.json` names the current approved version; `index.json` lists every
  version, oldest first, with digest, source commit and compatibility summary.

## Publication rules (enforced by the publisher)

- Only bytes signed in the approval manifest are published.
- Publishing bytes that are already published is a no-op.
- A publication from an older source commit than the current version is
  refused (re-running an old pipeline cannot roll the contract back).
- Re-publishing a previously published but no-longer-current version is
  refused; a rollback is a new, approved change in the backend.

## Pinning and updates (consumers)

- `init` pins `current`; `init --version <v>` pins a specific version.
- `contract.lock` records version, sha256, manifest sha256, source commit.
- `verify` checks the local files; `verify --remote` also checks the
  published manifest for the pinned version.
- `status` compares the pin with `current.json` and lists newer versions with
  their compatibility summary; it never changes the pin.
- `update [--version <v>]` moves the pin explicitly and prints added/removed
  operations. Do it in a dedicated change, then run tests and `check`.
- Reproducing an issue: check out the consumer commit; its
  `contract.lock` names the exact contract; `sync` restores the bytes.

## Compatibility and the breaking-change policy

Each publication is compared with the previous approved contract:

| Class | Effect |
|---|---|
| `DOCUMENTATION_ONLY`, `NON_BREAKING` | allowed; recorded in the manifest |
| `BREAKING` | **blocked** — the pipeline fails |
| `UNKNOWN` (cannot be classified) | **blocked** — treated as breaking |

An intentional breaking change is made **additively**, never in place:

1. Add the new route/field alongside the old one (non-breaking), publish.
2. Mark the old one `deprecated` (documentation-only), publish; consumers
   migrate and `update` their pins.
3. Removing the old route is a breaking change and stays blocked by this
   pipeline. It requires a deliberate owner decision to change the gate
   (`--fail-on-breaking`) in a reviewed MR — there is no silent exception.

The approval manifest can record `allow_breaking`/`allow_unknown` scope, but
the validation gate still blocks such changes today; the scope fields exist so
an owner-approved policy change does not need a new approval format.

## Initial publication

The very first approved version has no previous contract to compare with.
It is allowed only when explicitly opted in, only before any approval exists
in the history, and the signed manifest records `initial_publication: true`.
Its manifest says `baseline.initial_publication: true`.
