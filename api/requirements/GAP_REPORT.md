# GAP_REPORT — Capitalix backend vs owner-app contract

Generated 2026-10-26 from `docs/api/openapi.json` (sha256 `faeedcf46ba5`, 1286 operations, branch `direct/contract-fixes-2026-10-26`).
Supersedes the report for contract 2026.10.18-06d388692794 / 2026.10.25-7530c9a3319d. Contract label to use in the docs repo: **2026.10.26** + the sha above.

Scope of this report: response `data` that the contract still describes without keys (objects with no properties, arrays with no item type, untyped values). These are the fields a client cannot rely on from the contract alone. Nothing here is a runtime defect by itself.

## Issues resolved in this contract (owner-app list of 2026-10-26)

| Issue | Resolution |
|---|---|
| #8 | Subscription/renew carry bank_name, account_holder, account_number, iban, swift, vat_rate |
| #16 | renew + change-plan return data.payment.reference/status |
| #20/#21 | Registration proof linked to payment (both orders); application reaches pending_review/under_review |
| #23 | OTP by SMS (registration, recovery, new mobile) through the SMS simulator/provider port |
| #25 | Logout removes the device token and does not re-register it |
| #28 | PO create/PATCH accept numeric or UUID supplier ids |
| #29 | PO send through the WhatsApp simulator; send_status SENT / SEND_FAILED |
| #32 | Booking creates a Google Meet link (Meet simulator provider); list/details carry meet_link |
| p2-04 | Dashboard sections/kpis/quick_actions documented as string keys |
| p4-06 | Stock PUT persists unit + supplier_reference |
| p4-12 | PO and direct-purchase create document the created order |
| p4-13 | purchase form-options items[] keys documented |
| p4-18 | OCR data.fields §10.2 keys (incl. po_number), pending read via GET expenses/documents/{ref} |
| p4-19 | document is binary in create and resubmit |
| p4-21 | purchase-orders lists/opens direct purchases (§8.2); owner direct-purchases routes in §8 shape |
| p5-02 | Tax upload answers document_id + version |
| p5-04 | period_type/year/period/branch_id on report operations; ledger/waste dates optional |
| p5-05..p5-09 | Hub keys, account rows, journal rows/lines/owner_requests, statement slugs + mapping |
| p5-14 | VAT source/document types: sales, purchase, expense |
| p6-04 | Payroll create answers the §27 run shape |
| p6-09 | Payroll lines carry id; {lineId} accepts line id or employee id |

## Remaining documentation gaps by module

503 of 1286 operations still have at least one untyped part of the success `data` (objects without keys, arrays without an item type, untyped values). Up to 6 locations are listed per operation. These are documentation gaps only.

### Accountant / Accounting (38)

- `GET /api/accountant/accounting/journal-entries` (200) — `data.items` array without item type
- `GET /api/accountant/accounting/posting-mappings` (200) — `data.items[].assigned_by` untyped; `data.items[].ended_by` untyped; `data.items[].end_reason` untyped
- `POST /api/accountant/accounting/posting-mappings/{reference}/unassign` (200) — `data` object without keys
- `PUT /api/accountant/accounting/posting-mappings/{role}` (200) — `data` object without keys
- `GET /api/accountant/accounting/posting-requests` (200) — `data` object without keys
- `GET /api/accountant/accounting/posting-requests/{reference}` (200) — `data.lines` untyped; `data.corrected_by` untyped; `data.correction_reason` untyped
- `POST /api/accountant/accounting/posting-requests/{reference}/closed-period-correction` (200) — `data.lines` untyped; `data.corrected_by` untyped; `data.correction_reason` untyped
- `POST /api/accountant/accounting/posting-requests/{reference}/reprocess` (200) — `data.lines` untyped; `data.corrected_by` untyped; `data.correction_reason` untyped
- `GET /api/accountant/accounting/posting-roles` (200) — `data.items` array without item type
- `GET /api/accountant/accounting/posting-templates` (200) — `data.items[].roles` array without item type
- `POST /api/accountant/accounting/posting-templates/{template}/apply` (200) — `data` object without keys
- `GET /api/accountant/accounting/reconciliation/bank-statements` (200) — `data.items` array without item type
- `POST /api/accountant/accounting/reconciliation/bank-statements/{id}/reconcile` (200) — `data` object without keys
- `GET /api/accountant/accounting/reconciliation/bank-transactions` (200) — `data.items` array without item type
- `GET /api/accountant/accounting/reconciliation/reconciliation-items/{id}/history` (200) — `data` object without keys
- `POST /api/accountant/accounting/reconciliation/reconciliation-items/{id}/match` (200) — `data` object without keys
- `POST /api/accountant/accounting/reconciliation/reconciliation-items/{id}/resolve` (200) — `data` object without keys
- `POST /api/accountant/accounting/reconciliation/reconciliation-items/{id}/unmatch` (200) — `data` object without keys
- `GET /api/accountant/accounting/reconciliation/reconciliations/{id}` (200) — `data` object without keys
- `GET /api/v1/accounting/posting-mappings` (200) — `data.items[].assigned_by` untyped; `data.items[].ended_by` untyped; `data.items[].end_reason` untyped
- `POST /api/v1/accounting/posting-mappings/{reference}/unassign` (200) — `data` object without keys
- `PUT /api/v1/accounting/posting-mappings/{role}` (200) — `data` object without keys
- `GET /api/v1/accounting/posting-requests` (200) — `data` object without keys
- `GET /api/v1/accounting/posting-requests/{reference}` (200) — `data.lines` untyped; `data.corrected_by` untyped; `data.correction_reason` untyped
- `POST /api/v1/accounting/posting-requests/{reference}/closed-period-correction` (200) — `data.lines` untyped; `data.corrected_by` untyped; `data.correction_reason` untyped
- `POST /api/v1/accounting/posting-requests/{reference}/reprocess` (200) — `data.lines` untyped; `data.corrected_by` untyped; `data.correction_reason` untyped
- `GET /api/v1/accounting/posting-roles` (200) — `data.items` array without item type
- `GET /api/v1/accounting/posting-templates` (200) — `data.items[].roles` array without item type
- `POST /api/v1/accounting/posting-templates/{template}/apply` (200) — `data` object without keys
- `GET /api/v1/journal-entries` (200) — `data.items` array without item type
- `GET /api/v1/reconciliation/bank-statements` (200) — `data.items` array without item type
- `POST /api/v1/reconciliation/bank-statements/{id}/reconcile` (200) — `data` object without keys
- `GET /api/v1/reconciliation/bank-transactions` (200) — `data.items` array without item type
- `GET /api/v1/reconciliation/reconciliation-items/{id}/history` (200) — `data` object without keys
- `POST /api/v1/reconciliation/reconciliation-items/{id}/match` (200) — `data` object without keys
- `POST /api/v1/reconciliation/reconciliation-items/{id}/resolve` (200) — `data` object without keys
- `POST /api/v1/reconciliation/reconciliation-items/{id}/unmatch` (200) — `data` object without keys
- `GET /api/v1/reconciliation/reconciliations/{id}` (200) — `data` object without keys

### Accountant / Expenses (8)

- `GET /api/accountant/expenses/expenses` (200) — `data.items` array without item type
- `PUT /api/accountant/expenses/expenses/documents/{document}` (200) — `data.reviewed_fields` array without item type
- `GET /api/accountant/expenses/expenses/{expense_reference}/duplicate-candidates` (200) — `data.candidates` array without item type
- `GET /api/accountant/expenses/expenses/{reference}/journal-preview` (200) — `data.lines` array without item type
- `GET /api/v1/expenses` (200) — `data.items` array without item type
- `PUT /api/v1/expenses/documents/{document}` (200) — `data.reviewed_fields` array without item type
- `GET /api/v1/expenses/{expense_reference}/duplicate-candidates` (200) — `data.candidates` array without item type
- `GET /api/v1/expenses/{reference}/journal-preview` (200) — `data.lines` array without item type

### Accountant / General (12)

