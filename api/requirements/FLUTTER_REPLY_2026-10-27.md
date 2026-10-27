# Reply to the Flutter developer — owner app backend issues (re-check 2026-10-27)

Against contract `2026.10.26-551d198a747e`. Proof for each item is in `docs/reference/CONTRACT_ISSUES_STATUS_2026-10-26.md` (commit `99615ebc`). Items marked **changed today** are in the working tree and will carry a new contract label once published.

## Open issues

| ID | Status | What to do in the app |
|---|---|---|
| p4-19 | Already fixed in `docs/api/openapi.json` | `document` is `type: string, format: binary` in both multipart bodies: `POST /api/owner/expenses/expenses` and `POST /api/owner/expenses/expenses/{reference}/resubmit`. On create it is optional (PDF/JPEG/PNG, max 5 MB). On resubmit it is optional and the old file stays if omitted. If you still see `string` only, you have a stale copy of the contract. Re-pull it. |
| p5-09 | **Use the owner route** | `{id, hero, sections}` (+ `branches`) is returned by `GET /api/owner/accounting/financial-statements/{statement}`, not by `/api/auth/accounting/...`. Per ADR-030 the auth route keeps its own payload and is not owner-shaped. Slugs: `income-statement` → income, `financial-position` → balance, `cash-flows` → cash_flow. Pass `from_date` / `to_date`. **Decision (owner, 2026-10-27): use the owner route.** Switch the three screens to the `/api/owner/...` path. The auth route stays unchanged and p5-09 is closed on the backend side. |
| p5-14 | **Changed today** | `data.sources[].type` and `data.documents[].type` use the same values: `sales` (output VAT), `purchase` and `expense` (input VAT). The contract example is corrected from `sales_invoice` / `input` to these values. Your parser (sales*/output, purchase/supplier/input, expense) already covers them. |
| #15 | Done | `GAP_REPORT.md` is regenerated for the 2026.10.26 contract (sha `faeedcf46ba5`). PR: https://github.com/abdo-taher/project-shared-docs/pull/39 |

### p5-09 — the three endpoints affected (call the owner route, never the auth twin)

| Use (owner-shaped) | Do not use (auth twin, different payload) |
|---|---|
| `GET /api/owner/accounting/financial-statements` | `GET /api/auth/accounting/financial-statements` |
| `GET /api/owner/accounting/financial-statements/{statement}` | `GET /api/auth/accounting/financial-statements/{statement}` |
| `GET /api/owner/accounting/reports/trial-balance` | `GET /api/auth/accounting/reports/trial-balance` |

Of the 79 owner-shaped operations in the contract, only these 3 have an auth twin, so no other endpoint can be mixed up this way.

## Items to confirm (runtime) — all resolved and covered by tests

| ID | Answer |
|---|---|
| #20 | Resolved. Uploading the proof links it to the subscription payment in either order (payment then proof, or proof then payment). `registration-request` shows the payment under review with the proof attached. |
| #21 | Resolved. After the proof, the application moves collecting → pending_review, and `registration-request` returns `under_review`. |
| #23 | Resolved. The registration code goes by SMS to the entered mobile (email only if no phone). Password-recovery and new-mobile codes are SMS. |
| #25 | Resolved. Logout removes the device token by the `DeviceId` header and does not register it again. No push is sent to that token afterwards. |
| #28 | Resolved. PO create and PATCH accept the numeric supplier id from the suppliers list, or the UUID. An unknown supplier gives 422 `SUPPLIER_NOT_FOUND`. |
| #29 | Resolved. `send_status` now follows the delivery: `SENT` or `SEND_FAILED` (it was only `NOT_SENT` / `SEND_REQUESTED`). The message carries the PO number and link token. |
| #32 | Resolved. Booking requests the Meet link, and the book response and meetings list carry `meet_link`. If the provider fails, the booking stays, `meet_link` is null, and a retry route exists. |
| p4-22 | **Confirmed — no merge needed in the app.** `GET /api/owner/purchases/purchase-orders` with no `type` filter returns POs and direct purchases together (direct items have `type: direct`). `type=direct` lists direct purchases only. `purchase-orders/{id}` also opens a direct purchase in the §8.2 shape. |

## Caveats

- #23, #29 and #32 are verified against the SMS, WhatsApp and Meet simulators in tests. Real delivery depends on the provider credentials configured per environment. On a staging environment without them, expect simulator behaviour (`meet_link` stays null, WhatsApp is `SEND_FAILED`). Tell us the environment if a real send fails.
- Please re-test #20, #21, #28 and p4-22 against the staging build and report only the ones that still fail.
