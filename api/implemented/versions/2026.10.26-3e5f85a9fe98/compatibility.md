# OpenAPI Contract Compatibility Report

- Baseline: `published 2026.10.25-7530c9a3319d` (1264 operations)
- Candidate: `build 952732c413d5` (1286 operations)
- Generated: 2026-10-26T09:11:20.443530+00:00

## Summary

| Category | Count |
|---|---|
| BREAKING | 455 |
| UNKNOWN | 35 |
| NON_BREAKING | 848 |
| DOCUMENTATION_ONLY | 222 |
| **total** | **1560** |

## Breaking changes (455)

| Kind | Location | Detail |
|---|---|---|
| `response_schema_type_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0]` | type removed (['object'] -> any) |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.account_reference` | field [account_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.accountant_notes` | field [accountant_notes] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.amount_before_tax` | field [amount_before_tax] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.branch_id` | field [branch_id] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.description` | field [description] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.document_url` | field [document_url] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.due_date` | field [due_date] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.expense_category` | field [expense_category] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.extracted_data` | field [extracted_data] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.invoice_date` | field [invoice_date] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.invoice_number` | field [invoice_number] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.modification_history` | field [modification_history] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.operation_type` | field [operation_type] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.original_document_path` | field [original_document_path] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.paid_amount` | field [paid_amount] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.payment_method` | field [payment_method] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.payment_status` | field [payment_status] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.po_number` | field [po_number] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.public_reference` | field [public_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.purchase_order_reference` | field [purchase_order_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.remaining_amount` | field [remaining_amount] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.review_status` | field [review_status] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.source` | field [source] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.supplier_reference` | field [supplier_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.suspicion_reason` | field [suspicion_reason] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.total_amount` | field [total_amount] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.uploaded_by_reference` | field [uploaded_by_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.vat_amount` | field [vat_amount] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.vendor_name` | field [vendor_name] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.version` | field [version] removed |
| `response_schema_field_removed` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.available_count` | field [available_count] removed |
| `response_schema_field_removed` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.available_value` | field [available_value] removed |
| `response_schema_field_removed` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.branch_label` | field [branch_label] removed |
| `response_schema_field_removed` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.integrations` | field [integrations] removed |
| `response_schema_field_removed` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.items_count` | field [items_count] removed |
| `response_schema_field_removed` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.low_count` | field [low_count] removed |
| `response_schema_field_removed` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.out_count` | field [out_count] removed |
| `response_schema_field_removed` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.total_value` | field [total_value] removed |
| `response_schema_field_removed` | `paths./api/accountant/inventory/inventory/items/{item}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | field [items] removed |
| `response_schema_type_changed` | `paths./api/accountant/reports/statements/export-bundle.post.responses.200.content.application/json.schema.allOf[1].properties.data` | type changed (['string'] -> ['object']) |
| `response_schema_type_removed` | `paths./api/accountant/reports/statements/export-bundle/{bundleId}.get.responses.200.content.application/json.schema` | type removed (['object'] -> any) |
| `response_schema_field_removed` | `paths./api/accountant/reports/statements/export-bundle/{bundleId}.get.responses.200.content.application/json.schema.properties.data` | field [data] removed |
| `response_schema_field_removed` | `paths./api/accountant/reports/statements/export-bundle/{bundleId}.get.responses.200.content.application/json.schema.properties.message` | field [message] removed |
| `response_schema_const_removed` | `paths./api/admin/dashboard.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subscriptions_active_count` | const removed (value set widened) |
| `response_schema_const_removed` | `paths./api/admin/dashboard.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subscriptions_expired_count` | const removed (value set widened) |
| `response_schema_const_removed` | `paths./api/admin/dashboard.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subscriptions_near_renewal_count` | const removed (value set widened) |
| `response_schema_type_changed` | `paths./api/auth/accountant-reports.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items` | type changed (['string'] -> ['object']) |
| `response_schema_type_removed` | `paths./api/auth/onboarding/applications/recover/verify.post.responses.200.content.application/json.schema` | type removed (['object'] -> any) |
| `response_schema_field_removed` | `paths./api/auth/onboarding/applications/recover/verify.post.responses.200.content.application/json.schema.properties.data` | field [data] removed |
| `response_schema_field_removed` | `paths./api/auth/onboarding/applications/recover/verify.post.responses.200.content.application/json.schema.properties.message` | field [message] removed |
| `required_request_body_added` | `paths./api/auth/onboarding/applications/{reference}/package.put.requestBody` | request body added and REQUIRED |
| `response_schema_field_removed` | `paths./api/auth/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | field [items] removed |
| `response_schema_field_removed` | `paths./api/owner/accounting/accounts.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | field [items] removed |
| `response_schema_field_removed` | `paths./api/owner/accounting/assets.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | field [items] removed |
| `response_schema_field_removed` | `paths./api/owner/accounting/journal-book.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | field [items] removed |
| `response_schema_nullability_added` | `paths./api/owner/accounting/journal-book.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta` | type now also accepts/returns null |
| `response_schema_constraint_widened` | `paths./api/owner/accounting/journal-book.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.current_page` | [minimum] 1 -> None |
| `response_schema_nullability_added` | `paths./api/owner/accounting/journal-book.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.current_page` | type now also accepts/returns null |
| `response_schema_constraint_widened` | `paths./api/owner/accounting/journal-book.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.last_page` | [minimum] 1 -> None |
| `response_schema_nullability_added` | `paths./api/owner/accounting/journal-book.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.last_page` | type now also accepts/returns null |
| `response_schema_constraint_widened` | `paths./api/owner/accounting/journal-book.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.total` | [minimum] 0 -> None |
| `response_schema_nullability_added` | `paths./api/owner/accounting/journal-book.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.total` | type now also accepts/returns null |
| `response_schema_field_removed` | `paths./api/owner/accounting/reports/trial-balance.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | field [items] removed |
| `response_schema_nullability_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | type now also accepts/returns null |
| `response_schema_nullability_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta` | type now also accepts/returns null |
| `response_schema_constraint_widened` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.current_page` | [minimum] 1 -> None |
| `response_schema_nullability_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.current_page` | type now also accepts/returns null |
| `response_schema_constraint_widened` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.last_page` | [minimum] 1 -> None |
| `response_schema_nullability_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.last_page` | type now also accepts/returns null |
| `response_schema_constraint_widened` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.total` | [minimum] 0 -> None |
| `response_schema_nullability_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.total` | type now also accepts/returns null |
| `response_schema_nullability_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary` | type now also accepts/returns null |
| `response_schema_type_changed` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.approved_total` | type changed (['string'] -> ['integer', 'null']) |
| `response_schema_type_changed` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.due_total` | type changed (['string'] -> ['integer', 'null']) |
| `response_schema_type_changed` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.input_vat` | type changed (['string'] -> ['null', 'number']) |
| `response_schema_constraint_widened` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.under_review_count` | [minimum] 0 -> None |
| `response_schema_nullability_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.under_review_count` | type now also accepts/returns null |
| `request_media_type_removed` | `paths./api/owner/expenses/expenses/documents.post.requestBody.content.application/json` | request media type [application/json] removed |
| `response_schema_type_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0]` | type removed (['object'] -> any) |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.account_reference` | field [account_reference] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.accountant_notes` | field [accountant_notes] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.amount_before_tax` | field [amount_before_tax] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.branch_id` | field [branch_id] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.description` | field [description] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.document_url` | field [document_url] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.due_date` | field [due_date] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.expense_category` | field [expense_category] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.extracted_data` | field [extracted_data] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.invoice_date` | field [invoice_date] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.invoice_number` | field [invoice_number] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.modification_history` | field [modification_history] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.operation_type` | field [operation_type] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.original_document_path` | field [original_document_path] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.paid_amount` | field [paid_amount] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.payment_method` | field [payment_method] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.payment_status` | field [payment_status] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.po_number` | field [po_number] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.public_reference` | field [public_reference] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.purchase_order_reference` | field [purchase_order_reference] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.remaining_amount` | field [remaining_amount] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.review_status` | field [review_status] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.source` | field [source] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.supplier_reference` | field [supplier_reference] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.suspicion_reason` | field [suspicion_reason] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.total_amount` | field [total_amount] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.uploaded_by_reference` | field [uploaded_by_reference] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.vat_amount` | field [vat_amount] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.vendor_name` | field [vendor_name] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.version` | field [version] removed |
| `response_schema_field_removed` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.available_count` | field [available_count] removed |
| `response_schema_field_removed` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.available_value` | field [available_value] removed |
| `response_schema_field_removed` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.branch_label` | field [branch_label] removed |
| `response_schema_field_removed` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.integrations` | field [integrations] removed |
| `response_schema_field_removed` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.items_count` | field [items_count] removed |
| `response_schema_field_removed` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.low_count` | field [low_count] removed |
| `response_schema_field_removed` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.out_count` | field [out_count] removed |
| `response_schema_field_removed` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.total_value` | field [total_value] removed |
| `response_schema_field_removed` | `paths./api/owner/inventory/inventory/items/{item}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | field [items] removed |
| `response_schema_field_removed` | `paths./api/owner/meetings/meetings/{meetingReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | field [items] removed |
| `response_schema_field_removed` | `paths./api/owner/payroll/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | field [items] removed |
| `response_schema_type_removed` | `paths./api/owner/payroll/payroll/employees/form-options.get.responses.200.content.application/json.schema` | type removed (['object'] -> any) |
| `response_schema_field_removed` | `paths./api/owner/payroll/payroll/employees/form-options.get.responses.200.content.application/json.schema.properties.data` | field [data] removed |
| `response_schema_field_removed` | `paths./api/owner/payroll/payroll/employees/form-options.get.responses.200.content.application/json.schema.properties.message` | field [message] removed |
| `response_schema_type_removed` | `paths./api/owner/payroll/payroll/run.get.responses.200.content.application/json.schema` | type removed (['object'] -> any) |
| `response_schema_field_removed` | `paths./api/owner/payroll/payroll/run.get.responses.200.content.application/json.schema.properties.data` | field [data] removed |
| `response_schema_field_removed` | `paths./api/owner/payroll/payroll/run.get.responses.200.content.application/json.schema.properties.message` | field [message] removed |
| `response_schema_field_removed` | `paths./api/owner/payroll/payroll/runs.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | field [items] removed |
| `response_status_removed` | `paths./api/owner/payroll/payroll/runs.post.responses.201` | response [201] removed from the contract |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.establishment` | field [establishment] removed |
| `response_schema_nullability_added` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | type now also accepts/returns null |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.approved_by` | field [approved_by] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.current_sale_price` | field [current_sale_price] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.final_margin_percent` | field [final_margin_percent] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.final_profit` | field [final_profit] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.final_sale_price` | field [final_sale_price] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.finalized_at` | field [finalized_at] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.last_updated_at` | field [last_updated_at] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.materials.items.properties.component_reference` | field [component_reference] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.materials.items.properties.id` | field [id] removed |
| `response_schema_type_changed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.materials.items.properties.quantity` | type changed (['string'] -> ['null', 'number']) |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.materials.items.properties.supplier_reference` | field [supplier_reference] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.materials.items.properties.total_cost` | field [total_cost] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.materials.items.properties.unit_cost` | field [unit_cost] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.operating_cost_per_unit` | field [operating_cost_per_unit] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.operating_items.items.properties.cost_item_name` | field [cost_item_name] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.operating_items.items.properties.unit_share` | field [unit_share] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.previous_sale_price` | field [previous_sale_price] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.pricing_session_reference` | field [pricing_session_reference] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.pricing_status` | field [pricing_status] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.product_name` | field [product_name] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.product_reference` | field [product_reference] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.proposed_margin_percent` | field [proposed_margin_percent] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.proposed_profit` | field [proposed_profit] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.proposed_sale_price` | field [proposed_sale_price] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.submitted_at` | field [submitted_at] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.submitted_by` | field [submitted_by] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.submitted_by_name` | field [submitted_by_name] removed |
| `response_schema_type_changed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.total_cost` | type changed (['string'] -> ['null', 'number']) |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.total_material_cost` | field [total_material_cost] removed |
| `response_schema_nullability_added` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.version` | type now also accepts/returns null |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.waste` | field [waste] removed |
| `response_schema_nullability_added` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta` | type now also accepts/returns null |
| `response_schema_constraint_widened` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.current_page` | [minimum] 1 -> None |
| `response_schema_nullability_added` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.current_page` | type now also accepts/returns null |
| `response_schema_constraint_widened` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.last_page` | [minimum] 1 -> None |
| `response_schema_nullability_added` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.last_page` | type now also accepts/returns null |
| `response_schema_constraint_widened` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.total` | [minimum] 0 -> None |
| `response_schema_nullability_added` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.total` | type now also accepts/returns null |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.current` | field [current] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.establishment` | field [establishment] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.history` | field [history] removed |
| `response_schema_field_removed` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.waste` | field [waste] removed |
| `response_schema_const_changed` | `paths./api/owner/purchases/purchase-orders.post.responses.200.content.application/json.schema.allOf[1].properties.data` | const added with a value the other schema does not accept |
| `response_schema_type_changed` | `paths./api/owner/purchases/purchase-orders.post.responses.200.content.application/json.schema.allOf[1].properties.data` | type changed (['string'] -> ['integer']) |
| `required_request_body_added` | `paths./api/owner/purchases/purchase-orders/{reference}/supplier-invoice.post.requestBody` | request body added and REQUIRED |
| `response_schema_const_changed` | `paths./api/owner/purchases/purchase-orders/{reference}/supplier-invoice.post.responses.200.content.application/json.schema.allOf[1].properties.data` | const added with a value the other schema does not accept |
| `response_schema_type_changed` | `paths./api/owner/purchases/purchase-orders/{reference}/supplier-invoice.post.responses.200.content.application/json.schema.allOf[1].properties.data` | type changed (['string'] -> ['integer']) |
| `request_schema_field_removed` | `paths./api/owner/purchases/suppliers/pay.post.requestBody.content.multipart/form-data.schema.properties.amount` | field [amount] removed |
| `request_schema_field_removed` | `paths./api/owner/purchases/suppliers/pay.post.requestBody.content.multipart/form-data.schema.properties.date` | field [date] removed |
| `request_schema_field_removed` | `paths./api/owner/purchases/suppliers/pay.post.requestBody.content.multipart/form-data.schema.properties.invoice_id` | field [invoice_id] removed |
| `request_schema_field_removed` | `paths./api/owner/purchases/suppliers/pay.post.requestBody.content.multipart/form-data.schema.properties.notes` | field [notes] removed |
| `request_schema_field_removed` | `paths./api/owner/purchases/suppliers/pay.post.requestBody.content.multipart/form-data.schema.properties.payment_method` | field [payment_method] removed |
| `request_schema_field_removed` | `paths./api/owner/purchases/suppliers/pay.post.requestBody.content.multipart/form-data.schema.properties.proof` | field [proof] removed |
| `request_schema_field_removed` | `paths./api/owner/purchases/suppliers/pay.post.requestBody.content.multipart/form-data.schema.properties.reference` | field [reference] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.accountant_notes` | field [accountant_notes] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branch_id` | field [branch_id] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.document_url` | field [document_url] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.draft_version` | field [draft_version] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.fiscal_period_reference` | field [fiscal_period_reference] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.generated_at` | field [generated_at] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.generated_by_kind` | field [generated_by_kind] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.generated_by_reference` | field [generated_by_reference] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.indicators` | field [indicators] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.issued_months` | field [issued_months] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.period` | field [period] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.reference` | field [reference] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.report_month` | field [report_month] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.reviewed_at` | field [reviewed_at] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.reviewed_by_reference` | field [reviewed_by_reference] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.revision` | field [revision] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.revision_of_reference` | field [revision_of_reference] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.revision_reason` | field [revision_reason] removed |
| `response_schema_items_changed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.sections` | array items schema removed or added |
| `response_schema_type_changed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.sections` | type changed (['object'] -> ['array', 'null']) |
| `response_schema_field_removed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.sent_at` | field [sent_at] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.sent_by_name` | field [sent_by_name] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.sent_by_reference` | field [sent_by_reference] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | field [status] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.version` | field [version] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.view` | field [view] removed |
| `response_schema_type_changed` | `paths./api/owner/reports/statements/export-bundle.post.responses.200.content.application/json.schema.allOf[1].properties.data` | type changed (['string'] -> ['object']) |
| `response_schema_type_removed` | `paths./api/owner/reports/statements/export-bundle/{bundleId}.get.responses.200.content.application/json.schema` | type removed (['object'] -> any) |
| `response_schema_field_removed` | `paths./api/owner/reports/statements/export-bundle/{bundleId}.get.responses.200.content.application/json.schema.properties.data` | field [data] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/statements/export-bundle/{bundleId}.get.responses.200.content.application/json.schema.properties.message` | field [message] removed |
| `response_status_removed` | `paths./api/owner/settings/branches.post.responses.201` | response [201] removed from the contract |
| `response_schema_field_removed` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | field [items] removed |
| `response_schema_type_changed` | `paths./api/owner/summary/more/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data` | type changed (['string'] -> ['object']) |
| `response_schema_const_changed` | `paths./api/owner/tax/tax/documents/upload.post.responses.200.content.application/json.schema.allOf[1].properties.data` | const added with a value the other schema does not accept |
| `response_schema_type_changed` | `paths./api/owner/tax/tax/documents/upload.post.responses.200.content.application/json.schema.allOf[1].properties.data` | type changed (['string'] -> ['integer']) |
| `response_schema_type_removed` | `paths./api/owner/tax/tax/vat-returns/export.post.responses.200.content.application/json.schema` | type removed (['object'] -> any) |
| `response_schema_field_removed` | `paths./api/owner/tax/tax/vat-returns/export.post.responses.200.content.application/json.schema.properties.data` | field [data] removed |
| `response_schema_field_removed` | `paths./api/owner/tax/tax/vat-returns/export.post.responses.200.content.application/json.schema.properties.message` | field [message] removed |
| `response_schema_nullability_added` | `paths./api/owner/tax/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.completeness` | type now also accepts/returns null |
| `response_schema_nullability_added` | `paths./api/owner/tax/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.completeness.properties.complete` | type now also accepts/returns null |
| `response_schema_field_removed` | `paths./api/owner/tax/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.completeness.properties.missing_vat` | field [missing_vat] removed |
| `response_schema_field_removed` | `paths./api/owner/tax/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.completeness.properties.missing_vat_count` | field [missing_vat_count] removed |
| `response_schema_field_removed` | `paths./api/owner/tax/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.completeness.properties.needs_review_count` | field [needs_review_count] removed |
| `response_schema_nullability_added` | `paths./api/owner/tax/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.documents` | type now also accepts/returns null |
| `response_schema_field_removed` | `paths./api/owner/tax/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.from` | field [from] removed |
| `response_schema_type_changed` | `paths./api/owner/tax/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.input_vat` | type changed (['null', 'string'] -> ['integer', 'null']) |
| `response_schema_field_removed` | `paths./api/owner/tax/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.net_tax_due` | field [net_tax_due] removed |
| `response_schema_type_changed` | `paths./api/owner/tax/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.net_vat` | type changed (['null', 'string'] -> ['null', 'number']) |
| `response_schema_type_changed` | `paths./api/owner/tax/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.output_vat` | type changed (['null', 'string'] -> ['null', 'number']) |
| `response_schema_field_removed` | `paths./api/owner/tax/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.period_type` | field [period_type] removed |
| `response_schema_field_removed` | `paths./api/owner/tax/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.period_value` | field [period_value] removed |
| `response_schema_nullability_added` | `paths./api/owner/tax/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.sources` | type now also accepts/returns null |
| `response_schema_field_removed` | `paths./api/owner/tax/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.to` | field [to] removed |
| `response_schema_field_removed` | `paths./api/owner/tax/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total_purchases_amount` | field [total_purchases_amount] removed |
| `response_schema_field_removed` | `paths./api/owner/tax/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total_purchases_tax` | field [total_purchases_tax] removed |
| `response_schema_field_removed` | `paths./api/owner/tax/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total_sales_amount` | field [total_sales_amount] removed |
| `response_schema_field_removed` | `paths./api/owner/tax/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total_sales_tax` | field [total_sales_tax] removed |
| `response_schema_field_removed` | `paths./api/owner/tax/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.year` | field [year] removed |
| `response_schema_items_changed` | `paths./api/owner/tax/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.years` | array items schema removed or added |
| `response_schema_field_removed` | `paths./api/owner/tax/zakat/sessions/{uuid}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.fiscal_period` | field [fiscal_period] removed |
| `response_schema_nullability_added` | `paths./api/owner/tax/zakat/sessions/{uuid}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.periods` | type now also accepts/returns null |
| `response_schema_field_removed` | `paths./api/owner/tax/zakat/sessions/{uuid}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.periods.items.properties.ends_on` | field [ends_on] removed |
| `response_schema_nullability_added` | `paths./api/owner/tax/zakat/sessions/{uuid}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.periods.items.properties.id` | type now also accepts/returns null |
| `response_schema_field_removed` | `paths./api/owner/tax/zakat/sessions/{uuid}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.periods.items.properties.starts_on` | field [starts_on] removed |
| `response_schema_type_changed` | `paths./api/v1/accountant-reports.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items` | type changed (['string'] -> ['object']) |
| `response_schema_field_removed` | `paths./api/v1/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | field [items] removed |
| `response_schema_nullability_added` | `paths./api/v1/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta` | type now also accepts/returns null |
| `response_schema_constraint_widened` | `paths./api/v1/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.current_page` | [minimum] 1 -> None |
| `response_schema_nullability_added` | `paths./api/v1/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.current_page` | type now also accepts/returns null |
| `response_schema_constraint_widened` | `paths./api/v1/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.last_page` | [minimum] 1 -> None |
| `response_schema_nullability_added` | `paths./api/v1/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.last_page` | type now also accepts/returns null |
| `response_schema_constraint_widened` | `paths./api/v1/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.total` | [minimum] 0 -> None |
| `response_schema_nullability_added` | `paths./api/v1/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.total` | type now also accepts/returns null |
| `response_schema_field_removed` | `paths./api/v1/accounting/reports/trial-balance.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | field [items] removed |
| `response_schema_field_removed` | `paths./api/v1/accounts.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | field [items] removed |
| `response_schema_field_removed` | `paths./api/v1/assets.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | field [items] removed |
| `response_status_removed` | `paths./api/v1/branches.post.responses.201` | response [201] removed from the contract |
| `response_schema_field_removed` | `paths./api/v1/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | field [items] removed |
| `request_schema_field_became_required` | `paths./api/v1/erp/onboarding/applications/{reference}/package.put.requestBody.content.application/json.schema.properties.package_id` | field [package_id] became required |
| `request_body_became_required` | `paths./api/v1/erp/onboarding/applications/{reference}/package.put.requestBody.required` | request body became required |
| `response_schema_field_removed` | `paths./api/v1/erp/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | field [items] removed |
| `response_schema_nullability_added` | `paths./api/v1/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | type now also accepts/returns null |
| `response_schema_nullability_added` | `paths./api/v1/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta` | type now also accepts/returns null |
| `response_schema_constraint_widened` | `paths./api/v1/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.current_page` | [minimum] 1 -> None |
| `response_schema_nullability_added` | `paths./api/v1/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.current_page` | type now also accepts/returns null |
| `response_schema_constraint_widened` | `paths./api/v1/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.last_page` | [minimum] 1 -> None |
| `response_schema_nullability_added` | `paths./api/v1/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.last_page` | type now also accepts/returns null |
| `response_schema_constraint_widened` | `paths./api/v1/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.total` | [minimum] 0 -> None |
| `response_schema_nullability_added` | `paths./api/v1/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.total` | type now also accepts/returns null |
| `response_schema_nullability_added` | `paths./api/v1/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary` | type now also accepts/returns null |
| `response_schema_type_changed` | `paths./api/v1/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.approved_total` | type changed (['string'] -> ['integer', 'null']) |
| `response_schema_type_changed` | `paths./api/v1/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.due_total` | type changed (['string'] -> ['integer', 'null']) |
| `response_schema_type_changed` | `paths./api/v1/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.input_vat` | type changed (['string'] -> ['null', 'number']) |
| `response_schema_constraint_widened` | `paths./api/v1/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.under_review_count` | [minimum] 0 -> None |
| `response_schema_nullability_added` | `paths./api/v1/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.under_review_count` | type now also accepts/returns null |
| `request_media_type_removed` | `paths./api/v1/expenses/documents.post.requestBody.content.application/json` | request media type [application/json] removed |
| `response_schema_type_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0]` | type removed (['object'] -> any) |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.account_reference` | field [account_reference] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.accountant_notes` | field [accountant_notes] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.amount_before_tax` | field [amount_before_tax] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.branch_id` | field [branch_id] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.description` | field [description] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.document_url` | field [document_url] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.due_date` | field [due_date] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.expense_category` | field [expense_category] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.extracted_data` | field [extracted_data] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.invoice_date` | field [invoice_date] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.invoice_number` | field [invoice_number] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.modification_history` | field [modification_history] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.operation_type` | field [operation_type] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.original_document_path` | field [original_document_path] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.paid_amount` | field [paid_amount] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.payment_method` | field [payment_method] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.payment_status` | field [payment_status] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.po_number` | field [po_number] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.public_reference` | field [public_reference] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.purchase_order_reference` | field [purchase_order_reference] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.remaining_amount` | field [remaining_amount] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.review_status` | field [review_status] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.source` | field [source] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.supplier_reference` | field [supplier_reference] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.suspicion_reason` | field [suspicion_reason] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.total_amount` | field [total_amount] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.uploaded_by_reference` | field [uploaded_by_reference] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.vat_amount` | field [vat_amount] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.vendor_name` | field [vendor_name] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.version` | field [version] removed |
| `response_schema_field_removed` | `paths./api/v1/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.available_count` | field [available_count] removed |
| `response_schema_field_removed` | `paths./api/v1/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.available_value` | field [available_value] removed |
| `response_schema_field_removed` | `paths./api/v1/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.branch_label` | field [branch_label] removed |
| `response_schema_field_removed` | `paths./api/v1/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.integrations` | field [integrations] removed |
| `response_schema_field_removed` | `paths./api/v1/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.items_count` | field [items_count] removed |
| `response_schema_field_removed` | `paths./api/v1/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.low_count` | field [low_count] removed |
| `response_schema_field_removed` | `paths./api/v1/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.out_count` | field [out_count] removed |
| `response_schema_field_removed` | `paths./api/v1/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.total_value` | field [total_value] removed |
| `response_schema_field_removed` | `paths./api/v1/inventory/items/{item}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | field [items] removed |
| `response_schema_field_removed` | `paths./api/v1/meetings/{meetingReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | field [items] removed |
| `response_schema_field_removed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.accountant_notes` | field [accountant_notes] removed |
| `response_schema_field_removed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branch_id` | field [branch_id] removed |
| `response_schema_field_removed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.document_url` | field [document_url] removed |
| `response_schema_field_removed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.draft_version` | field [draft_version] removed |
| `response_schema_field_removed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.fiscal_period_reference` | field [fiscal_period_reference] removed |
| `response_schema_field_removed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.generated_at` | field [generated_at] removed |
| `response_schema_field_removed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.generated_by_kind` | field [generated_by_kind] removed |
| `response_schema_field_removed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.generated_by_reference` | field [generated_by_reference] removed |
| `response_schema_field_removed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.indicators` | field [indicators] removed |
| `response_schema_field_removed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.issued_months` | field [issued_months] removed |
| `response_schema_field_removed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.period` | field [period] removed |
| `response_schema_field_removed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.reference` | field [reference] removed |
| `response_schema_field_removed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.report_month` | field [report_month] removed |
| `response_schema_field_removed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.reviewed_at` | field [reviewed_at] removed |
| `response_schema_field_removed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.reviewed_by_reference` | field [reviewed_by_reference] removed |
| `response_schema_field_removed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.revision` | field [revision] removed |
| `response_schema_field_removed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.revision_of_reference` | field [revision_of_reference] removed |
| `response_schema_field_removed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.revision_reason` | field [revision_reason] removed |
| `response_schema_items_changed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.sections` | array items schema removed or added |
| `response_schema_type_changed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.sections` | type changed (['object'] -> ['array', 'null']) |
| `response_schema_field_removed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.sent_at` | field [sent_at] removed |
| `response_schema_field_removed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.sent_by_name` | field [sent_by_name] removed |
| `response_schema_field_removed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.sent_by_reference` | field [sent_by_reference] removed |
| `response_schema_field_removed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | field [status] removed |
| `response_schema_field_removed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.version` | field [version] removed |
| `response_schema_field_removed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.view` | field [view] removed |
| `response_schema_type_changed` | `paths./api/v1/more/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data` | type changed (['string'] -> ['object']) |
| `response_schema_type_removed` | `paths./api/v1/onboarding/applications/recover/verify.post.responses.200.content.application/json.schema` | type removed (['object'] -> any) |
| `response_schema_field_removed` | `paths./api/v1/onboarding/applications/recover/verify.post.responses.200.content.application/json.schema.properties.data` | field [data] removed |
| `response_schema_field_removed` | `paths./api/v1/onboarding/applications/recover/verify.post.responses.200.content.application/json.schema.properties.message` | field [message] removed |
| `response_schema_field_removed` | `paths./api/v1/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | field [items] removed |
| `response_schema_type_removed` | `paths./api/v1/payroll/employees/form-options.get.responses.200.content.application/json.schema` | type removed (['object'] -> any) |
| `response_schema_field_removed` | `paths./api/v1/payroll/employees/form-options.get.responses.200.content.application/json.schema.properties.data` | field [data] removed |
| `response_schema_field_removed` | `paths./api/v1/payroll/employees/form-options.get.responses.200.content.application/json.schema.properties.message` | field [message] removed |
| `response_schema_type_removed` | `paths./api/v1/payroll/run.get.responses.200.content.application/json.schema` | type removed (['object'] -> any) |
| `response_schema_field_removed` | `paths./api/v1/payroll/run.get.responses.200.content.application/json.schema.properties.data` | field [data] removed |
| `response_schema_field_removed` | `paths./api/v1/payroll/run.get.responses.200.content.application/json.schema.properties.message` | field [message] removed |
| `response_schema_field_removed` | `paths./api/v1/payroll/runs.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | field [items] removed |
| `response_status_removed` | `paths./api/v1/payroll/runs.post.responses.201` | response [201] removed from the contract |
| `response_schema_const_removed` | `paths./api/v1/platform/dashboard.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subscriptions_active_count` | const removed (value set widened) |
| `response_schema_const_removed` | `paths./api/v1/platform/dashboard.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subscriptions_expired_count` | const removed (value set widened) |
| `response_schema_const_removed` | `paths./api/v1/platform/dashboard.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subscriptions_near_renewal_count` | const removed (value set widened) |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.establishment` | field [establishment] removed |
| `response_schema_nullability_added` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | type now also accepts/returns null |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.approved_by` | field [approved_by] removed |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.current_sale_price` | field [current_sale_price] removed |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.final_margin_percent` | field [final_margin_percent] removed |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.final_profit` | field [final_profit] removed |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.final_sale_price` | field [final_sale_price] removed |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.finalized_at` | field [finalized_at] removed |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.last_updated_at` | field [last_updated_at] removed |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.materials.items.properties.component_reference` | field [component_reference] removed |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.materials.items.properties.id` | field [id] removed |
| `response_schema_type_changed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.materials.items.properties.quantity` | type changed (['string'] -> ['null', 'number']) |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.materials.items.properties.supplier_reference` | field [supplier_reference] removed |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.materials.items.properties.total_cost` | field [total_cost] removed |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.materials.items.properties.unit_cost` | field [unit_cost] removed |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.operating_cost_per_unit` | field [operating_cost_per_unit] removed |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.operating_items.items.properties.cost_item_name` | field [cost_item_name] removed |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.operating_items.items.properties.unit_share` | field [unit_share] removed |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.previous_sale_price` | field [previous_sale_price] removed |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.pricing_session_reference` | field [pricing_session_reference] removed |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.pricing_status` | field [pricing_status] removed |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.product_name` | field [product_name] removed |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.product_reference` | field [product_reference] removed |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.proposed_margin_percent` | field [proposed_margin_percent] removed |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.proposed_profit` | field [proposed_profit] removed |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.proposed_sale_price` | field [proposed_sale_price] removed |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.submitted_at` | field [submitted_at] removed |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.submitted_by` | field [submitted_by] removed |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.submitted_by_name` | field [submitted_by_name] removed |
| `response_schema_type_changed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.total_cost` | type changed (['string'] -> ['null', 'number']) |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.total_material_cost` | field [total_material_cost] removed |
| `response_schema_nullability_added` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.version` | type now also accepts/returns null |
| `response_schema_field_removed` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.waste` | field [waste] removed |
| `response_schema_nullability_added` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta` | type now also accepts/returns null |
| `response_schema_constraint_widened` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.current_page` | [minimum] 1 -> None |
| `response_schema_nullability_added` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.current_page` | type now also accepts/returns null |

_… and 55 more (see the JSON report)._

## Unclassified changes (fail closed) (35)

| Kind | Location | Detail |
|---|---|---|
| `response_schema_anyOf_changed` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0]` | anyOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/accountant/reports/statements/export-bundle/{bundleId}.get.responses.200.content.application/json.schema` | allOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/accountant/reports/statements/export.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/auth/onboarding/applications/recover/verify.post.responses.200.content.application/json.schema` | allOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/owner/accounting/assets/{asset}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | allOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/owner/accounting/financial-statements.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/owner/accounting/financial-statements/{statement}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/owner/accounting/journal-book/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/owner/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0]` | anyOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/owner/payroll/payroll/employees/form-options.get.responses.200.content.application/json.schema` | allOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/owner/payroll/payroll/run.get.responses.200.content.application/json.schema` | allOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/owner/purchases/purchase-orders.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/owner/purchases/purchase-orders/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `request_schema_allOf_changed` | `paths./api/owner/purchases/suppliers/pay.post.requestBody.content.multipart/form-data.schema` | allOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/owner/reports/statements/export-bundle/{bundleId}.get.responses.200.content.application/json.schema` | allOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/owner/reports/statements/export.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/owner/tax/tax/vat-returns/export.post.responses.200.content.application/json.schema` | allOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/owner/tax/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.years` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounting/financial-statements.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounting/financial-statements/{statement}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounting/journal-entries/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/v1/assets/{asset}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | allOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0]` | anyOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/v1/onboarding/applications/recover/verify.post.responses.200.content.application/json.schema` | allOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/v1/payroll/employees/form-options.get.responses.200.content.application/json.schema` | allOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/v1/payroll/run.get.responses.200.content.application/json.schema` | allOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/purchase-orders.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/purchase-orders/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/v1/statements/export-bundle/{bundleId}.get.responses.200.content.application/json.schema` | allOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/statements/export.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `request_schema_allOf_changed` | `paths./api/v1/suppliers/pay.post.requestBody.content.multipart/form-data.schema` | allOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/v1/tax/vat-returns/export.post.responses.200.content.application/json.schema` | allOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.years` | anyOf composition added or removed |

## Non-breaking changes (848)

| Kind | Location | Detail |
|---|---|---|
| `shared_component_added` | `components.schemas.ChannelAuthorizationRequest` | component [schemas.ChannelAuthorizationRequest] added |
| `component_schema_field_added` | `components.schemas.CreateSupplierRequest.properties.whatsapp` | new optional field [whatsapp] |
| `shared_component_added` | `components.schemas.DirectPurchaseResource` | component [schemas.DirectPurchaseResource] added |
| `component_schema_field_added` | `components.schemas.RenewSubscriptionRequest.properties.payment_method` | new optional field [payment_method] |
| `component_schema_field_added` | `components.schemas.RenewSubscriptionRequest.properties.payment_reference` | new optional field [payment_reference] |
| `shared_component_added` | `components.schemas.ScanProofRequest` | component [schemas.ScanProofRequest] added |
| `component_schema_required_field_added` | `components.schemas.SupplierResource.properties.classification` | new REQUIRED field [classification] |
| `component_schema_field_added` | `components.schemas.UpdateSupplierRequest.properties.whatsapp` | new optional field [whatsapp] |
| `optional_parameter_added` | `paths./api/accountant/inventory/inventory/items.get.parameters.all` | optional parameter [all] (in query) added |
| `optional_parameter_added` | `paths./api/accountant/inventory/inventory/items.get.parameters.fields` | optional parameter [fields] (in query) added |
| `response_schema_type_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items` | type added (any -> ['object']) |
| `response_schema_type_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.current_page` | type added (any -> ['integer']) |
| `response_schema_type_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.last_page` | type added (any -> ['integer']) |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items/{item}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.moves` | new REQUIRED field [moves] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items/{item}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.usage` | new REQUIRED field [usage] |
| `operation_added` | `paths./api/accountant/purchases/direct-purchases.get` | GET /api/accountant/purchases/direct-purchases added to the contract |
| `operation_added` | `paths./api/accountant/purchases/direct-purchases/{reference}.get` | GET /api/accountant/purchases/direct-purchases/{reference} added to the contract |
| `optional_parameter_added` | `paths./api/accountant/purchases/suppliers.get.parameters.classification` | optional parameter [classification] (in query) added |
| `response_schema_required_field_added` | `paths./api/accountant/reports/statements/export-bundle.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.error` | new REQUIRED field [error] |
| `response_schema_required_field_added` | `paths./api/accountant/reports/statements/export-bundle.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.expires_at` | new REQUIRED field [expires_at] |
| `response_schema_required_field_added` | `paths./api/accountant/reports/statements/export-bundle.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.file_url` | new REQUIRED field [file_url] |
| `response_schema_required_field_added` | `paths./api/accountant/reports/statements/export-bundle.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.format` | new REQUIRED field [format] |
| `response_schema_required_field_added` | `paths./api/accountant/reports/statements/export-bundle.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/accountant/reports/statements/export-bundle.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.reports` | new REQUIRED field [reports] |
| `response_schema_required_field_added` | `paths./api/accountant/reports/statements/export-bundle.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | new REQUIRED field [status] |
| `response_schema_type_added` | `paths./api/accountant/reports/statements/export.get.responses.200.content.application/json.schema.allOf[1].properties.data` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/accountant/reports/statements/export.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.file_url` | new REQUIRED field [file_url] |
| `response_schema_required_field_added` | `paths./api/auth/accountant-reports.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.accountant` | new REQUIRED field [accountant] |
| `response_schema_required_field_added` | `paths./api/auth/accountant-reports.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.figures` | new REQUIRED field [figures] |
| `response_schema_required_field_added` | `paths./api/auth/accountant-reports.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.file_url` | new REQUIRED field [file_url] |
| `response_schema_required_field_added` | `paths./api/auth/accountant-reports.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/auth/accountant-reports.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.issued_at` | new REQUIRED field [issued_at] |
| `response_schema_required_field_added` | `paths./api/auth/accountant-reports.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.notes` | new REQUIRED field [notes] |
| `response_schema_required_field_added` | `paths./api/auth/accountant-reports.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.period` | new REQUIRED field [period] |
| `response_schema_required_field_added` | `paths./api/auth/accountant-reports.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.summary` | new REQUIRED field [summary] |
| `response_schema_required_field_added` | `paths./api/auth/accountant-reports.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.title` | new REQUIRED field [title] |
| `response_schema_required_field_added` | `paths./api/auth/accountant-reports.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.type` | new REQUIRED field [type] |
| `response_schema_nullability_removed` | `paths./api/auth/accountant-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | type no longer accepts/returns null |
| `response_schema_required_field_added` | `paths./api/auth/accountant-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.accountant` | new REQUIRED field [accountant] |
| `response_schema_required_field_added` | `paths./api/auth/accountant-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.figures` | new REQUIRED field [figures] |
| `response_schema_required_field_added` | `paths./api/auth/accountant-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.file_url` | new REQUIRED field [file_url] |
| `response_schema_required_field_added` | `paths./api/auth/accountant-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/auth/accountant-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.issued_at` | new REQUIRED field [issued_at] |
| `response_schema_required_field_added` | `paths./api/auth/accountant-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.notes` | new REQUIRED field [notes] |
| `response_schema_required_field_added` | `paths./api/auth/accountant-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.period` | new REQUIRED field [period] |
| `response_schema_required_field_added` | `paths./api/auth/accountant-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary` | new REQUIRED field [summary] |
| `response_schema_required_field_added` | `paths./api/auth/accountant-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.title` | new REQUIRED field [title] |
| `response_schema_required_field_added` | `paths./api/auth/accountant-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.type` | new REQUIRED field [type] |
| `optional_parameter_added` | `paths./api/auth/accounting/journal-entries.get.parameters.from_date` | optional parameter [from_date] (in query) added |
| `optional_parameter_added` | `paths./api/auth/accounting/journal-entries.get.parameters.status` | optional parameter [status] (in query) added |
| `optional_parameter_added` | `paths./api/auth/accounting/journal-entries.get.parameters.to_date` | optional parameter [to_date] (in query) added |
| `operation_added` | `paths./api/auth/broadcasting/auth.post` | POST /api/auth/broadcasting/auth added to the contract |
| `response_schema_required_field_added` | `paths./api/auth/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.account_holder` | new REQUIRED field [account_holder] |
| `response_schema_required_field_added` | `paths./api/auth/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.account_number` | new REQUIRED field [account_number] |
| `response_schema_required_field_added` | `paths./api/auth/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.available_payment_methods` | new REQUIRED field [available_payment_methods] |
| `response_schema_required_field_added` | `paths./api/auth/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.bank_name` | new REQUIRED field [bank_name] |
| `response_schema_required_field_added` | `paths./api/auth/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.duration_months` | new REQUIRED field [duration_months] |
| `response_schema_required_field_added` | `paths./api/auth/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.iban` | new REQUIRED field [iban] |
| `response_schema_required_field_added` | `paths./api/auth/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.package_name` | new REQUIRED field [package_name] |
| `response_schema_required_field_added` | `paths./api/auth/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subscription_value` | new REQUIRED field [subscription_value] |
| `response_schema_required_field_added` | `paths./api/auth/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.swift` | new REQUIRED field [swift] |
| `response_schema_required_field_added` | `paths./api/auth/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total_amount` | new REQUIRED field [total_amount] |
| `response_schema_required_field_added` | `paths./api/auth/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.vat_rate` | new REQUIRED field [vat_rate] |
| `response_schema_required_field_added` | `paths./api/auth/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.vat_value` | new REQUIRED field [vat_value] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/accounts.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.accounts` | new REQUIRED field [accounts] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/accounts.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches` | new REQUIRED field [branches] |
| `optional_parameter_added` | `paths./api/owner/accounting/assets.get.parameters.search` | optional parameter [search] (in query) added |
| `optional_parameter_added` | `paths./api/owner/accounting/assets.get.parameters.status` | optional parameter [status] (in query) added |
| `optional_parameter_added` | `paths./api/owner/accounting/assets.get.parameters.type` | optional parameter [type] (in query) added |
| `response_schema_required_field_added` | `paths./api/owner/accounting/assets.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.assets` | new REQUIRED field [assets] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/assets.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary` | new REQUIRED field [summary] |
| `response_schema_type_added` | `paths./api/owner/accounting/assets/{asset}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/owner/accounting/assets/{asset}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.accumulated` | new REQUIRED field [accumulated] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/assets/{asset}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.annual_depreciation` | new REQUIRED field [annual_depreciation] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/assets/{asset}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.as_of` | new REQUIRED field [as_of] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/assets/{asset}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.book_value` | new REQUIRED field [book_value] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/assets/{asset}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branch` | new REQUIRED field [branch] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/assets/{asset}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.code` | new REQUIRED field [code] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/assets/{asset}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.cost` | new REQUIRED field [cost] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/assets/{asset}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.depreciable` | new REQUIRED field [depreciable] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/assets/{asset}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.depreciation_start` | new REQUIRED field [depreciation_start] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/assets/{asset}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/assets/{asset}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.life_years` | new REQUIRED field [life_years] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/assets/{asset}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.log` | new REQUIRED field [log] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/assets/{asset}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.monthly_depreciation` | new REQUIRED field [monthly_depreciation] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/assets/{asset}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.name` | new REQUIRED field [name] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/assets/{asset}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.notes` | new REQUIRED field [notes] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/assets/{asset}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.purchase_date` | new REQUIRED field [purchase_date] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/assets/{asset}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.salvage_value` | new REQUIRED field [salvage_value] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/assets/{asset}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | new REQUIRED field [status] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/assets/{asset}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.type` | new REQUIRED field [type] |
| `response_schema_type_added` | `paths./api/owner/accounting/financial-statements.get.responses.200.content.application/json.schema.allOf[1].properties.data` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/owner/accounting/financial-statements.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.accounts_count` | new REQUIRED field [accounts_count] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/financial-statements.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches` | new REQUIRED field [branches] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/financial-statements.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.expenses` | new REQUIRED field [expenses] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/financial-statements.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.journals_count` | new REQUIRED field [journals_count] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/financial-statements.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.monthly_report_label` | new REQUIRED field [monthly_report_label] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/financial-statements.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.revenue` | new REQUIRED field [revenue] |
| `response_schema_type_added` | `paths./api/owner/accounting/financial-statements/{statement}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/owner/accounting/financial-statements/{statement}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches` | new REQUIRED field [branches] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/financial-statements/{statement}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.hero` | new REQUIRED field [hero] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/financial-statements/{statement}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/financial-statements/{statement}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.sections` | new REQUIRED field [sections] |
| `response_schema_type_added` | `paths./api/owner/accounting/general-ledger.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches.items` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/owner/accounting/general-ledger.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches.items.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/general-ledger.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches.items.properties.name` | new REQUIRED field [name] |
| `optional_parameter_added` | `paths./api/owner/accounting/journal-book.get.parameters.from_date` | optional parameter [from_date] (in query) added |
| `optional_parameter_added` | `paths./api/owner/accounting/journal-book.get.parameters.status` | optional parameter [status] (in query) added |
| `optional_parameter_added` | `paths./api/owner/accounting/journal-book.get.parameters.to_date` | optional parameter [to_date] (in query) added |
| `response_schema_required_field_added` | `paths./api/owner/accounting/journal-book.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches` | new REQUIRED field [branches] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/journal-book.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.entries` | new REQUIRED field [entries] |
| `response_schema_type_added` | `paths./api/owner/accounting/journal-book/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/owner/accounting/journal-book/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.amount` | new REQUIRED field [amount] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/journal-book/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.created_at` | new REQUIRED field [created_at] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/journal-book/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.date` | new REQUIRED field [date] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/journal-book/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.description` | new REQUIRED field [description] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/journal-book/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/journal-book/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.lines` | new REQUIRED field [lines] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/journal-book/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.log` | new REQUIRED field [log] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/journal-book/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.operation_type` | new REQUIRED field [operation_type] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/journal-book/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.ref_id` | new REQUIRED field [ref_id] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/journal-book/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.ref_type` | new REQUIRED field [ref_type] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/journal-book/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.reference` | new REQUIRED field [reference] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/journal-book/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.source` | new REQUIRED field [source] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/journal-book/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | new REQUIRED field [status] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/journal-book/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.updated_at` | new REQUIRED field [updated_at] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/reports/trial-balance.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches` | new REQUIRED field [branches] |
| `response_schema_required_field_added` | `paths./api/owner/accounting/reports/trial-balance.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.rows` | new REQUIRED field [rows] |
| `response_schema_type_added` | `paths./api/owner/dashboard/owner.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches.items` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/owner/dashboard/owner.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches.items.properties.city` | new REQUIRED field [city] |
| `response_schema_required_field_added` | `paths./api/owner/dashboard/owner.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches.items.properties.code` | new REQUIRED field [code] |
| `response_schema_required_field_added` | `paths./api/owner/dashboard/owner.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches.items.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/owner/dashboard/owner.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches.items.properties.is_active` | new REQUIRED field [is_active] |
| `response_schema_required_field_added` | `paths./api/owner/dashboard/owner.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches.items.properties.name` | new REQUIRED field [name] |
| `response_schema_required_field_added` | `paths./api/owner/dashboard/owner.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches.items.properties.operations_count` | new REQUIRED field [operations_count] |
| `response_schema_required_field_added` | `paths./api/owner/dashboard/owner.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches.items.properties.short_name` | new REQUIRED field [short_name] |
| `optional_parameter_added` | `paths./api/owner/expenses/expense-analysis.get.parameters.period` | optional parameter [period] (in query) added |
| `optional_parameter_added` | `paths./api/owner/expenses/expense-analysis.get.parameters.period_type` | optional parameter [period_type] (in query) added |
| `optional_parameter_added` | `paths./api/owner/expenses/expense-analysis.get.parameters.year` | optional parameter [year] (in query) added |
| `response_schema_type_added` | `paths./api/owner/expenses/expense-analysis.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.categories.items` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-analysis.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.categories.items.properties.amount` | new REQUIRED field [amount] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-analysis.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.categories.items.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-analysis.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.categories.items.properties.name` | new REQUIRED field [name] |
| `response_schema_nullability_removed` | `paths./api/owner/expenses/expense-analysis.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total` | type no longer accepts/returns null |
| `optional_parameter_added` | `paths./api/owner/expenses/expense-register.get.parameters.review_status` | optional parameter [review_status] (in query) added |
| `response_schema_type_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.amount` | new REQUIRED field [amount] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.branch` | new REQUIRED field [branch] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.branch_id` | new REQUIRED field [branch_id] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.category` | new REQUIRED field [category] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.category_id` | new REQUIRED field [category_id] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.date` | new REQUIRED field [date] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.description` | new REQUIRED field [description] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.due_date` | new REQUIRED field [due_date] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.file_name` | new REQUIRED field [file_name] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.file_url` | new REQUIRED field [file_url] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.from_purchase` | new REQUIRED field [from_purchase] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.number` | new REQUIRED field [number] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.operation_type` | new REQUIRED field [operation_type] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.paid` | new REQUIRED field [paid] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.payment_method` | new REQUIRED field [payment_method] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.payment_method_id` | new REQUIRED field [payment_method_id] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.payment_status` | new REQUIRED field [payment_status] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.po_number` | new REQUIRED field [po_number] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.review_note` | new REQUIRED field [review_note] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.review_status` | new REQUIRED field [review_status] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.supplier_id` | new REQUIRED field [supplier_id] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.supplier_name` | new REQUIRED field [supplier_name] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.total` | new REQUIRED field [total] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.uploaded_by` | new REQUIRED field [uploaded_by] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.vat` | new REQUIRED field [vat] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.vendor` | new REQUIRED field [vendor] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.version` | new REQUIRED field [version] |
| `response_schema_field_became_required` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary` | field [summary] became required |
| `response_schema_type_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.amount` | new REQUIRED field [amount] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branch` | new REQUIRED field [branch] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branch_id` | new REQUIRED field [branch_id] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.category` | new REQUIRED field [category] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.category_id` | new REQUIRED field [category_id] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.date` | new REQUIRED field [date] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.description` | new REQUIRED field [description] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.due_date` | new REQUIRED field [due_date] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.file_name` | new REQUIRED field [file_name] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.file_url` | new REQUIRED field [file_url] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.from_purchase` | new REQUIRED field [from_purchase] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.number` | new REQUIRED field [number] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.operation_type` | new REQUIRED field [operation_type] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.paid` | new REQUIRED field [paid] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.payment_method` | new REQUIRED field [payment_method] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.payment_method_id` | new REQUIRED field [payment_method_id] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.payment_status` | new REQUIRED field [payment_status] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.po_number` | new REQUIRED field [po_number] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.review_note` | new REQUIRED field [review_note] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.review_status` | new REQUIRED field [review_status] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.supplier_id` | new REQUIRED field [supplier_id] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.supplier_name` | new REQUIRED field [supplier_name] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total` | new REQUIRED field [total] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.uploaded_by` | new REQUIRED field [uploaded_by] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.vat` | new REQUIRED field [vat] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.vendor` | new REQUIRED field [vendor] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.version` | new REQUIRED field [version] |
| `request_media_type_added` | `paths./api/owner/expenses/expenses/documents.post.requestBody.content.multipart/form-data` | request media type [multipart/form-data] added |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expenses/documents.post.responses.201.content.application/json.schema.properties.data.properties.fields` | new REQUIRED field [fields] |
| `response_schema_required_field_added` | `paths./api/owner/expenses/expenses/documents.post.responses.202.content.application/json.schema.properties.data.properties.fields` | new REQUIRED field [fields] |
| `response_schema_type_added` | `paths./api/owner/forms/form-options/purchases.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches.items` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/owner/forms/form-options/purchases.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches.items.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/owner/forms/form-options/purchases.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches.items.properties.is_active` | new REQUIRED field [is_active] |
| `response_schema_required_field_added` | `paths./api/owner/forms/form-options/purchases.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches.items.properties.name` | new REQUIRED field [name] |
| `response_schema_type_added` | `paths./api/owner/forms/form-options/purchases.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items` | type added (any -> ['object']) |
| `response_schema_type_added` | `paths./api/owner/forms/form-options/purchases.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.suppliers.items` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/owner/forms/form-options/purchases.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.suppliers.items.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/owner/forms/form-options/purchases.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.suppliers.items.properties.items` | new REQUIRED field [items] |
| `response_schema_required_field_added` | `paths./api/owner/forms/form-options/purchases.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.suppliers.items.properties.name` | new REQUIRED field [name] |
| `response_schema_required_field_added` | `paths./api/owner/forms/form-options/purchases.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.suppliers.items.properties.person` | new REQUIRED field [person] |
| `response_schema_required_field_added` | `paths./api/owner/forms/form-options/purchases.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.suppliers.items.properties.whatsapp` | new REQUIRED field [whatsapp] |
| `operation_added` | `paths./api/owner/general/account/subscription/payments/{reference}/proof.post` | POST /api/owner/general/account/subscription/payments/{reference}/proof added to the contract |
| `response_schema_type_added` | `paths./api/owner/inventory/catalog/products/{productReference}/recipe-components.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.components.items.properties.item_name` | type added (any -> ['null', 'string']) |
| `response_schema_type_added` | `paths./api/owner/inventory/catalog/products/{productReference}/recipe-components.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.components.items.properties.unit` | type added (any -> ['null', 'string']) |
| `response_schema_type_added` | `paths./api/owner/inventory/catalog/products/{productReference}/recipe-components.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/owner/inventory/catalog/products/{productReference}/recipe-components.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.code` | new REQUIRED field [code] |
| `response_schema_required_field_added` | `paths./api/owner/inventory/catalog/products/{productReference}/recipe-components.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/owner/inventory/catalog/products/{productReference}/recipe-components.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.name` | new REQUIRED field [name] |
| `response_schema_required_field_added` | `paths./api/owner/inventory/catalog/products/{productReference}/recipe-components.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.unit` | new REQUIRED field [unit] |
| `optional_parameter_added` | `paths./api/owner/inventory/inventory/items.get.parameters.all` | optional parameter [all] (in query) added |
| `optional_parameter_added` | `paths./api/owner/inventory/inventory/items.get.parameters.fields` | optional parameter [fields] (in query) added |
| `response_schema_type_added` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items` | type added (any -> ['object']) |
| `response_schema_type_added` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.current_page` | type added (any -> ['integer']) |
| `response_schema_type_added` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.last_page` | type added (any -> ['integer']) |
| `response_schema_required_field_added` | `paths./api/owner/inventory/inventory/items/{item}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.moves` | new REQUIRED field [moves] |
| `response_schema_required_field_added` | `paths./api/owner/inventory/inventory/items/{item}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.usage` | new REQUIRED field [usage] |
| `response_schema_type_added` | `paths./api/owner/inventory/waste/analytics.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches.items` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/owner/inventory/waste/analytics.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches.items.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/owner/inventory/waste/analytics.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches.items.properties.name` | new REQUIRED field [name] |
| `response_schema_type_added` | `paths./api/owner/inventory/waste/analytics.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.records.items.properties.branch` | type added (any -> ['null', 'string']) |
| `response_schema_type_added` | `paths./api/owner/inventory/waste/analytics.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.records.items.properties.branch_id` | type added (any -> ['null', 'string']) |
| `response_schema_required_field_added` | `paths./api/owner/meetings/meetings/{meetingReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.accountant` | new REQUIRED field [accountant] |
| `response_schema_required_field_added` | `paths./api/owner/meetings/meetings/{meetingReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.can_cancel` | new REQUIRED field [can_cancel] |
| `response_schema_required_field_added` | `paths./api/owner/meetings/meetings/{meetingReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.can_edit` | new REQUIRED field [can_edit] |
| `response_schema_required_field_added` | `paths./api/owner/meetings/meetings/{meetingReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.cancellation_reason` | new REQUIRED field [cancellation_reason] |
| `response_schema_required_field_added` | `paths./api/owner/meetings/meetings/{meetingReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.created_at` | new REQUIRED field [created_at] |
| `response_schema_required_field_added` | `paths./api/owner/meetings/meetings/{meetingReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.date` | new REQUIRED field [date] |
| `response_schema_required_field_added` | `paths./api/owner/meetings/meetings/{meetingReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/owner/meetings/meetings/{meetingReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meet_link` | new REQUIRED field [meet_link] |
| `response_schema_required_field_added` | `paths./api/owner/meetings/meetings/{meetingReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.notes` | new REQUIRED field [notes] |
| `response_schema_required_field_added` | `paths./api/owner/meetings/meetings/{meetingReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | new REQUIRED field [status] |
| `response_schema_required_field_added` | `paths./api/owner/meetings/meetings/{meetingReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subject` | new REQUIRED field [subject] |
| `response_schema_required_field_added` | `paths./api/owner/meetings/meetings/{meetingReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.time` | new REQUIRED field [time] |
| `response_schema_required_field_added` | `paths./api/owner/meetings/meetings/{meetingReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.updated_at` | new REQUIRED field [updated_at] |
| `response_schema_required_field_added` | `paths./api/owner/payroll/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.file_url` | new REQUIRED field [file_url] |
| `optional_parameter_added` | `paths./api/owner/payroll/payroll/employees.get.parameters.per_page` | optional parameter [per_page] (in query) added |
| `optional_parameter_added` | `paths./api/owner/payroll/payroll/employees.get.parameters.search` | optional parameter [search] (in query) added |
| `optional_parameter_added` | `paths./api/owner/payroll/payroll/employees.get.parameters.status` | optional parameter [status] (in query) added |
| `response_schema_type_added` | `paths./api/owner/payroll/payroll/employees/{publicReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches.items` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/owner/payroll/payroll/employees/{publicReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches.items.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/owner/payroll/payroll/employees/{publicReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches.items.properties.name` | new REQUIRED field [name] |
| `request_schema_enum_removed` | `paths./api/owner/payroll/payroll/employees/{publicReference}/action.post.requestBody.content.application/json.schema.properties.action` | enum constraint removed |
| `request_schema_field_added` | `paths./api/owner/payroll/payroll/employees/{publicReference}/action.post.requestBody.content.application/json.schema.properties.amount` | new optional field [amount] |
| `request_schema_field_added` | `paths./api/owner/payroll/payroll/employees/{publicReference}/action.post.requestBody.content.application/json.schema.properties.base_salary` | new optional field [base_salary] |
| `request_schema_field_added` | `paths./api/owner/payroll/payroll/employees/{publicReference}/action.post.requestBody.content.application/json.schema.properties.branch_id` | new optional field [branch_id] |
| `request_schema_field_added` | `paths./api/owner/payroll/payroll/employees/{publicReference}/action.post.requestBody.content.application/json.schema.properties.date` | new optional field [date] |
| `request_schema_field_added` | `paths./api/owner/payroll/payroll/employees/{publicReference}/action.post.requestBody.content.application/json.schema.properties.days` | new optional field [days] |
| `request_schema_field_added` | `paths./api/owner/payroll/payroll/employees/{publicReference}/action.post.requestBody.content.application/json.schema.properties.effective_from` | new optional field [effective_from] |
| `request_schema_field_added` | `paths./api/owner/payroll/payroll/employees/{publicReference}/action.post.requestBody.content.application/json.schema.properties.holder` | new optional field [holder] |
| `request_schema_field_added` | `paths./api/owner/payroll/payroll/employees/{publicReference}/action.post.requestBody.content.application/json.schema.properties.hours` | new optional field [hours] |
| `request_schema_field_added` | `paths./api/owner/payroll/payroll/employees/{publicReference}/action.post.requestBody.content.application/json.schema.properties.iban` | new optional field [iban] |
| `request_schema_field_added` | `paths./api/owner/payroll/payroll/employees/{publicReference}/action.post.requestBody.content.application/json.schema.properties.note` | new optional field [note] |
| `request_schema_field_added` | `paths./api/owner/payroll/payroll/employees/{publicReference}/action.post.requestBody.content.application/json.schema.properties.reason` | new optional field [reason] |
| `request_schema_field_added` | `paths./api/owner/payroll/payroll/employees/{publicReference}/action.post.requestBody.content.application/json.schema.properties.type` | new optional field [type] |
| `request_schema_field_added` | `paths./api/owner/payroll/payroll/employees/{publicReference}/action.post.requestBody.content.application/json.schema.properties.version` | new optional field [version] |
| `response_schema_required_field_added` | `paths./api/owner/payroll/payroll/runs.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.runs` | new REQUIRED field [runs] |
| `response_status_added` | `paths./api/owner/payroll/payroll/runs.post.responses.200` | response [200] added to the contract |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.accountant` | new REQUIRED field [accountant] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.current_price` | new REQUIRED field [current_price] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.date` | new REQUIRED field [date] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.final_price` | new REQUIRED field [final_price] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.materials.items.properties.cost` | new REQUIRED field [cost] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.materials.items.properties.name` | new REQUIRED field [name] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.materials.items.properties.supplier` | new REQUIRED field [supplier] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.materials.items.properties.unit` | new REQUIRED field [unit] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.materials.items.properties.unit_price` | new REQUIRED field [unit_price] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.materials_cost` | new REQUIRED field [materials_cost] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.operating_cost` | new REQUIRED field [operating_cost] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.operating_items.items.properties.name` | new REQUIRED field [name] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.operating_items.items.properties.per_unit` | new REQUIRED field [per_unit] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.product` | new REQUIRED field [product] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.status` | new REQUIRED field [status] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.suggested_price` | new REQUIRED field [suggested_price] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.waste_note` | new REQUIRED field [waste_note] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.waste_percent` | new REQUIRED field [waste_percent] |
| `response_schema_nullability_removed` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | type no longer accepts/returns null |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.accountant` | new REQUIRED field [accountant] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.approved_at` | new REQUIRED field [approved_at] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.current_price` | new REQUIRED field [current_price] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.date` | new REQUIRED field [date] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.final_price` | new REQUIRED field [final_price] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.materials` | new REQUIRED field [materials] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.materials_cost` | new REQUIRED field [materials_cost] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.operating_cost` | new REQUIRED field [operating_cost] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.operating_items` | new REQUIRED field [operating_items] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.product` | new REQUIRED field [product] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | new REQUIRED field [status] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.suggested_price` | new REQUIRED field [suggested_price] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total_cost` | new REQUIRED field [total_cost] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.version` | new REQUIRED field [version] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.waste_note` | new REQUIRED field [waste_note] |
| `response_schema_required_field_added` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.waste_percent` | new REQUIRED field [waste_percent] |
| `operation_added` | `paths./api/owner/purchases/direct-purchases.get` | GET /api/owner/purchases/direct-purchases added to the contract |
| `operation_added` | `paths./api/owner/purchases/direct-purchases.post` | POST /api/owner/purchases/direct-purchases added to the contract |
| `operation_added` | `paths./api/owner/purchases/direct-purchases/{reference}.get` | GET /api/owner/purchases/direct-purchases/{reference} added to the contract |
| `operation_added` | `paths./api/owner/purchases/direct-purchases/{reference}/cancel.post` | POST /api/owner/purchases/direct-purchases/{reference}/cancel added to the contract |
| `operation_added` | `paths./api/owner/purchases/direct-purchases/{reference}/complete.post` | POST /api/owner/purchases/direct-purchases/{reference}/complete added to the contract |
| `response_schema_type_added` | `paths./api/owner/purchases/purchase-orders.get.responses.200.content.application/json.schema.allOf[1].properties.data` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/owner/purchases/purchase-orders.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | new REQUIRED field [items] |
| `response_schema_required_field_added` | `paths./api/owner/purchases/purchase-orders.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.low_stock` | new REQUIRED field [low_stock] |
| `response_schema_required_field_added` | `paths./api/owner/purchases/purchase-orders.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta` | new REQUIRED field [meta] |
| `response_schema_required_field_added` | `paths./api/owner/purchases/purchase-orders.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary` | new REQUIRED field [summary] |
| `response_schema_type_added` | `paths./api/owner/purchases/purchase-orders/generate.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/owner/purchases/purchase-orders/generate.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/owner/purchases/purchase-orders/generate.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.number` | new REQUIRED field [number] |
| `response_schema_required_field_added` | `paths./api/owner/purchases/purchase-orders/generate.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.po_number` | new REQUIRED field [po_number] |
| `response_schema_required_field_added` | `paths./api/owner/purchases/purchase-orders/generate.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.reference` | new REQUIRED field [reference] |
| `response_schema_type_added` | `paths./api/owner/purchases/purchase-orders/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/owner/purchases/purchase-orders/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branch_id` | new REQUIRED field [branch_id] |
| `response_schema_required_field_added` | `paths./api/owner/purchases/purchase-orders/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branch_name` | new REQUIRED field [branch_name] |
| `response_schema_required_field_added` | `paths./api/owner/purchases/purchase-orders/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.cancel_reason` | new REQUIRED field [cancel_reason] |
| `response_schema_required_field_added` | `paths./api/owner/purchases/purchase-orders/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.date` | new REQUIRED field [date] |
| `response_schema_required_field_added` | `paths./api/owner/purchases/purchase-orders/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.expected_date` | new REQUIRED field [expected_date] |
| `response_schema_required_field_added` | `paths./api/owner/purchases/purchase-orders/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/owner/purchases/purchase-orders/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.invoice` | new REQUIRED field [invoice] |
| `response_schema_required_field_added` | `paths./api/owner/purchases/purchase-orders/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.lines` | new REQUIRED field [lines] |
| `response_schema_required_field_added` | `paths./api/owner/purchases/purchase-orders/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.notes` | new REQUIRED field [notes] |
| `response_schema_required_field_added` | `paths./api/owner/purchases/purchase-orders/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.number` | new REQUIRED field [number] |
| `response_schema_required_field_added` | `paths./api/owner/purchases/purchase-orders/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.received_date` | new REQUIRED field [received_date] |
| `response_schema_required_field_added` | `paths./api/owner/purchases/purchase-orders/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.sent_at` | new REQUIRED field [sent_at] |
| `response_schema_required_field_added` | `paths./api/owner/purchases/purchase-orders/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | new REQUIRED field [status] |
| `response_schema_required_field_added` | `paths./api/owner/purchases/purchase-orders/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.supplier` | new REQUIRED field [supplier] |
| `response_schema_required_field_added` | `paths./api/owner/purchases/purchase-orders/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total` | new REQUIRED field [total] |
| `response_schema_required_field_added` | `paths./api/owner/purchases/purchase-orders/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.type` | new REQUIRED field [type] |
| `optional_parameter_added` | `paths./api/owner/purchases/suppliers.get.parameters.classification` | optional parameter [classification] (in query) added |
| `response_schema_type_added` | `paths./api/owner/purchases/suppliers.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.suppliers.items.properties.items.items.properties.name` | type added (any -> ['null', 'string']) |
| `request_schema_type_removed` | `paths./api/owner/purchases/suppliers/pay.post.requestBody.content.multipart/form-data.schema` | type removed (['object'] -> any) |
| `request_body_became_optional` | `paths./api/owner/purchases/suppliers/pay.post.requestBody.required` | request body became optional |
| `operation_added` | `paths./api/owner/purchases/suppliers/payment-scan.post` | POST /api/owner/purchases/suppliers/payment-scan added to the contract |
| `response_schema_type_added` | `paths./api/owner/purchases/suppliers/{id}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.name` | type added (any -> ['null', 'string']) |
| `operation_added` | `paths./api/owner/purchases/suppliers/{id}/convert-to-permanent.post` | POST /api/owner/purchases/suppliers/{id}/convert-to-permanent added to the contract |
| `response_schema_required_field_added` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.accountant` | new REQUIRED field [accountant] |
| `response_schema_required_field_added` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.extras` | new REQUIRED field [extras] |
| `response_schema_required_field_added` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.file_url` | new REQUIRED field [file_url] |
| `response_schema_required_field_added` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.hero` | new REQUIRED field [hero] |
| `response_schema_required_field_added` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.issued_at` | new REQUIRED field [issued_at] |
| `response_schema_required_field_added` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.months` | new REQUIRED field [months] |
| `response_schema_required_field_added` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.period_label` | new REQUIRED field [period_label] |
| `response_schema_required_field_added` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.tables` | new REQUIRED field [tables] |
| `response_schema_type_added` | `paths./api/owner/reports/owner/reporting/financial.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches.items` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/owner/reports/owner/reporting/financial.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches.items.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/owner/reports/owner/reporting/financial.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches.items.properties.name` | new REQUIRED field [name] |
| `response_schema_required_field_added` | `paths./api/owner/reports/statements/export-bundle.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.error` | new REQUIRED field [error] |
| `response_schema_required_field_added` | `paths./api/owner/reports/statements/export-bundle.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.expires_at` | new REQUIRED field [expires_at] |
| `response_schema_required_field_added` | `paths./api/owner/reports/statements/export-bundle.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.file_url` | new REQUIRED field [file_url] |
| `response_schema_required_field_added` | `paths./api/owner/reports/statements/export-bundle.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.format` | new REQUIRED field [format] |
| `response_schema_required_field_added` | `paths./api/owner/reports/statements/export-bundle.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/owner/reports/statements/export-bundle.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.reports` | new REQUIRED field [reports] |
| `response_schema_required_field_added` | `paths./api/owner/reports/statements/export-bundle.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | new REQUIRED field [status] |
| `response_schema_type_added` | `paths./api/owner/reports/statements/export.get.responses.200.content.application/json.schema.allOf[1].properties.data` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/owner/reports/statements/export.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.file_url` | new REQUIRED field [file_url] |
| `operation_added` | `paths./api/owner/sales/invoices/collection-scan.post` | POST /api/owner/sales/invoices/collection-scan added to the contract |
| `response_status_added` | `paths./api/owner/settings/branches.post.responses.200` | response [200] added to the contract |
| `response_schema_required_field_added` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.address` | new REQUIRED field [address] |
| `response_schema_required_field_added` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.city` | new REQUIRED field [city] |
| `response_schema_required_field_added` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.city_id` | new REQUIRED field [city_id] |
| `response_schema_required_field_added` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.code` | new REQUIRED field [code] |
| `response_schema_required_field_added` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.created_at` | new REQUIRED field [created_at] |
| `response_schema_required_field_added` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.email` | new REQUIRED field [email] |
| `response_schema_required_field_added` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.is_active` | new REQUIRED field [is_active] |
| `response_schema_required_field_added` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.is_main` | new REQUIRED field [is_main] |
| `response_schema_required_field_added` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.manager` | new REQUIRED field [manager] |
| `response_schema_required_field_added` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.name` | new REQUIRED field [name] |
| `response_schema_required_field_added` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.operations_count` | new REQUIRED field [operations_count] |
| `response_schema_required_field_added` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.phone` | new REQUIRED field [phone] |
| `response_schema_required_field_added` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.public_reference` | new REQUIRED field [public_reference] |
| `response_schema_required_field_added` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.short_name` | new REQUIRED field [short_name] |
| `response_schema_required_field_added` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.staff_count` | new REQUIRED field [staff_count] |
| `response_schema_required_field_added` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | new REQUIRED field [status] |
| `response_schema_required_field_added` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.version` | new REQUIRED field [version] |
| `response_schema_type_added` | `paths./api/owner/settings/organizations/current.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.log.items.properties.by` | type added (any -> ['null', 'string']) |
| `response_schema_field_added` | `paths./api/owner/summary/more/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.account` | new optional field [account] |
| `response_schema_field_added` | `paths./api/owner/summary/more/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.app_settings` | new optional field [app_settings] |
| `response_schema_field_added` | `paths./api/owner/summary/more/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.assets` | new optional field [assets] |
| `response_schema_field_added` | `paths./api/owner/summary/more/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branches` | new optional field [branches] |
| `response_schema_field_added` | `paths./api/owner/summary/more/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.business_settings` | new optional field [business_settings] |
| `response_schema_field_added` | `paths./api/owner/summary/more/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.customers` | new optional field [customers] |
| `response_schema_field_added` | `paths./api/owner/summary/more/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.expenses` | new optional field [expenses] |
| `response_schema_field_added` | `paths./api/owner/summary/more/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meetings` | new optional field [meetings] |

_… and 448 more (see the JSON report)._

## Documentation-only changes (222)

| Kind | Location | Detail |
|---|---|---|
| `component_schema_documentation` | `components.schemas.UploadRegistrationPaymentProofRequest` | description changed |
| `operation_documentation` | `paths./api/accountant/inventory/inventory/items.get.summary` | summary changed |
| `operation_documentation` | `paths./api/accountant/reports/statements/export-bundle.post.summary` | summary changed |
| `operation_documentation` | `paths./api/accountant/reports/statements/export-bundle/{bundleId}.get.summary` | summary changed |
| `operation_documentation` | `paths./api/accountant/reports/statements/export.get.summary` | summary changed |
| `operation_documentation` | `paths./api/auth/accountant-reports.get.summary` | summary changed |
| `operation_documentation` | `paths./api/auth/accountant-reports/{reportId}.get.summary` | summary changed |
| `response_status_added` | `paths./api/auth/accounting/journal-entries.get.responses.422` | response [422] added to the contract |
| `operation_documentation` | `paths./api/auth/onboarding/applications/recover/verify.post.description` | description changed |
| `operation_documentation` | `paths./api/auth/onboarding/applications/{reference}/subscription-summary.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/owner/accounting/accounts.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/owner/accounting/accounts.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/owner/accounting/accounts.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/owner/accounting/assets.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/owner/accounting/assets.get.responses.200.description` | response description changed |
| `response_status_added` | `paths./api/owner/accounting/assets.get.responses.422` | response [422] added to the contract |
| `operation_extension_changed` | `paths./api/owner/accounting/assets.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/owner/accounting/assets/{asset}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/owner/accounting/assets/{asset}.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/owner/accounting/assets/{asset}.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/owner/accounting/financial-statements.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/owner/accounting/financial-statements.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/owner/accounting/financial-statements.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/owner/accounting/financial-statements/{statement}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/owner/accounting/financial-statements/{statement}.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/owner/accounting/financial-statements/{statement}.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/owner/accounting/general-ledger.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/owner/accounting/journal-book.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_reference_shape` | `paths./api/owner/accounting/journal-book.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/owner/accounting/journal-book.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.current_page` | examples changed |
| `response_schema_documentation` | `paths./api/owner/accounting/journal-book.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.last_page` | examples changed |
| `response_schema_documentation` | `paths./api/owner/accounting/journal-book.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.total` | examples changed |
| `response_schema_documentation` | `paths./api/owner/accounting/journal-book.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.total` | description changed |
| `response_description_changed` | `paths./api/owner/accounting/journal-book.get.responses.200.description` | response description changed |
| `response_status_added` | `paths./api/owner/accounting/journal-book.get.responses.422` | response [422] added to the contract |
| `operation_extension_changed` | `paths./api/owner/accounting/journal-book.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/owner/accounting/journal-book/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/owner/accounting/journal-book/{reference}.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/owner/accounting/journal-book/{reference}.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/owner/accounting/reports/trial-balance.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/owner/accounting/reports/trial-balance.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/owner/accounting/reports/trial-balance.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/owner/dashboard/owner.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_documentation` | `paths./api/owner/expenses/expense-analysis.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_reference_shape` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.current_page` | examples changed |
| `response_schema_documentation` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.last_page` | examples changed |
| `response_schema_documentation` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.total` | examples changed |
| `response_schema_documentation` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.total` | description changed |
| `response_description_changed` | `paths./api/owner/expenses/expense-register.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/owner/expenses/expense-register.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/owner/expenses/expense-register/{reference}.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/owner/expenses/expense-register/{reference}.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `operation_documentation` | `paths./api/owner/forms/form-options/purchases.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/owner/inventory/catalog/products/{productReference}/recipe-components.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_documentation` | `paths./api/owner/inventory/inventory/items.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/owner/inventory/waste/analytics.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_documentation` | `paths./api/owner/payroll/payroll-runs/{runId}/export-payment-file.post.summary` | summary changed |
| `response_status_added` | `paths./api/owner/payroll/payroll/employees.get.responses.422` | response [422] added to the contract |
| `response_schema_documentation` | `paths./api/owner/payroll/payroll/employees/{publicReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `request_schema_documentation` | `paths./api/owner/payroll/payroll/employees/{publicReference}/action.post.requestBody.content.application/json.schema.properties.action` | description changed |
| `operation_documentation` | `paths./api/owner/payroll/payroll/run.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/owner/payroll/payroll/runs.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/owner/payroll/payroll/runs.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/owner/payroll/payroll/runs.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `operation_documentation` | `paths./api/owner/payroll/payroll/runs.post.summary` | summary changed |
| `response_schema_documentation` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_reference_shape` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.current_page` | examples changed |
| `response_schema_documentation` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.last_page` | examples changed |
| `response_schema_documentation` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.total` | examples changed |
| `response_schema_documentation` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.total` | description changed |
| `response_description_changed` | `paths./api/owner/pricing/pricing/register.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/owner/pricing/pricing/register.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/owner/purchases/purchase-orders.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/owner/purchases/purchase-orders.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/owner/purchases/purchase-orders.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `operation_documentation` | `paths./api/owner/purchases/purchase-orders.post.summary` | summary changed |
| `operation_documentation` | `paths./api/owner/purchases/purchase-orders/generate.post.summary` | summary changed |
| `response_schema_documentation` | `paths./api/owner/purchases/purchase-orders/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/owner/purchases/purchase-orders/{reference}.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/owner/purchases/purchase-orders/{reference}.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `operation_documentation` | `paths./api/owner/purchases/purchase-orders/{reference}/supplier-invoice.post.summary` | summary changed |
| `response_schema_documentation` | `paths./api/owner/purchases/suppliers.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `request_schema_documentation` | `paths./api/owner/purchases/suppliers/pay.post.requestBody.content.multipart/form-data.schema` | description changed |
| `request_schema_documentation` | `paths./api/owner/purchases/suppliers/pay.post.requestBody.content.multipart/form-data.schema` | title changed |
| `request_schema_reference_shape` | `paths./api/owner/purchases/suppliers/pay.post.requestBody.content.multipart/form-data.schema` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/owner/purchases/suppliers/{id}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/owner/reports/owner/reporting/financial.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_documentation` | `paths./api/owner/reports/statements/export-bundle.post.summary` | summary changed |
| `operation_documentation` | `paths./api/owner/reports/statements/export-bundle/{bundleId}.get.summary` | summary changed |
| `operation_documentation` | `paths./api/owner/reports/statements/export.get.summary` | summary changed |
| `operation_documentation` | `paths./api/owner/settings/branches.post.summary` | summary changed |
| `operation_documentation` | `paths./api/owner/settings/branches/{reference}.put.summary` | summary changed |
| `response_schema_documentation` | `paths./api/owner/settings/organizations/current.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_documentation` | `paths./api/owner/summary/more/summary.get.summary` | summary changed |
| `operation_documentation` | `paths./api/owner/tax/tax/documents/upload.post.summary` | summary changed |
| `operation_documentation` | `paths./api/owner/tax/tax/vat-returns/export.post.summary` | summary changed |
| `response_schema_documentation` | `paths./api/owner/tax/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/owner/tax/tax/vat-returns/summary.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/owner/tax/tax/vat-returns/summary.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/owner/tax/zakat/sessions/{uuid}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/owner/tax/zakat/sessions/{uuid}.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/owner/tax/zakat/sessions/{uuid}.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `operation_documentation` | `paths./api/v1/accountant-reports.get.summary` | summary changed |
| `operation_documentation` | `paths./api/v1/accountant-reports/{reportId}.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/v1/accounting/financial-statements.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/v1/accounting/financial-statements.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/v1/accounting/financial-statements.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/v1/accounting/financial-statements/{statement}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/v1/accounting/financial-statements/{statement}.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/v1/accounting/financial-statements/{statement}.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/v1/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_reference_shape` | `paths./api/v1/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/v1/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.current_page` | examples changed |
| `response_schema_documentation` | `paths./api/v1/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.last_page` | examples changed |
| `response_schema_documentation` | `paths./api/v1/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.total` | examples changed |
| `response_schema_documentation` | `paths./api/v1/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.total` | description changed |
| `response_description_changed` | `paths./api/v1/accounting/journal-entries.get.responses.200.description` | response description changed |
| `response_status_added` | `paths./api/v1/accounting/journal-entries.get.responses.422` | response [422] added to the contract |
| `operation_extension_changed` | `paths./api/v1/accounting/journal-entries.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/v1/accounting/journal-entries/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/v1/accounting/journal-entries/{reference}.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/v1/accounting/journal-entries/{reference}.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/v1/accounting/reports/trial-balance.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/v1/accounting/reports/trial-balance.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/v1/accounting/reports/trial-balance.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/v1/accounts.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/v1/accounts.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/v1/accounts.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/v1/assets.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/v1/assets.get.responses.200.description` | response description changed |
| `response_status_added` | `paths./api/v1/assets.get.responses.422` | response [422] added to the contract |
| `operation_extension_changed` | `paths./api/v1/assets.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/v1/assets/{asset}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/v1/assets/{asset}.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/v1/assets/{asset}.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `operation_documentation` | `paths./api/v1/branches.post.summary` | summary changed |
| `operation_documentation` | `paths./api/v1/branches/{reference}.put.summary` | summary changed |
| `response_schema_documentation` | `paths./api/v1/catalog/products/{productReference}/recipe-components.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/v1/dashboards/owner.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `request_schema_documentation` | `paths./api/v1/erp/onboarding/applications/{reference}/package.put.requestBody.content.application/json.schema.properties.package_id` | description changed |
| `response_schema_documentation` | `paths./api/v1/erp/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/v1/erp/onboarding/applications/{reference}/subscription-summary.get.responses.200.description` | response description changed |
| `operation_documentation` | `paths./api/v1/erp/onboarding/applications/{reference}/subscription-summary.get.summary` | summary changed |
| `operation_extension_changed` | `paths./api/v1/erp/onboarding/applications/{reference}/subscription-summary.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `operation_documentation` | `paths./api/v1/expense-analysis.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/v1/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_reference_shape` | `paths./api/v1/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/v1/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.current_page` | examples changed |
| `response_schema_documentation` | `paths./api/v1/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.last_page` | examples changed |
| `response_schema_documentation` | `paths./api/v1/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.total` | examples changed |
| `response_schema_documentation` | `paths./api/v1/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.total` | description changed |
| `response_description_changed` | `paths./api/v1/expense-register.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/v1/expense-register.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/v1/expense-register/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/v1/expense-register/{reference}.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/v1/expense-register/{reference}.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `operation_documentation` | `paths./api/v1/form-options/purchases.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/v1/general-ledger.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_documentation` | `paths./api/v1/inventory/items.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/v1/monthly-reports/{reportId}.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `operation_documentation` | `paths./api/v1/more/summary.get.summary` | summary changed |
| `operation_documentation` | `paths./api/v1/onboarding/applications/recover/verify.post.description` | description changed |
| `response_schema_documentation` | `paths./api/v1/organizations/current.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/v1/owner/reporting/financial.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_documentation` | `paths./api/v1/payroll-runs/{runId}/export-payment-file.post.summary` | summary changed |
| `response_status_added` | `paths./api/v1/payroll/employees.get.responses.422` | response [422] added to the contract |
| `response_schema_documentation` | `paths./api/v1/payroll/employees/{publicReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `request_schema_documentation` | `paths./api/v1/payroll/employees/{publicReference}/action.post.requestBody.content.application/json.schema.properties.action` | description changed |
| `operation_documentation` | `paths./api/v1/payroll/run.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/v1/payroll/runs.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/v1/payroll/runs.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/v1/payroll/runs.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `operation_documentation` | `paths./api/v1/payroll/runs.post.summary` | summary changed |
| `response_schema_documentation` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_reference_shape` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.current_page` | examples changed |
| `response_schema_documentation` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.last_page` | examples changed |
| `response_schema_documentation` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.total` | examples changed |
| `response_schema_documentation` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.total` | description changed |
| `response_description_changed` | `paths./api/v1/pricing/register.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/v1/pricing/register.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/v1/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/v1/pricing/register/{product_reference}.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/v1/pricing/register/{product_reference}.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/v1/purchase-orders.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/v1/purchase-orders.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/v1/purchase-orders.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `operation_documentation` | `paths./api/v1/purchase-orders.post.summary` | summary changed |
| `operation_documentation` | `paths./api/v1/purchase-orders/generate.post.summary` | summary changed |
| `response_schema_documentation` | `paths./api/v1/purchase-orders/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/v1/purchase-orders/{reference}.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/v1/purchase-orders/{reference}.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `operation_documentation` | `paths./api/v1/purchase-orders/{reference}/supplier-invoice.post.summary` | summary changed |
| `operation_documentation` | `paths./api/v1/statements/export-bundle.post.summary` | summary changed |
| `operation_documentation` | `paths./api/v1/statements/export-bundle/{bundleId}.get.summary` | summary changed |
| `operation_documentation` | `paths./api/v1/statements/export.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/v1/suppliers.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `request_schema_documentation` | `paths./api/v1/suppliers/pay.post.requestBody.content.multipart/form-data.schema` | description changed |
| `request_schema_documentation` | `paths./api/v1/suppliers/pay.post.requestBody.content.multipart/form-data.schema` | title changed |
| `request_schema_reference_shape` | `paths./api/v1/suppliers/pay.post.requestBody.content.multipart/form-data.schema` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/v1/suppliers/{id}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_documentation` | `paths./api/v1/tax/documents/upload.post.summary` | summary changed |
| `operation_documentation` | `paths./api/v1/tax/vat-returns/export.post.summary` | summary changed |
| `response_schema_documentation` | `paths./api/v1/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/v1/tax/vat-returns/summary.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/v1/tax/vat-returns/summary.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/v1/waste/analytics.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/v1/zakat/sessions/{uuid}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/v1/zakat/sessions/{uuid}.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/v1/zakat/sessions/{uuid}.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |

> **Fail closed:** unclassified changes require an explicit
> compatibility decision before this contract may be approved.