- `GET /api/accountant/general/depreciation-runs/{publicReference}` (200) — `data` object without keys
- `POST /api/accountant/general/depreciation-runs/{publicReference}/post` (202) — `data` object without keys
- `POST /api/accountant/general/depreciation-runs/{publicReference}/review` (200) — `data` object without keys
- `POST /api/accountant/general/vat-returns/{vatReturn}/approve` (200) — `data.reconciliation.details` untyped; `data.review` untyped
- `POST /api/accountant/general/vat-returns/{vatReturn}/export` (200) — `data` object without keys
- `GET /api/accountant/general/vat-returns/{vatReturn}/preparation` (200) — `data.reconciliation.details` untyped; `data.review` untyped
- `GET /api/v1/depreciation-runs/{publicReference}` (200) — `data` object without keys
- `POST /api/v1/depreciation-runs/{publicReference}/post` (202) — `data` object without keys
- `POST /api/v1/depreciation-runs/{publicReference}/review` (200) — `data` object without keys
- `POST /api/v1/vat-returns/{vatReturn}/approve` (200) — `data.reconciliation.details` untyped; `data.review` untyped
- `POST /api/v1/vat-returns/{vatReturn}/export` (200) — `data` object without keys
- `GET /api/v1/vat-returns/{vatReturn}/preparation` (200) — `data.reconciliation.details` untyped; `data.review` untyped

### Accountant / Integrations (12)

- `GET /api/accountant/integrations/integrations/purchase-orders/{purchaseOrderReference}/delivery` (200) — `data` object without keys
- `GET /api/accountant/integrations/integrations/sync-runs` (200) — `data.items[]` object without keys
- `POST /api/accountant/integrations/integrations/sync-runs` (201) — `data` object without keys
- `GET /api/accountant/integrations/integrations/sync-runs/{syncRun}` (200) — `data` object without keys
- `PUT /api/accountant/integrations/integrations/sync-runs/{syncRun}` (200) — `data` object without keys
- `PATCH /api/accountant/integrations/integrations/sync-runs/{syncRun}` (200) — `data` object without keys
- `GET /api/v1/integrations/purchase-orders/{purchaseOrderReference}/delivery` (200) — `data` object without keys
- `GET /api/v1/integrations/sync-runs` (200) — `data.items[]` object without keys
- `POST /api/v1/integrations/sync-runs` (201) — `data` object without keys
- `GET /api/v1/integrations/sync-runs/{syncRun}` (200) — `data` object without keys
- `PUT /api/v1/integrations/sync-runs/{syncRun}` (200) — `data` object without keys
- `PATCH /api/v1/integrations/sync-runs/{syncRun}` (200) — `data` object without keys

### Accountant / Inventory (5)

- `GET /api/accountant/inventory/catalog-products` (200) — `data.items[]` array without item type
- `GET /api/accountant/inventory/inventory/items` (200) — `data.summary` object without keys; `data.categories` array without item type; `data.items[]` object without keys
- `GET /api/v1/catalog-products` (200) — `data.summary.categories_count` untyped; `data.summary.sub_categories_count` untyped; `data.categories` untyped
- `GET /api/v1/catalog-products/{catalogProduct}` (200) — `data.recipe` untyped
- `GET /api/v1/inventory/items` (200) — `data.summary` object without keys; `data.categories` array without item type; `data.items[]` object without keys

### Accountant / Notifications (2)

- `GET /api/v1/erp/notifications` (200) — `data.notifications[].branch_name` untyped; `data.notifications[].business_name` untyped
- `GET /api/v1/erp/notifications/{uuid}` (200) — `data.branch_name` untyped; `data.business_name` untyped

### Accountant / Payroll (10)

- `POST /api/accountant/payroll/payroll-runs/{runId}/prepare-payment` (200) — `data` object without keys
- `POST /api/accountant/payroll/payroll/runs/{runId}/approve` (200) — `data` object without keys
- `POST /api/accountant/payroll/payroll/runs/{runId}/return-to-draft` (200) — `data` object without keys
- `GET /api/accountant/payroll/payroll/runs/{runId}/review` (200) — `data` object without keys
- `POST /api/accountant/payroll/payroll/runs/{runId}/review` (200) — `data` object without keys
- `POST /api/v1/payroll-runs/{runId}/prepare-payment` (200) — `data` object without keys
- `POST /api/v1/payroll/runs/{runId}/approve` (200) — `data` object without keys
- `POST /api/v1/payroll/runs/{runId}/return-to-draft` (200) — `data` object without keys
- `GET /api/v1/payroll/runs/{runId}/review` (200) — `data` object without keys
- `POST /api/v1/payroll/runs/{runId}/review` (200) — `data` object without keys

### Accountant / Pricing (2)

- `GET /api/accountant/pricing/pricing/sessions` (200) — `data.items` array without item type
- `GET /api/v1/pricing/sessions` (200) — `data.items` array without item type

### Accountant / Purchases (26)

- `GET /api/accountant/purchases/direct-purchases` (200) — `data` untyped
- `GET /api/accountant/purchases/purchase-orders` (200) — `data.low_stock[].open_order_number` untyped
- `GET /api/accountant/purchases/purchase-orders/{reference}` (200) — `data.invoices[].supplier_invoice_reference` untyped; `data.invoices[].invoice_number` untyped; `data.invoices[].supplier_reference` untyped; `data.invoices[].purchase_order_number` untyped; `data.invoices[].invoice_amount` untyped; `data.invoices[].uploaded_by_kind` untyped
- `POST /api/accountant/purchases/purchase-orders/{reference}/approve` (200) — `data.invoices[].supplier_invoice_reference` untyped; `data.invoices[].invoice_number` untyped; `data.invoices[].supplier_reference` untyped; `data.invoices[].purchase_order_number` untyped; `data.invoices[].invoice_amount` untyped; `data.invoices[].uploaded_by_kind` untyped
- `GET /api/accountant/purchases/purchase-orders/{reference}/supplier-invoice` (200) — `data.invoices[]` array without item type
- `GET /api/accountant/purchases/purchase-returns` (200) — `data.items` array without item type
- `POST /api/accountant/purchases/purchase-returns` (201) — `data.supplier_invoice_reference` untyped
- `POST /api/accountant/purchases/purchase-returns/{id}/approve` (200) — `data.supplier_invoice_reference` untyped
- `GET /api/accountant/purchases/purchase-returns/{purchaseReturn}` (200) — `data.supplier_invoice_reference` untyped
- `GET /api/accountant/purchases/supplier-invoices` (200) — `data.items` array without item type
- `GET /api/accountant/purchases/suppliers/payments` (200) — `data.links` object without keys
- `GET /api/accountant/purchases/suppliers/{id}` (200) — `data` object without keys
- `GET /api/v1/direct-purchases` (200) — `data.items[].invoice` untyped
- `GET /api/v1/direct-purchases/{reference}` (200) — `data.invoice` untyped
- `GET /api/v1/purchase-orders` (200) — `data.items[].lines[].received_qty` untyped
- `GET /api/v1/purchase-orders/{reference}` (200) — `data.lines[].received_qty` untyped
- `POST /api/v1/purchase-orders/{reference}/approve` (200) — `data.invoices[].supplier_invoice_reference` untyped; `data.invoices[].invoice_number` untyped; `data.invoices[].supplier_reference` untyped; `data.invoices[].purchase_order_number` untyped; `data.invoices[].invoice_amount` untyped; `data.invoices[].uploaded_by_kind` untyped
- `GET /api/v1/purchase-orders/{reference}/supplier-invoice` (200) — `data.invoices[]` array without item type
- `GET /api/v1/purchase-returns` (200) — `data.items` array without item type
- `POST /api/v1/purchase-returns` (201) — `data.supplier_invoice_reference` untyped
- `POST /api/v1/purchase-returns/{id}/approve` (200) — `data.supplier_invoice_reference` untyped
- `GET /api/v1/purchase-returns/{purchaseReturn}` (200) — `data.supplier_invoice_reference` untyped
- `GET /api/v1/supplier-invoices` (200) — `data.items` array without item type
- `GET /api/v1/suppliers` (200) — `data.suppliers[].phone` untyped; `data.suppliers[].whatsapp` untyped; `data.suppliers[].has_account` untyped; `data.suppliers[].purchase_orders_count` untyped; `data.suppliers[].invoices_count` untyped; `data.suppliers[].total_invoiced` untyped
- `GET /api/v1/suppliers/payments` (200) — `data.links` object without keys
- `GET /api/v1/suppliers/{id}` (200) — `data.phone` untyped; `data.whatsapp` untyped; `data.has_account` untyped; `data.purchase_orders_count` untyped; `data.invoices_count` untyped; `data.total_invoiced` untyped

