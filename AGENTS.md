# Shared Documentation Agent Rules

This repository is the source of truth for shared API contracts and approved
business rules.

## Consumers (frontend / mobile projects)

Do not fetch "the latest" contract during feature work. Pin it and use the
pinned copy: follow [`docs/AI_AGENT_INSTRUCTIONS.md`](docs/AI_AGENT_INSTRUCTIONS.md)
(copy it into your project's AGENTS.md) and
[`docs/DEVELOPER_QUICKSTART.md`](docs/DEVELOPER_QUICKSTART.md).

## Working in this repository

- `api/implemented/` is written ONLY by the GitLab `alalmiyalhura/capitalix`
  publish job. Never edit it by hand; `versions/<version>/` is immutable.
- `business/` is written by the GitHub `abdo-taher/capitalix` "Publish Shared
  Documentation" workflow.
- `api/BACKEND_API.md` is the owner app's requirements (wishes), not the API.
- Changes to `tools/`, `docs/`, `examples/` go through a pull request; the
  `contract-toolkit` workflow must pass.
- Never fabricate API contracts; never modify approved contracts; report any
  incompatible or missing contract instead.
