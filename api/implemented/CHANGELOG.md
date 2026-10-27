# Consumer-visible contract changes

Newest first. Each entry names what consumers must do. The exact operation
diff of every published version is in `versions/<version>/compatibility.md`.

## 2026.10.27-abe5a72d2ae0

Built by abdo-taher/capitalix@71d380a36251 (run https://github.com/abdo-taher/capitalix/actions/runs/40472403917). Changes vs the previous version: 0 breaking, 0 unclassified, 0 non-breaking, 2 documentation-only. Full list: `versions/2026.10.27-abe5a72d2ae0/compatibility.md`. Upgrade explicitly: `python3 tool/capitalix_contract.py update --version 2026.10.27-abe5a72d2ae0`, then run your tests.

## 2026.10.26-551d198a747e

Built by abdo-taher/capitalix@2c8b16b79cc7 (run https://github.com/abdo-taher/capitalix/actions/runs/40329737750). Changes vs the previous version: 128 breaking, 22 unclassified, 1172 non-breaking, 138 documentation-only. Full list: `versions/2026.10.26-551d198a747e/compatibility.md`. Upgrade explicitly: `python3 tool/capitalix_contract.py update --version 2026.10.26-551d198a747e`, then run your tests.

## 2026.10.26-3e5f85a9fe98

Built by abdo-taher/capitalix@952732c413d5 (run https://github.com/abdo-taher/capitalix/actions/runs/40292671661). Changes vs the previous version: 455 breaking, 35 unclassified, 848 non-breaking, 222 documentation-only. Full list: `versions/2026.10.26-3e5f85a9fe98/compatibility.md`. Upgrade explicitly: `python3 tool/capitalix_contract.py update --version 2026.10.26-3e5f85a9fe98`, then run your tests.

## 2026.10.25-7530c9a3319d

Built by abdo-taher/capitalix@cb85f7b33756 (run https://github.com/abdo-taher/capitalix/actions/runs/40194461614). Changes vs the previous version: 8 breaking, 0 unclassified, 89 non-breaking, 23 documentation-only. Full list: `versions/2026.10.25-7530c9a3319d/compatibility.md`. Upgrade explicitly: `python3 tool/capitalix_contract.py update --version 2026.10.25-7530c9a3319d`, then run your tests.

## 2026.10.21-6846e086006f

Built by abdo-taher/capitalix@9d5502f689ae (run https://github.com/abdo-taher/capitalix/actions/runs/39585984564). Changes vs the previous version: 602 breaking, 32 unclassified, 1887 non-breaking, 389 documentation-only. Full list: `versions/2026.10.21-6846e086006f/compatibility.md`. Upgrade explicitly: `python3 tool/capitalix_contract.py update --version 2026.10.21-6846e086006f`, then run your tests.

## First approved publication (contract v4)

No earlier contract was ever approved or published, so there is nothing to
migrate from. Facts consumers must rely on, corrected in this publication
after validating real backend traffic against the contract:

| Area | Contract now says (and the backend returns) | Consumer action |
|---|---|---|
| Lists (145 operations) | `data: {items: [...]}`; paginated lists also `data.meta: {current_page, last_page, total}` | read `data.items` / `data.meta`, never a bare `data` array |
| Empty payloads (e.g. DELETE) | `data: {}` | do not expect `data: null` |
| `POST /api/auth/login` 201 | `data` is a token object **or** the user object (with `token`) | read `data.token` |
| User object `phone` | `string \| null` | handle null |
| User object `has_subscription` | `boolean` | parse as boolean |
| `customer-balances` rows `mobile` | `string \| null` | handle null |

Canonical routes are `/api/owner|accountant|admin|auth|public/...`; `/api/v1/*`
are deprecated aliases (`x-canonical-replacement` names the successor).