### Accountant / Reports (18)

- `GET /api/accountant/reports/financial-analysis` (200) — `data.breakdown` array without item type; `data.meta.page` untyped; `data.meta.per_page` untyped
- `POST /api/accountant/reports/monthly-reports` (200) — `data.indicators[].comparison` object without keys; `data.indicators[].provenance` object without keys; `data.sections` object without keys
- `GET /api/accountant/reports/monthly-reports/{reportId}` (200) — `data.indicators[].comparison` object without keys; `data.indicators[].provenance` object without keys; `data.sections` object without keys; `data.view` object without keys
- `PUT /api/accountant/reports/monthly-reports/{reportId}/commentary` (200) — `data.indicators[].comparison` object without keys; `data.indicators[].provenance` object without keys; `data.sections` object without keys
- `GET /api/accountant/reports/monthly-reports/{reportId}/document` (200) — `data` object without keys
- `POST /api/accountant/reports/monthly-reports/{reportId}/ready` (200) — `data.indicators[].comparison` object without keys; `data.indicators[].provenance` object without keys; `data.sections` object without keys
- `POST /api/accountant/reports/monthly-reports/{reportId}/refresh-draft` (200) — `data.indicators[].comparison` object without keys; `data.indicators[].provenance` object without keys; `data.sections` object without keys
- `GET /api/accountant/reports/monthly-reports/{reportId}/review` (200) — `data.product_analysis.products` array without item type; `data.warnings_and_recommendations.accountant_warnings` array without item type; `data.warnings_and_recommendations.accountant_recommendations` array without item type; `data.accountant_commentary.notes` array without item type; `data.accountant_commentary.clarifications` array without item type; `data.accountant_commentary.analysis` array without item type
- `POST /api/accountant/reports/monthly-reports/{reportId}/revisions` (201) — `data.indicators[].comparison` object without keys; `data.indicators[].provenance` object without keys; `data.sections` object without keys
- `GET /api/v1/financial-analysis` (200) — `data.breakdown` array without item type; `data.meta.page` untyped; `data.meta.per_page` untyped
- `POST /api/v1/monthly-reports` (200) — `data.indicators[].comparison` object without keys; `data.indicators[].provenance` object without keys; `data.sections` object without keys
- `GET /api/v1/monthly-reports/{reportId}` (200) — `data.sections[].rows` array without item type; `data.sections[].bars` array without item type
- `PUT /api/v1/monthly-reports/{reportId}/commentary` (200) — `data.indicators[].comparison` object without keys; `data.indicators[].provenance` object without keys; `data.sections` object without keys
- `GET /api/v1/monthly-reports/{reportId}/document` (200) — `data` object without keys
- `POST /api/v1/monthly-reports/{reportId}/ready` (200) — `data.indicators[].comparison` object without keys; `data.indicators[].provenance` object without keys; `data.sections` object without keys
- `POST /api/v1/monthly-reports/{reportId}/refresh-draft` (200) — `data.indicators[].comparison` object without keys; `data.indicators[].provenance` object without keys; `data.sections` object without keys
- `GET /api/v1/monthly-reports/{reportId}/review` (200) — `data.product_analysis.products` array without item type; `data.warnings_and_recommendations.accountant_warnings` array without item type; `data.warnings_and_recommendations.accountant_recommendations` array without item type; `data.accountant_commentary.notes` array without item type; `data.accountant_commentary.clarifications` array without item type; `data.accountant_commentary.analysis` array without item type
- `POST /api/v1/monthly-reports/{reportId}/revisions` (201) — `data.indicators[].comparison` object without keys; `data.indicators[].provenance` object without keys; `data.sections` object without keys

### Accountant / Sales (26)

- `GET /api/accountant/sales/customers` (200) — `data` object without keys
- `GET /api/accountant/sales/customers/{id}` (200) — `data.financial_summary` array without item type; `data.invoices` array without item type
- `GET /api/accountant/sales/customers/{id}/financial-summary` (200) — `data.summary` array without item type
- `GET /api/accountant/sales/customers/{reference}/balance` (200) — `data.invoices` array without item type
- `GET /api/accountant/sales/notes` (200) — `data` object without keys
- `POST /api/accountant/sales/notes` (201) — `data` object without keys
- `GET /api/accountant/sales/notes/{id}` (200) — `data` object without keys
- `POST /api/accountant/sales/notes/{id}/cancel` (200) — `data` object without keys
- `POST /api/accountant/sales/notes/{id}/issue` (200) — `data` object without keys
- `GET /api/accountant/sales/sales-returns` (200) — `data.items` array without item type
- `POST /api/accountant/sales/sales-returns` (201) — `data` object without keys
- `GET /api/accountant/sales/sales-returns/{publicReference}` (200) — `data` object without keys
- `POST /api/accountant/sales/sales-returns/{publicReference}/approve` (200) — `data.lines` array without item type; `data.inventory_dispositions` array without item type
- `GET /api/v1/customers` (200) — `data` object without keys
- `GET /api/v1/customers/{id}` (200) — `data.financial_summary` array without item type; `data.invoices` array without item type
- `GET /api/v1/customers/{id}/financial-summary` (200) — `data.summary` array without item type
- `GET /api/v1/customers/{reference}/balance` (200) — `data.invoices` array without item type
- `GET /api/v1/sales-notes` (200) — `data` object without keys
- `POST /api/v1/sales-notes` (201) — `data` object without keys
- `GET /api/v1/sales-notes/{id}` (200) — `data` object without keys
- `POST /api/v1/sales-notes/{id}/cancel` (200) — `data` object without keys
- `POST /api/v1/sales-notes/{id}/issue` (200) — `data` object without keys
- `GET /api/v1/sales-returns` (200) — `data.items` array without item type
- `POST /api/v1/sales-returns` (201) — `data` object without keys
- `GET /api/v1/sales-returns/{publicReference}` (200) — `data` object without keys
- `POST /api/v1/sales-returns/{publicReference}/approve` (200) — `data.lines` array without item type; `data.inventory_dispositions` array without item type

### Accountant / Tax (23)

