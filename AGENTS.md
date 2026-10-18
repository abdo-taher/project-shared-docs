# Shared Documentation Agent Rules

This repository is the source of truth for shared API contracts
and approved business rules.

Before implementing any API-dependent task:

1. Fetch the latest documentation from the default branch.
2. Read the relevant Markdown files.
3. Check API contracts and breaking changes.
4. Compare the contracts with the local implementation.
5. Apply required code changes.
6. Run relevant tests.
7. Report any incompatible or missing contracts.

Never assume that locally cached documentation is current.

Never modify approved API contracts without coordination
with the backend owner.
