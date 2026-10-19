# Capitalix Implemented API Contracts

Source: GitHub abdo-taher/capitalix, branch integration/E01-FOUNDATION-SAAS
(version 2026.10.18-06d388692794 is historical: it was published from the former GitLab
production repository and keeps that provenance forever, because versions are immutable)

This directory contains consumer-facing API documentation
verified against the actual Laravel implementation.

Rules:

1. Document implemented APIs only.
2. Keep requests and responses accurate.
3. Describe authentication and permissions.
4. Document breaking changes.
5. Do not publish credentials or private configuration.
6. Update contracts when API behavior changes.
7. Do not treat planned features as implemented APIs.

## Layout

| Path | |
|---|---|
| `current.json` | the current approved version (version, sha256, source commit) |
| `index.json` | every published version, oldest first |
| `versions/<version>/openapi.json` | immutable contract bytes |
| `versions/<version>/manifest.json` | digest, source commit, pipeline/job, approval evidence, compatibility |
| `CHANGELOG.md` | consumer-visible changes and required actions |

Pin and use the contract with `tools/capitalix_contract.py`
(see `docs/DEVELOPER_QUICKSTART.md` in this repository). Written only by the
the `contract-publish` workflow of this repository, through a pull request the owner approves
(see `docs/api-gap/GITHUB_PUBLICATION.md`).