- `GET /api/accountant/tax/tax/documents/supplemental` (200) — `data.items[]` array without item type
- `GET /api/accountant/tax/tax/documents/supplemental/{document}` (200) — `data.missing_fields` array without item type
- `POST /api/accountant/tax/tax/documents/{document}/confirm` (200) — `data.missing_fields` array without item type
- `GET /api/accountant/tax/tax/periods` (200) — `data.items[]` array without item type
- `GET /api/accountant/tax/tax/periods/{period}` (200) — `data` array without item type
- `GET /api/accountant/tax/tax/periods/{period}/input-invoices` (200) — `data.meta.last_page` untyped
- `GET /api/accountant/tax/tax/periods/{period}/invoices` (200) — `data.meta.last_page` untyped
- `GET /api/accountant/tax/tax/vat-returns/invoices` (200) — `data.sales_invoices[].id` untyped; `data.sales_invoices[].status` untyped; `data.sales_invoices[].created_at` untyped; `data.purchase_invoices[].id` untyped; `data.purchase_invoices[].status` untyped; `data.purchase_invoices[].created_at` untyped
- `GET /api/accountant/tax/zakat/history` (200) — `data.items[].period_label` untyped
- `POST /api/accountant/tax/zakat/sessions` (201) — `data` object without keys
- `POST /api/accountant/tax/zakat/sessions/{uuid}/worksheet` (200) — `data.items` array without item type
- `GET /api/v1/tax/documents/supplemental` (200) — `data.items[]` array without item type
- `GET /api/v1/tax/documents/supplemental/{document}` (200) — `data.missing_fields` array without item type
- `POST /api/v1/tax/documents/{document}/confirm` (200) — `data.missing_fields` array without item type
- `GET /api/v1/tax/periods` (200) — `data.items[]` array without item type
- `GET /api/v1/tax/periods/{period}` (200) — `data` array without item type
- `GET /api/v1/tax/periods/{period}/input-invoices` (200) — `data.meta.last_page` untyped
- `GET /api/v1/tax/periods/{period}/invoices` (200) — `data.meta.last_page` untyped
- `GET /api/v1/tax/vat-returns/invoices` (200) — `data.sales_invoices[].id` untyped; `data.sales_invoices[].status` untyped; `data.sales_invoices[].created_at` untyped; `data.purchase_invoices[].id` untyped; `data.purchase_invoices[].status` untyped; `data.purchase_invoices[].created_at` untyped
- `GET /api/v1/zakat/history` (200) — `data.items[].period_label` untyped
- `POST /api/v1/zakat/sessions` (201) — `data` object without keys
- `GET /api/v1/zakat/sessions/{uuid}` (200) — `data.calculation.base[].manual_amount` untyped; `data.calculation.deductions[].manual_amount` untyped
- `POST /api/v1/zakat/sessions/{uuid}/worksheet` (200) — `data.items` array without item type

### Admin / Admin Roles (6)

- `PUT /api/admin/admin-roles/{roleReference}/permissions` (200) — `data` object without keys
- `POST /api/admin/admin-roles/{roleReference}/users` (200) — `data` object without keys
- `DELETE /api/admin/admin-roles/{roleReference}/users/{userReference}` (200) — `data` object without keys
- `PUT /api/v1/platform/admin-roles/{roleReference}/permissions` (200) — `data` object without keys
- `POST /api/v1/platform/admin-roles/{roleReference}/users` (200) — `data` object without keys
- `DELETE /api/v1/platform/admin-roles/{roleReference}/users/{userReference}` (200) — `data` object without keys

### Admin / Ai Usage (6)

- `GET /api/admin/ai-usage/operations` (200) — `data` object without keys
- `GET /api/admin/ai-usage/operations/{reference}` (200) — `data` object without keys
- `GET /api/admin/ai-usage/summary` (200) — `data` object without keys
- `GET /api/v1/platform/ai-usage/operations` (200) — `data` object without keys
- `GET /api/v1/platform/ai-usage/operations/{reference}` (200) — `data` object without keys
- `GET /api/v1/platform/ai-usage/summary` (200) — `data` object without keys

### Admin / Audit Log (6)

- `GET /api/admin/audit-log` (200) — `data` object without keys
- `GET /api/admin/audit-log/action-types` (200) — `data` object without keys
- `GET /api/admin/audit-log/{reference}` (200) — `data` object without keys
- `GET /api/v1/platform/audit-log` (200) — `data` object without keys
- `GET /api/v1/platform/audit-log/action-types` (200) — `data` object without keys
- `GET /api/v1/platform/audit-log/{reference}` (200) — `data` object without keys

### Admin / Clients (6)

- `GET /api/admin/clients/registration-requests` (200) — `data` object without keys
- `POST /api/admin/clients/registration-requests/{id}/payment/reject` (200) — `data.items` array without item type
- `POST /api/admin/clients/registration-requests/{id}/payment/verify` (200) — `data` array without item type
- `GET /api/v1/platform/clients/registration-requests` (200) — `data` object without keys
- `POST /api/v1/platform/clients/registration-requests/{id}/payment/reject` (200) — `data.items` array without item type
- `POST /api/v1/platform/clients/registration-requests/{id}/payment/verify` (200) — `data` array without item type

### Admin / Establishments (2)

- `GET /api/admin/establishments/{id}` (200) — `data.accountants.company` array without item type; `data.accountants.branches[].accountants` array without item type
- `GET /api/v1/platform/establishments/{id}` (200) — `data.accountants.company` array without item type; `data.accountants.branches[].accountants` array without item type

### Admin / Integrations (10)

- `GET /api/admin/integrations/{code}` (200) — `data` object without keys
- `POST /api/admin/integrations/{code}/activate` (200) — `data` object without keys
- `POST /api/admin/integrations/{code}/deactivate` (200) — `data` object without keys
- `GET /api/admin/integrations/{code}/issues` (200) — `data` object without keys
- `GET /api/admin/integrations/{code}/issues/{reference}` (200) — `data` object without keys
- `GET /api/v1/platform/integrations/{code}` (200) — `data` object without keys
- `POST /api/v1/platform/integrations/{code}/activate` (200) — `data` object without keys
- `POST /api/v1/platform/integrations/{code}/deactivate` (200) — `data` object without keys
- `GET /api/v1/platform/integrations/{code}/issues` (200) — `data` object without keys
- `GET /api/v1/platform/integrations/{code}/issues/{reference}` (200) — `data` object without keys

### Admin / Notifications (4)

- `GET /api/admin/notifications/{reference}` (200) — `data` object without keys
- `POST /api/admin/notifications/{reference}/read` (200) — `data` object without keys
- `GET /api/v1/platform/notifications/{reference}` (200) — `data` object without keys
- `POST /api/v1/platform/notifications/{reference}/read` (200) — `data` object without keys

### Admin / Packages (10)

- `GET /api/admin/packages` (200) — `data.items[].features` array without item type
- `POST /api/admin/packages` (201) — `data.features` array without item type
- `PUT /api/admin/packages/{uuid}` (200) — `data.features` array without item type
- `PATCH /api/admin/packages/{uuid}` (200) — `data.features` array without item type
- `POST /api/admin/packages/{uuid}/toggle-status` (200) — `data.features` array without item type
- `GET /api/v1/platform/packages` (200) — `data.items[].features` array without item type
- `POST /api/v1/platform/packages` (201) — `data.features` array without item type
- `PUT /api/v1/platform/packages/{uuid}` (200) — `data.features` array without item type
- `PATCH /api/v1/platform/packages/{uuid}` (200) — `data.features` array without item type
- `POST /api/v1/platform/packages/{uuid}/toggle-status` (200) — `data.features` array without item type

### Admin / Reports (14)

- `GET /api/admin/reports/accountant-assignments` (200) — `data.items[]` object without keys
- `GET /api/admin/reports/accountant-workload` (200) — `data.items[]` object without keys
- `GET /api/admin/reports/clients` (200) — `data.items[]` object without keys
- `GET /api/admin/reports/renewals` (200) — `data.items[]` object without keys
- `GET /api/admin/reports/subscriptions` (200) — `data.items[]` object without keys
- `GET /api/admin/reports/suppliers` (200) — `data.items[]` object without keys
- `GET /api/admin/reports/tasks` (200) — `data.items[]` object without keys
- `GET /api/v1/platform/reports/accountant-assignments` (200) — `data.items[]` object without keys
- `GET /api/v1/platform/reports/accountant-workload` (200) — `data.items[]` object without keys
- `GET /api/v1/platform/reports/clients` (200) — `data.items[]` object without keys
- `GET /api/v1/platform/reports/renewals` (200) — `data.items[]` object without keys
- `GET /api/v1/platform/reports/subscriptions` (200) — `data.items[]` object without keys
- `GET /api/v1/platform/reports/suppliers` (200) — `data.items[]` object without keys
- `GET /api/v1/platform/reports/tasks` (200) — `data.items[]` object without keys

### Admin / Subscriptions (12)

