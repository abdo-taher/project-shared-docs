# Owner-app requirements vs. the published contract

| File | |
|---|---|
| `GAP_REPORT.md` | generated report: every endpoint in `api/BACKEND_API.md` against the current contract |
| `owner-app-map.json` | reviewed / live-verified mappings (highest precedence) |
| `owner-app-bindings.json` | the backend's Owner-API conformance bindings (name → route), with provenance |

Regenerate against the current published contract:

```sh
python3 tools/capitalix_contract.py --dir /tmp/pin init --source github:abdo-taher/project-shared-docs
python3 tools/capitalix_contract.py --dir /tmp/pin gap api/BACKEND_API.md \
  --map api/requirements/owner-app-map.json --bindings api/requirements/owner-app-bindings.json \
  --out api/requirements/GAP_REPORT.md
```

Refresh the bindings from the backend development repository:

```sh
git -C ../capitalix show <commit>:tests/Feature/ApiContract/Owner/bindings.json  # then wrap as {"source": {...}, "bindings": {...}}
```

Statuses never claim more than the evidence: path-suffix candidates are marked
for review, and response shapes are only compared where a mapping was
exercised against a running backend.
