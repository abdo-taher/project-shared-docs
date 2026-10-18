# Consumer-visible contract changes

Newest first. Each entry names what consumers must do. The exact operation
diff of every published version is in `versions/<version>/compatibility.md`.

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