- `POST /api/admin/subscriptions/payments/{reference}/reject` (200) — `data.vat_treatment` untyped; `data.evidence_reference` untyped
- `POST /api/admin/subscriptions/payments/{reference}/verify` (200) — `data.items` array without item type
- `GET /api/admin/subscriptions/status` (200) — `data.current_package.features` array without item type; `data.pending_next_package.features` array without item type
- `GET /api/admin/subscriptions/{userId}` (200) — `data.subscription` object without keys
- `POST /api/admin/subscriptions/{userId}/payments` (201) — `data.vat_treatment` untyped; `data.evidence_reference` untyped
- `POST /api/admin/subscriptions/{userId}/renew` (200) — `data` object without keys
- `POST /api/v1/platform/subscriptions/payments/{reference}/reject` (200) — `data.vat_treatment` untyped; `data.evidence_reference` untyped
- `POST /api/v1/platform/subscriptions/payments/{reference}/verify` (200) — `data.items` array without item type
- `GET /api/v1/platform/subscriptions/status` (200) — `data.current_package.features` array without item type; `data.pending_next_package.features` array without item type
- `GET /api/v1/platform/subscriptions/{userId}` (200) — `data.subscription` object without keys
- `POST /api/v1/platform/subscriptions/{userId}/payments` (201) — `data.vat_treatment` untyped; `data.evidence_reference` untyped
- `POST /api/v1/platform/subscriptions/{userId}/renew` (200) — `data` object without keys

### Auth (34)

- `GET /api/auth/account` (200) — `data.name` untyped; `data.email` untyped; `data.mobile` untyped; `data.status` untyped; `data.subscription.usage` array without item type
- `POST /api/auth/account/profile` (200) — `data.name` untyped; `data.email` untyped; `data.mobile` untyped
- `POST /api/auth/account/profile/verify-mobile` (200) — `data.name` untyped; `data.email` untyped; `data.mobile` untyped; `data.status` untyped
- `GET /api/auth/accountant/meeting-slots` (200) — `data.items[].organization_reference` untyped; `data.items[].organization_name` untyped
- `POST /api/auth/accountant/meeting-slots` (201) — `data.organization_reference` untyped; `data.organization_name` untyped
- `PUT /api/auth/accountant/meeting-slots/{slotReference}` (200) — `data.organization_reference` untyped; `data.organization_name` untyped
- `GET /api/auth/accountant/meetings` (200) — `data.items[].organization_reference` untyped; `data.items[].organization_name` untyped
- `GET /api/auth/accountant/meetings/organizations` (200) — `data.items[].organization_reference` untyped; `data.items[].organization_name` untyped
- `GET /api/auth/accountant/meetings/owner-booked` (200) — `data.items[].organization_reference` untyped; `data.items[].organization_name` untyped
- `GET /api/auth/accountant/meetings/{meetingReference}` (200) — `data.organization_reference` untyped; `data.organization_name` untyped
- `PUT /api/auth/accountant/meetings/{meetingReference}` (200) — `data.organization_reference` untyped; `data.organization_name` untyped; `data.organization_reference` untyped; `data.organization_name` untyped
- `POST /api/auth/accountant/meetings/{meetingReference}/cancel` (200) — `data.organization_reference` untyped; `data.organization_name` untyped; `data.organization_reference` untyped; `data.organization_name` untyped
- `GET /api/auth/accounting/financial-statements/{statement}/pdf` (200) — `data` object without keys
- `GET /api/auth/bootstrap` (200) — `data.detail.tenant_admin_permissions` array without item type; `data.detail.caps` array without item type; `data.detail.caps` array without item type; `data.platform.permissions` array without item type
- `POST /api/auth/onboarding/applications` (201) — `data.items` array without item type
- `POST /api/auth/onboarding/applications/verify` (200) — `data` array without item type
- `POST /api/auth/subscriptions/registration/resubmit` (200) — `data` object without keys
- `GET /api/v1/account` (200) — `data.name` untyped; `data.email` untyped; `data.mobile` untyped; `data.status` untyped; `data.subscription.usage` array without item type
- `POST /api/v1/account/profile` (200) — `data.name` untyped; `data.email` untyped; `data.mobile` untyped
- `POST /api/v1/account/profile/verify-mobile` (200) — `data.name` untyped; `data.email` untyped; `data.mobile` untyped; `data.status` untyped
- `GET /api/v1/accountant/meeting-slots` (200) — `data.items[].organization_reference` untyped; `data.items[].organization_name` untyped
- `POST /api/v1/accountant/meeting-slots` (201) — `data.organization_reference` untyped; `data.organization_name` untyped
- `PUT /api/v1/accountant/meeting-slots/{slotReference}` (200) — `data.organization_reference` untyped; `data.organization_name` untyped
- `GET /api/v1/accountant/meetings` (200) — `data.items[].organization_reference` untyped; `data.items[].organization_name` untyped
- `GET /api/v1/accountant/meetings/organizations` (200) — `data.items[].organization_reference` untyped; `data.items[].organization_name` untyped
- `GET /api/v1/accountant/meetings/owner-booked` (200) — `data.items[].organization_reference` untyped; `data.items[].organization_name` untyped
- `GET /api/v1/accountant/meetings/{meetingReference}` (200) — `data.organization_reference` untyped; `data.organization_name` untyped
- `PUT /api/v1/accountant/meetings/{meetingReference}` (200) — `data.organization_reference` untyped; `data.organization_name` untyped; `data.organization_reference` untyped; `data.organization_name` untyped
- `POST /api/v1/accountant/meetings/{meetingReference}/cancel` (200) — `data.organization_reference` untyped; `data.organization_name` untyped; `data.organization_reference` untyped; `data.organization_name` untyped
- `GET /api/v1/accounting/financial-statements/{statement}/pdf` (200) — `data` object without keys
- `GET /api/v1/bootstrap` (200) — `data.detail.tenant_admin_permissions` array without item type; `data.detail.caps` array without item type; `data.detail.caps` array without item type; `data.platform.permissions` array without item type
- `POST /api/v1/onboarding/applications` (201) — `data.items` array without item type
- `POST /api/v1/onboarding/applications/verify` (200) — `data` array without item type
- `POST /api/v1/subscriptions/registration/resubmit` (200) — `data` object without keys

### Owner / Accounting (10)

- `GET /api/owner/accounting/assets` (200) — `data.assets[].notes` untyped
- `GET /api/owner/accounting/assets/{asset}` (200) — `data.notes` untyped
- `GET /api/owner/accounting/journal-entries` (200) — `data.items` array without item type
- `GET /api/owner/accounting/posting-mappings` (200) — `data.items[].assigned_by` untyped; `data.items[].ended_by` untyped; `data.items[].end_reason` untyped
- `GET /api/owner/accounting/posting-requests` (200) — `data` object without keys
- `GET /api/owner/accounting/posting-requests/{reference}` (200) — `data.lines` untyped; `data.corrected_by` untyped; `data.correction_reason` untyped
- `GET /api/owner/accounting/posting-roles` (200) — `data.items` array without item type
- `GET /api/owner/accounting/posting-templates` (200) — `data.items[].roles` array without item type
- `GET /api/v1/assets` (200) — `data.assets[].notes` untyped
- `GET /api/v1/assets/{asset}` (200) — `data.notes` untyped

### Owner / Dashboard (2)

- `GET /api/owner/dashboard/owner` (200) — `data.business_name` untyped; `data.profit_change` untyped; `data.items_count` untyped; `data.low_stock_count` untyped; `data.due_supplier_invoices` untyped; `data.recent_moves[].vat` untyped
- `GET /api/v1/dashboards/owner` (200) — `data.business_name` untyped; `data.profit_change` untyped; `data.items_count` untyped; `data.low_stock_count` untyped; `data.due_supplier_invoices` untyped; `data.recent_moves[].vat` untyped

### Owner / Expenses (8)

- `GET /api/owner/expenses/expenses/documents/{document}` (200) — `data.reviewed_fields` object without keys
- `PUT /api/owner/expenses/expenses/documents/{document}` (200) — `data.reviewed_fields` array without item type
- `GET /api/owner/expenses/expenses/{document}/extraction` (200) — `data.fields` array without item type
- `GET /api/owner/expenses/expenses/{expense_reference}/duplicate-candidates` (200) — `data.candidates` array without item type
- `POST /api/owner/expenses/expenses/{reference}/resubmit` (200) — `data` array without item type
- `GET /api/v1/expenses/documents/{document}` (200) — `data.reviewed_fields` object without keys
- `GET /api/v1/expenses/{document}/extraction` (200) — `data.fields` array without item type
- `POST /api/v1/expenses/{reference}/resubmit` (200) — `data` array without item type

### Owner / Forms (4)

- `GET /api/owner/forms/form-options/expenses` (200) — `data.categories` array without item type; `data.payment_methods` array without item type; `data.branches` array without item type
- `GET /api/owner/forms/form-options/inventory` (200) — `data.units` array without item type; `data.vat_rates` array without item type; `data.suppliers` array without item type; `data.branches` array without item type
- `GET /api/v1/form-options/expenses` (200) — `data.categories` array without item type; `data.payment_methods` array without item type; `data.branches` array without item type
- `GET /api/v1/form-options/inventory` (200) — `data.units` array without item type; `data.vat_rates` array without item type; `data.suppliers` array without item type; `data.branches` array without item type

### Owner / General (18)

- `GET /api/owner/general/account/subscription` (200) — `data.subscription` object without keys; `data.payments[]` object without keys
- `GET /api/owner/general/account/subscription/history` (200) — `data.items[]` object without keys
- `POST /api/owner/general/account/subscription/renew` (200) — `data` object without keys; `data.payment.plan_change` object without keys; `data.scheduled_change` object without keys
- `GET /api/owner/general/admin/roles` (200) — `data.items[].associated_users[]` object without keys
- `GET /api/owner/general/admin/roles/{roleReference}` (200) — `data.associated_users[]` object without keys
- `GET /api/owner/general/packages` (200) — `data.plans[].tag` untyped; `data.plans[].modules` untyped; `data.plans[].limits` untyped
- `GET /api/owner/general/packages/read-models` (200) — `data.available_features[]` object without keys; `data.usage_limits[]` object without keys; `data.available_modules[]` object without keys; `data.package_entitlements[]` object without keys
- `GET /api/owner/general/subscriptions` (200) — `data.remaining_days` untyped; `data.available_features` array without item type; `data.entitlement.company_reference` untyped; `data.available_packages[].features` array without item type
- `POST /api/owner/general/subscriptions/change-plan` (200) — `data.payment.plan_change` object without keys
- `GET /api/v1/account/subscription` (200) — `data.subscription` object without keys; `data.payments[]` object without keys
- `GET /api/v1/account/subscription/history` (200) — `data.items[]` object without keys
- `POST /api/v1/account/subscription/renew` (200) — `data` object without keys; `data.payment.plan_change` object without keys; `data.scheduled_change` object without keys
- `GET /api/v1/admin/roles` (200) — `data.items[].associated_users[]` object without keys
- `GET /api/v1/admin/roles/{roleReference}` (200) — `data.associated_users[]` object without keys
- `GET /api/v1/erp/packages/read-models` (200) — `data.available_features[]` object without keys; `data.usage_limits[]` object without keys; `data.available_modules[]` object without keys; `data.package_entitlements[]` object without keys
- `GET /api/v1/packages` (200) — `data.plans[].tag` untyped; `data.plans[].modules` untyped; `data.plans[].limits` untyped
- `GET /api/v1/subscriptions` (200) — `data.remaining_days` untyped; `data.available_features` array without item type; `data.entitlement.company_reference` untyped; `data.available_packages[].features` array without item type
- `POST /api/v1/subscriptions/change-plan` (200) — `data.payment.plan_change` object without keys

### Owner / Integrations (6)

- `GET /api/owner/integrations/integrations/purchase-orders/{purchaseOrderReference}/delivery` (200) — `data` object without keys
- `GET /api/owner/integrations/integrations/sync-runs` (200) — `data.items[]` object without keys
- `POST /api/owner/integrations/integrations/sync-runs` (201) — `data` object without keys
- `GET /api/owner/integrations/integrations/sync-runs/{syncRun}` (200) — `data` object without keys
- `PUT /api/owner/integrations/integrations/sync-runs/{syncRun}` (200) — `data` object without keys
- `PATCH /api/owner/integrations/integrations/sync-runs/{syncRun}` (200) — `data` object without keys

### Owner / Inventory (9)

- `GET /api/owner/inventory/catalog-products` (200) — `data.summary.categories_count` untyped; `data.summary.sub_categories_count` untyped; `data.categories` untyped
- `POST /api/owner/inventory/catalog-products` (201) — `data` array without item type
- `GET /api/owner/inventory/catalog-products/{catalogProduct}` (200) — `data.recipe` untyped
- `PUT /api/owner/inventory/catalog-products/{catalogProduct}` (200) — `data` array without item type
- `GET /api/owner/inventory/catalog/products/{productReference}/recipe-components` (200) — `data.id` untyped; `data.name` untyped; `data.category` untyped; `data.sub_category` untyped
- `GET /api/owner/inventory/inventory/items` (200) — `data.summary` object without keys; `data.categories` array without item type; `data.items[]` object without keys
- `POST /api/v1/catalog-products` (201) — `data` array without item type
- `PUT /api/v1/catalog-products/{catalogProduct}` (200) — `data` array without item type
- `GET /api/v1/catalog/products/{productReference}/recipe-components` (200) — `data.id` untyped; `data.name` untyped; `data.category` untyped; `data.sub_category` untyped

### Owner / Meetings (4)

- `GET /api/owner/meetings/meetings` (200) — `data.items[].subject` untyped; `data.items[].notes` untyped; `data.items[].created_at` untyped
- `GET /api/owner/meetings/meetings/availability` (200) — `data.accountant` untyped
- `GET /api/v1/meetings` (200) — `data.items[].subject` untyped; `data.items[].notes` untyped; `data.items[].created_at` untyped
- `GET /api/v1/meetings/availability` (200) — `data.accountant` untyped

### Owner / Notifications (2)

- `GET /api/owner/notifications/notifications` (200) — `data.notifications[].branch_name` untyped; `data.notifications[].business_name` untyped
- `GET /api/owner/notifications/notifications/{uuid}` (200) — `data.branch_name` untyped; `data.business_name` untyped

### Owner / Payroll (22)

- `POST /api/owner/payroll/payroll-runs/{runId}/prepare-payment` (200) — `data` object without keys
- `GET /api/owner/payroll/payroll/employees` (200) — `data.employees[].title` untyped; `data.employees[].branch_id` untyped; `data.employees[].branch` untyped; `data.employees[].iban` untyped; `data.employees[].bank_holder` untyped; `data.employees[].next_salary` untyped
- `POST /api/owner/payroll/payroll/employees` (200) — `data` object without keys
- `GET /api/owner/payroll/payroll/employees/{publicReference}` (200) — `data.title` untyped; `data.branch_id` untyped; `data.branch` untyped; `data.iban` untyped; `data.bank_holder` untyped; `data.next_salary` untyped
- `PATCH /api/owner/payroll/payroll/employees/{publicReference}` (200) — `data` object without keys
- `POST /api/owner/payroll/payroll/employees/{publicReference}/action` (200) — `data` object without keys
- `GET /api/owner/payroll/payroll/runs` (200) — `data.runs[].paid_at` untyped
- `GET /api/owner/payroll/payroll/runs/{id}` (200) — `data` object without keys
- `POST /api/owner/payroll/payroll/runs/{runId}/approve` (200) — `data` object without keys
- `PATCH /api/owner/payroll/payroll/runs/{runId}/lines/{lineId}` (200) — `data` object without keys
- `POST /api/owner/payroll/payroll/runs/{runId}/overtime-rate` (200) — `data` object without keys
- `POST /api/owner/payroll/payroll/runs/{runId}/return-to-draft` (200) — `data` object without keys
- `POST /api/owner/payroll/payroll/runs/{runId}/review` (200) — `data` object without keys
- `GET /api/v1/payroll/employees` (200) — `data.employees[].title` untyped; `data.employees[].branch_id` untyped; `data.employees[].branch` untyped; `data.employees[].iban` untyped; `data.employees[].bank_holder` untyped; `data.employees[].next_salary` untyped
- `POST /api/v1/payroll/employees` (200) — `data` object without keys
- `GET /api/v1/payroll/employees/{publicReference}` (200) — `data.title` untyped; `data.branch_id` untyped; `data.branch` untyped; `data.iban` untyped; `data.bank_holder` untyped; `data.next_salary` untyped
- `PATCH /api/v1/payroll/employees/{publicReference}` (200) — `data` object without keys
- `POST /api/v1/payroll/employees/{publicReference}/action` (200) — `data` object without keys
- `GET /api/v1/payroll/runs` (200) — `data.runs[].paid_at` untyped
- `GET /api/v1/payroll/runs/{id}` (200) — `data` object without keys
- `PATCH /api/v1/payroll/runs/{runId}/lines/{lineId}` (200) — `data` object without keys
- `POST /api/v1/payroll/runs/{runId}/overtime-rate` (200) — `data` object without keys

### Owner / Pricing (1)

- `GET /api/owner/pricing/pricing/sessions` (200) — `data.items` array without item type

### Owner / Purchases (32)

- `GET /api/owner/purchases/direct-purchases` (200) — `data.items[].invoice` untyped
- `POST /api/owner/purchases/direct-purchases` (201) — `data.lines[]` object without keys; `data.invoices[]` object without keys
- `GET /api/owner/purchases/direct-purchases/{reference}` (200) — `data.invoice` untyped
- `POST /api/owner/purchases/direct-purchases/{reference}/complete` (200) — `data.lines[]` object without keys; `data.invoices[]` object without keys
- `GET /api/owner/purchases/purchase-orders` (200) — `data.items[].lines[].received_qty` untyped
- `GET /api/owner/purchases/purchase-orders/{reference}` (200) — `data.lines[].received_qty` untyped
- `PATCH /api/owner/purchases/purchase-orders/{reference}` (200) — `data.invoices[].supplier_invoice_reference` untyped; `data.invoices[].invoice_number` untyped; `data.invoices[].supplier_reference` untyped; `data.invoices[].purchase_order_number` untyped; `data.invoices[].invoice_amount` untyped; `data.invoices[].uploaded_by_kind` untyped
- `POST /api/owner/purchases/purchase-orders/{reference}/cancel` (200) — `data.invoices[].supplier_invoice_reference` untyped; `data.invoices[].invoice_number` untyped; `data.invoices[].supplier_reference` untyped; `data.invoices[].purchase_order_number` untyped; `data.invoices[].invoice_amount` untyped; `data.invoices[].uploaded_by_kind` untyped
- `PATCH /api/owner/purchases/purchase-orders/{reference}/delivery` (200) — `data.invoices[].supplier_invoice_reference` untyped; `data.invoices[].invoice_number` untyped; `data.invoices[].supplier_reference` untyped; `data.invoices[].purchase_order_number` untyped; `data.invoices[].invoice_amount` untyped; `data.invoices[].uploaded_by_kind` untyped
- `POST /api/owner/purchases/purchase-orders/{reference}/send` (202) — `data.invoices[].supplier_invoice_reference` untyped; `data.invoices[].invoice_number` untyped; `data.invoices[].supplier_reference` untyped; `data.invoices[].purchase_order_number` untyped; `data.invoices[].invoice_amount` untyped; `data.invoices[].uploaded_by_kind` untyped
- `GET /api/owner/purchases/purchase-orders/{reference}/supplier-invoice` (200) — `data.invoices[]` array without item type
- `GET /api/owner/purchases/purchase-returns` (200) — `data.items` array without item type
- `POST /api/owner/purchases/purchase-returns` (201) — `data.supplier_invoice_reference` untyped
- `GET /api/owner/purchases/purchase-returns/{purchaseReturn}` (200) — `data.supplier_invoice_reference` untyped
- `GET /api/owner/purchases/supplier-invoices` (200) — `data.items` array without item type
- `GET /api/owner/purchases/suppliers` (200) — `data.suppliers[].phone` untyped; `data.suppliers[].whatsapp` untyped; `data.suppliers[].has_account` untyped; `data.suppliers[].purchase_orders_count` untyped; `data.suppliers[].invoices_count` untyped; `data.suppliers[].total_invoiced` untyped
- `POST /api/owner/purchases/suppliers/payment-scan` (200) — `data` object without keys
- `GET /api/owner/purchases/suppliers/payments` (200) — `data.links` object without keys
- `GET /api/owner/purchases/suppliers/{id}` (200) — `data.phone` untyped; `data.whatsapp` untyped; `data.has_account` untyped; `data.purchase_orders_count` untyped; `data.invoices_count` untyped; `data.total_invoiced` untyped
- `PUT /api/owner/purchases/suppliers/{id}` (200) — `data.supplied_items` array without item type
- `POST /api/owner/purchases/suppliers/{id}/convert-to-permanent` (200) — `data.supplied_items` array without item type
- `POST /api/owner/purchases/suppliers/{id}/status` (200) — `data.supplied_items` array without item type
- `POST /api/v1/direct-purchases` (201) — `data.lines[]` object without keys; `data.invoices[]` object without keys
- `POST /api/v1/direct-purchases/{reference}/complete` (200) — `data.lines[]` object without keys; `data.invoices[]` object without keys
- `PATCH /api/v1/purchase-orders/{reference}` (200) — `data.invoices[].supplier_invoice_reference` untyped; `data.invoices[].invoice_number` untyped; `data.invoices[].supplier_reference` untyped; `data.invoices[].purchase_order_number` untyped; `data.invoices[].invoice_amount` untyped; `data.invoices[].uploaded_by_kind` untyped
- `POST /api/v1/purchase-orders/{reference}/cancel` (200) — `data.invoices[].supplier_invoice_reference` untyped; `data.invoices[].invoice_number` untyped; `data.invoices[].supplier_reference` untyped; `data.invoices[].purchase_order_number` untyped; `data.invoices[].invoice_amount` untyped; `data.invoices[].uploaded_by_kind` untyped
- `PATCH /api/v1/purchase-orders/{reference}/delivery` (200) — `data.invoices[].supplier_invoice_reference` untyped; `data.invoices[].invoice_number` untyped; `data.invoices[].supplier_reference` untyped; `data.invoices[].purchase_order_number` untyped; `data.invoices[].invoice_amount` untyped; `data.invoices[].uploaded_by_kind` untyped
- `POST /api/v1/purchase-orders/{reference}/send` (202) — `data.invoices[].supplier_invoice_reference` untyped; `data.invoices[].invoice_number` untyped; `data.invoices[].supplier_reference` untyped; `data.invoices[].purchase_order_number` untyped; `data.invoices[].invoice_amount` untyped; `data.invoices[].uploaded_by_kind` untyped
- `POST /api/v1/suppliers/payment-scan` (200) — `data` object without keys
- `PUT /api/v1/suppliers/{id}` (200) — `data.supplied_items` array without item type
- `POST /api/v1/suppliers/{id}/convert-to-permanent` (200) — `data.supplied_items` array without item type
- `POST /api/v1/suppliers/{id}/status` (200) — `data.supplied_items` array without item type

### Owner / Reports (8)

- `GET /api/owner/reports/financial-analysis` (200) — `data.breakdown` array without item type; `data.meta.page` untyped; `data.meta.per_page` untyped
- `GET /api/owner/reports/monthly-reports` (200) — `data.items` array without item type
- `GET /api/owner/reports/monthly-reports/{reportId}` (200) — `data.sections[].rows` array without item type; `data.sections[].bars` array without item type
- `POST /api/owner/reports/monthly-reports/{reportId}/customize` (200) — `data` object without keys
- `GET /api/owner/reports/monthly-reports/{reportId}/document` (200) — `data` object without keys
- `GET /api/owner/reports/monthly-reports/{reportId}/review` (200) — `data.product_analysis.products` array without item type; `data.warnings_and_recommendations.accountant_warnings` array without item type; `data.warnings_and_recommendations.accountant_recommendations` array without item type; `data.accountant_commentary.notes` array without item type; `data.accountant_commentary.clarifications` array without item type; `data.accountant_commentary.analysis` array without item type
- `GET /api/v1/monthly-reports` (200) — `data.items` array without item type
- `POST /api/v1/monthly-reports/{reportId}/customize` (200) — `data` object without keys

### Owner / Sales (34)

- `GET /api/owner/sales/customers` (200) — `data` object without keys
- `GET /api/owner/sales/customers/{id}` (200) — `data.financial_summary` array without item type; `data.invoices` array without item type
- `DELETE /api/owner/sales/customers/{id}` (200) — `data` object without keys
- `GET /api/owner/sales/customers/{id}/financial-summary` (200) — `data.summary` array without item type
- `GET /api/owner/sales/customers/{reference}/balance` (200) — `data.invoices` array without item type
- `GET /api/owner/sales/invoices` (200) — `data` object without keys
- `POST /api/owner/sales/invoices` (201) — `data` object without keys
- `GET /api/owner/sales/invoices/collection-methods` (200) — `data` object without keys
- `POST /api/owner/sales/invoices/collection-scan` (200) — `data` object without keys
- `GET /api/owner/sales/invoices/form-options` (200) — `data.products[]` object without keys
- `GET /api/owner/sales/invoices/{id}` (200) — `data` object without keys
- `GET /api/owner/sales/notes` (200) — `data` object without keys
- `POST /api/owner/sales/notes` (201) — `data` object without keys
- `GET /api/owner/sales/notes/{id}` (200) — `data` object without keys
- `POST /api/owner/sales/notes/{id}/cancel` (200) — `data` object without keys
- `POST /api/owner/sales/notes/{id}/issue` (200) — `data` object without keys
- `GET /api/owner/sales/quotes` (200) — `data` object without keys
- `POST /api/owner/sales/quotes` (201) — `data` object without keys
- `GET /api/owner/sales/quotes/{reference}` (200) — `data` object without keys
- `POST /api/owner/sales/quotes/{reference}/convert` (200) — `data` object without keys
- `GET /api/owner/sales/sales-returns` (200) — `data.items` array without item type
- `POST /api/owner/sales/sales-returns` (201) — `data` object without keys
- `GET /api/owner/sales/sales-returns/{publicReference}` (200) — `data` object without keys
- `DELETE /api/v1/customers/{id}` (200) — `data` object without keys
- `GET /api/v1/invoices` (200) — `data` object without keys
- `POST /api/v1/invoices` (201) — `data` object without keys
- `GET /api/v1/invoices/collection-methods` (200) — `data` object without keys
- `POST /api/v1/invoices/collection-scan` (200) — `data` object without keys
- `GET /api/v1/invoices/form-options` (200) — `data.products[]` object without keys
- `GET /api/v1/invoices/{id}` (200) — `data` object without keys
- `GET /api/v1/quotes` (200) — `data` object without keys
- `POST /api/v1/quotes` (201) — `data` object without keys
- `GET /api/v1/quotes/{reference}` (200) — `data` object without keys
- `POST /api/v1/quotes/{reference}/convert` (200) — `data` object without keys

### Owner / Settings (24)

- `GET /api/owner/settings/branches/{reference}` (200) — `data.items` array without item type
- `DELETE /api/owner/settings/branches/{reference}` (200) — `data` object without keys
- `POST /api/owner/settings/branches/{reference}/activate` (200) — `data.items` array without item type
- `POST /api/owner/settings/branches/{reference}/disable` (200) — `data.items` array without item type
- `POST /api/owner/settings/branches/{reference}/main` (200) — `data.items` array without item type
- `POST /api/owner/settings/branches/{reference}/status` (200) — `data.items` array without item type
- `GET /api/owner/settings/identity/memberships/{membershipId}/companies/{companyId}/branches` (200) — `data.allowed_branches` object without keys; `data.allowed_branches` array without item type
- `GET /api/owner/settings/identity/roles` (200) — `data.roles[].description` untyped; `data.roles[].denied` untyped; `data.roles[].users_count` untyped
- `GET /api/owner/settings/identity/users/{userReference}` (200) — `data.items` array without item type
- `GET /api/owner/settings/organizations/current` (200) — `data.integrations` array without item type
- `GET /api/owner/settings/users` (200) — `data.users[].branches` array without item type
- `POST /api/owner/settings/users` (201) — `data` array without item type
- `GET /api/v1/branches/{reference}` (200) — `data.items` array without item type
- `DELETE /api/v1/branches/{reference}` (200) — `data` object without keys
- `POST /api/v1/branches/{reference}/activate` (200) — `data.items` array without item type
- `POST /api/v1/branches/{reference}/disable` (200) — `data.items` array without item type
- `POST /api/v1/branches/{reference}/main` (200) — `data.items` array without item type
- `POST /api/v1/branches/{reference}/status` (200) — `data.items` array without item type
- `GET /api/v1/identity/memberships/{membershipId}/companies/{companyId}/branches` (200) — `data.allowed_branches` object without keys; `data.allowed_branches` array without item type
- `GET /api/v1/identity/roles` (200) — `data.roles[].description` untyped; `data.roles[].denied` untyped; `data.roles[].users_count` untyped
- `GET /api/v1/identity/users/{userReference}` (200) — `data.items` array without item type
- `GET /api/v1/organizations/current` (200) — `data.integrations` array without item type
- `GET /api/v1/users` (200) — `data.users[].branches` array without item type
- `POST /api/v1/users` (201) — `data` array without item type

### Owner / Tax (13)

- `GET /api/owner/tax/tax/documents/supplemental` (200) — `data.items[]` array without item type
- `GET /api/owner/tax/tax/documents/supplemental/{document}` (200) — `data.missing_fields` array without item type
- `POST /api/owner/tax/tax/documents/upload` (200) — `data.extracted_data` object without keys
- `POST /api/owner/tax/tax/documents/{document}/confirm` (200) — `data.missing_fields` array without item type
- `GET /api/owner/tax/tax/periods` (200) — `data.items[]` array without item type
- `GET /api/owner/tax/tax/periods/{period}` (200) — `data` array without item type
- `GET /api/owner/tax/tax/periods/{period}/input-invoices` (200) — `data.meta.last_page` untyped
- `GET /api/owner/tax/tax/periods/{period}/invoices` (200) — `data.meta.last_page` untyped
- `GET /api/owner/tax/tax/vat-returns/invoices` (200) — `data.sales_invoices[].id` untyped; `data.sales_invoices[].status` untyped; `data.sales_invoices[].created_at` untyped; `data.purchase_invoices[].id` untyped; `data.purchase_invoices[].status` untyped; `data.purchase_invoices[].created_at` untyped
- `GET /api/owner/tax/zakat/history` (200) — `data.items[].period_label` untyped
- `POST /api/owner/tax/zakat/sessions` (201) — `data` object without keys
- `GET /api/owner/tax/zakat/sessions/{uuid}` (200) — `data.calculation.base[].manual_amount` untyped; `data.calculation.deductions[].manual_amount` untyped
- `POST /api/v1/tax/documents/upload` (200) — `data.extracted_data` object without keys

### Public (14)

- `GET /api/public/general/cities` (200) — `data` object without keys
- `GET /api/public/general/countries` (200) — `data` object without keys
- `GET /api/public/legal/privacy` (200) — `data.sections` array without item type
- `GET /api/public/legal/terms` (200) — `data.sections` array without item type
- `GET /api/public/pages` (200) — `data` object without keys
- `GET /api/public/pages/{key}` (200) — `data` object without keys
- `GET /api/public/supplier-portal/purchase-order-links/{token}` (200) — `data.invoices[]` array without item type
- `GET /api/v1/content/legal/privacy` (200) — `data.sections` array without item type
- `GET /api/v1/content/legal/terms` (200) — `data.sections` array without item type
- `GET /api/v1/general/cities` (200) — `data` object without keys
- `GET /api/v1/general/countries` (200) — `data` object without keys
- `GET /api/v1/pages` (200) — `data` object without keys
- `GET /api/v1/pages/{key}` (200) — `data` object without keys
- `GET /api/v1/supplier-portal/purchase-order-links/{token}` (200) — `data.invoices[]` array without item type

