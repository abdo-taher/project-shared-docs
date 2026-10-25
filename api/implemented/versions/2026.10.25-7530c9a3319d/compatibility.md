# OpenAPI Contract Compatibility Report

- Baseline: `published 2026.10.21-6846e086006f` (1244 operations)
- Candidate: `build cb85f7b33756` (1264 operations)
- Generated: 2026-10-25T13:12:08.674874+00:00

## Summary

| Category | Count |
|---|---|
| BREAKING | 8 |
| UNKNOWN | 0 |
| NON_BREAKING | 89 |
| DOCUMENTATION_ONLY | 23 |
| **total** | **120** |

## Breaking changes (8)

| Kind | Location | Detail |
|---|---|---|
| `component_schema_pattern_added` | `components.schemas.VerifyMobileRequest.properties.otp` | pattern added |
| `response_media_type_removed` | `paths./api/accountant/meetings/meetings/{meetingReference}/join.get.responses.200.content.application/json` | response media type [application/json] removed |
| `response_media_type_removed` | `paths./api/auth/accountant/meetings/{meetingReference}/join.get.responses.200.content.application/json` | response media type [application/json] removed |
| `response_media_type_removed` | `paths./api/owner/meetings/meetings/{meetingReference}/join.get.responses.200.content.application/json` | response media type [application/json] removed |
| `response_schema_enum_value_added` | `paths./api/public/integrations/purchase-order-links/{token}.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.next_action` | response may now contain a value clients do not handle |
| `response_media_type_removed` | `paths./api/v1/accountant/meetings/{meetingReference}/join.get.responses.200.content.application/json` | response media type [application/json] removed |
| `response_schema_enum_value_added` | `paths./api/v1/integrations/purchase-order-links/{token}.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.next_action` | response may now contain a value clients do not handle |
| `response_media_type_removed` | `paths./api/v1/meetings/{meetingReference}/join.get.responses.200.content.application/json` | response media type [application/json] removed |

## Unclassified changes (fail closed) (0)

_None._

## Non-breaking changes (89)

| Kind | Location | Detail |
|---|---|---|
| `component_schema_const_added` | `components.schemas.AccountantDetailsResource.properties.task_metrics.anyOf[1].properties.delayed` | const added (value set narrowed to one value) |
| `component_schema_const_added` | `components.schemas.AccountantDetailsResource.properties.task_metrics.anyOf[1].properties.open` | const added (value set narrowed to one value) |
| `component_schema_field_became_optional` | `components.schemas.CreatePurchaseReturnRequest.properties.branch_id` | field [branch_id] became optional |
| `component_schema_nullability_added` | `components.schemas.CreatePurchaseReturnRequest.properties.branch_id` | type now also accepts/returns null |
| `component_schema_field_added` | `components.schemas.CreatePurchaseReturnRequest.properties.lines.items.properties.inventory_item_reference` | new optional field [inventory_item_reference] |
| `component_schema_field_added` | `components.schemas.CreatePurchaseReturnRequest.properties.supplier_invoice_reference` | new optional field [supplier_invoice_reference] |
| `component_schema_field_added` | `components.schemas.CreatePurchaseReturnRequest.properties.supplier_reference` | new optional field [supplier_reference] |
| `component_schema_field_added` | `components.schemas.CreateSalesAdjustmentNoteRequest.properties.sales_return_reference` | new optional field [sales_return_reference] |
| `component_schema_required_field_added` | `components.schemas.PurchaseReturnLine.properties.inventory_item_reference` | new REQUIRED field [inventory_item_reference] |
| `component_schema_required_field_added` | `components.schemas.PurchaseReturnLine.properties.item_name` | new REQUIRED field [item_name] |
| `component_schema_required_field_added` | `components.schemas.PurchaseReturnResource.properties.created_at` | new REQUIRED field [created_at] |
| `component_schema_required_field_added` | `components.schemas.PurchaseReturnResource.properties.public_reference` | new REQUIRED field [public_reference] |
| `component_schema_required_field_added` | `components.schemas.PurchaseReturnResource.properties.supplier_invoice_reference` | new REQUIRED field [supplier_invoice_reference] |
| `component_schema_required_field_added` | `components.schemas.PurchaseReturnResource.properties.supplier_name` | new REQUIRED field [supplier_name] |
| `component_schema_required_field_added` | `components.schemas.PurchaseReturnResource.properties.supplier_reference` | new REQUIRED field [supplier_reference] |
| `component_schema_required_field_added` | `components.schemas.SalesReturnResource.properties.credit_note` | new REQUIRED field [credit_note] |
| `component_schema_constraint_widened` | `components.schemas.VerifyMobileRequest.properties.otp` | [minLength] 6 -> None |
| `component_schema_constraint_widened` | `components.schemas.VerifyMobileRequest.properties.otp` | [maxLength] 6 -> None |
| `response_schema_const_added` | `paths./api/accountant/accounting/posting-requests/reprocess.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.outbox_claimed` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.available_count` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.low_count` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/accountant/purchases/purchase-orders.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.summary.properties.open_count` | const added (value set narrowed to one value) |
| `operation_added` | `paths./api/accountant/purchases/purchase-returns.get` | GET /api/accountant/purchases/purchase-returns added to the contract |
| `operation_added` | `paths./api/accountant/purchases/purchase-returns/{purchaseReturn}.get` | GET /api/accountant/purchases/purchase-returns/{purchaseReturn} added to the contract |
| `parameter_became_optional` | `paths./api/accountant/purchases/supplier-invoices.get.parameters.supplier_reference.required` | parameter [supplier_reference] became optional |
| `parameter_schema_nullability_added` | `paths./api/accountant/purchases/supplier-invoices.get.parameters.supplier_reference.schema` | type now also accepts/returns null |
| `response_schema_const_added` | `paths./api/accountant/sales/customers/{reference}/balance.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.summary.properties.overdue_invoice_count` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/accountant/sales/customers/{reference}/balance.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.summary.properties.paid_invoice_count` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/accountant/sales/customers/{reference}/balance.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.summary.properties.partially_paid_invoice_count` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/accountant/sales/customers/{reference}/balance.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.summary.properties.unpaid_invoice_count` | const added (value set narrowed to one value) |
| `operation_added` | `paths./api/accountant/sales/sales-returns.get` | GET /api/accountant/sales/sales-returns added to the contract |
| `operation_added` | `paths./api/accountant/sales/sales-returns/{publicReference}.get` | GET /api/accountant/sales/sales-returns/{publicReference} added to the contract |
| `operation_added` | `paths./api/accountant/tax/zakat/history.get` | GET /api/accountant/tax/zakat/history added to the contract |
| `operation_added` | `paths./api/accountant/tax/zakat/periods.get` | GET /api/accountant/tax/zakat/periods added to the contract |
| `operation_added` | `paths./api/accountant/tax/zakat/rates.get` | GET /api/accountant/tax/zakat/rates added to the contract |
| `operation_added` | `paths./api/accountant/tax/zakat/sessions/{uuid}.get` | GET /api/accountant/tax/zakat/sessions/{uuid} added to the contract |
| `response_schema_const_added` | `paths./api/admin/dashboard.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subscriptions_active_count` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/admin/dashboard.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subscriptions_expired_count` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/admin/dashboard.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subscriptions_near_renewal_count` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/auth/account.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[1].properties.subscription.properties.usage.prefixItems[0].properties.limit` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/auth/account.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[1].properties.subscription.properties.usage.prefixItems[1].properties.limit` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/owner/general/account/subscription.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[1].properties.subscription.properties.usage.prefixItems[0].properties.limit` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/owner/general/account/subscription.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[1].properties.subscription.properties.usage.prefixItems[1].properties.limit` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.available_count` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.low_count` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/owner/purchases/purchase-orders.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.summary.properties.open_count` | const added (value set narrowed to one value) |
| `operation_added` | `paths./api/owner/purchases/purchase-returns.get` | GET /api/owner/purchases/purchase-returns added to the contract |
| `operation_added` | `paths./api/owner/purchases/purchase-returns/{purchaseReturn}.get` | GET /api/owner/purchases/purchase-returns/{purchaseReturn} added to the contract |
| `parameter_became_optional` | `paths./api/owner/purchases/supplier-invoices.get.parameters.supplier_reference.required` | parameter [supplier_reference] became optional |
| `parameter_schema_nullability_added` | `paths./api/owner/purchases/supplier-invoices.get.parameters.supplier_reference.schema` | type now also accepts/returns null |
| `response_schema_const_added` | `paths./api/owner/sales/customers/{reference}/balance.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.summary.properties.overdue_invoice_count` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/owner/sales/customers/{reference}/balance.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.summary.properties.paid_invoice_count` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/owner/sales/customers/{reference}/balance.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.summary.properties.partially_paid_invoice_count` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/owner/sales/customers/{reference}/balance.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.summary.properties.unpaid_invoice_count` | const added (value set narrowed to one value) |
| `operation_added` | `paths./api/owner/sales/sales-returns.get` | GET /api/owner/sales/sales-returns added to the contract |
| `operation_added` | `paths./api/owner/sales/sales-returns/{publicReference}.get` | GET /api/owner/sales/sales-returns/{publicReference} added to the contract |
| `response_schema_enum_value_removed` | `paths./api/public/integrations/purchase-order-links/{token}.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.next_action` | response no longer contains a previously possible value |
| `response_schema_required_field_added` | `paths./api/public/integrations/purchase-order-links/{token}.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.register_send_code_url` | new REQUIRED field [register_send_code_url] |
| `operation_added` | `paths./api/public/integrations/purchase-order-links/{token}/account/send-code.post` | POST /api/public/integrations/purchase-order-links/{token}/account/send-code added to the contract |
| `operation_added` | `paths./api/public/integrations/purchase-order-links/{token}/account/verify.post` | POST /api/public/integrations/purchase-order-links/{token}/account/verify added to the contract |
| `response_schema_const_added` | `paths./api/public/legal/privacy.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.sections.anyOf[1].prefixItems[0].properties.title` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/public/legal/terms.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.sections.anyOf[1].prefixItems[0].properties.title` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/v1/account.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[1].properties.subscription.properties.usage.prefixItems[0].properties.limit` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/v1/account.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[1].properties.subscription.properties.usage.prefixItems[1].properties.limit` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/v1/account/subscription.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[1].properties.subscription.properties.usage.prefixItems[0].properties.limit` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/v1/account/subscription.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[1].properties.subscription.properties.usage.prefixItems[1].properties.limit` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/v1/accounting/posting-requests/reprocess.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.outbox_claimed` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/v1/content/legal/privacy.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.sections.anyOf[1].prefixItems[0].properties.title` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/v1/content/legal/terms.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.sections.anyOf[1].prefixItems[0].properties.title` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/v1/customers/{reference}/balance.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.summary.properties.overdue_invoice_count` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/v1/customers/{reference}/balance.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.summary.properties.paid_invoice_count` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/v1/customers/{reference}/balance.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.summary.properties.partially_paid_invoice_count` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/v1/customers/{reference}/balance.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.summary.properties.unpaid_invoice_count` | const added (value set narrowed to one value) |
| `response_schema_enum_value_removed` | `paths./api/v1/integrations/purchase-order-links/{token}.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.next_action` | response no longer contains a previously possible value |
| `response_schema_required_field_added` | `paths./api/v1/integrations/purchase-order-links/{token}.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.register_send_code_url` | new REQUIRED field [register_send_code_url] |
| `operation_added` | `paths./api/v1/integrations/purchase-order-links/{token}/account/send-code.post` | POST /api/v1/integrations/purchase-order-links/{token}/account/send-code added to the contract |
| `operation_added` | `paths./api/v1/integrations/purchase-order-links/{token}/account/verify.post` | POST /api/v1/integrations/purchase-order-links/{token}/account/verify added to the contract |
| `response_schema_const_added` | `paths./api/v1/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.available_count` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/v1/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.low_count` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/v1/platform/dashboard.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subscriptions_active_count` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/v1/platform/dashboard.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subscriptions_expired_count` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/v1/platform/dashboard.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subscriptions_near_renewal_count` | const added (value set narrowed to one value) |
| `response_schema_const_added` | `paths./api/v1/purchase-orders.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.summary.properties.open_count` | const added (value set narrowed to one value) |
| `operation_added` | `paths./api/v1/purchase-returns.get` | GET /api/v1/purchase-returns added to the contract |
| `operation_added` | `paths./api/v1/purchase-returns/{purchaseReturn}.get` | GET /api/v1/purchase-returns/{purchaseReturn} added to the contract |
| `operation_added` | `paths./api/v1/sales-returns.get` | GET /api/v1/sales-returns added to the contract |
| `operation_added` | `paths./api/v1/sales-returns/{publicReference}.get` | GET /api/v1/sales-returns/{publicReference} added to the contract |
| `parameter_became_optional` | `paths./api/v1/supplier-invoices.get.parameters.supplier_reference.required` | parameter [supplier_reference] became optional |
| `parameter_schema_nullability_added` | `paths./api/v1/supplier-invoices.get.parameters.supplier_reference.schema` | type now also accepts/returns null |

## Documentation-only changes (23)

| Kind | Location | Detail |
|---|---|---|
| `component_schema_documentation` | `components.schemas.CreatePurchaseReturnRequest` | description changed |
| `response_status_added` | `paths./api/accountant/meetings/meetings/{meetingReference}/join.get.responses.302` | response [302] added to the contract |
| `parameter_documentation` | `paths./api/accountant/purchases/supplier-invoices.get.parameters.supplier_reference.description` | parameter description changed |
| `response_status_added` | `paths./api/auth/accountant/meetings/{meetingReference}/join.get.responses.302` | response [302] added to the contract |
| `response_status_added` | `paths./api/owner/meetings/meetings/{meetingReference}/join.get.responses.302` | response [302] added to the contract |
| `parameter_documentation` | `paths./api/owner/purchases/supplier-invoices.get.parameters.supplier_reference.description` | parameter description changed |
| `response_schema_documentation` | `paths./api/public/integrations/purchase-order-links/{token}.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.next_action` | description changed |
| `response_status_added` | `paths./api/v1/accountant/meetings/{meetingReference}/join.get.responses.302` | response [302] added to the contract |
| `response_schema_documentation` | `paths./api/v1/integrations/purchase-order-links/{token}.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.next_action` | description changed |
| `response_status_added` | `paths./api/v1/meetings/{meetingReference}/join.get.responses.302` | response [302] added to the contract |
| `parameter_documentation` | `paths./api/v1/supplier-invoices.get.parameters.supplier_reference.description` | parameter description changed |
| `operation_documentation` | `paths./api/v1/zakat/history.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/zakat/history.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/zakat/history.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/zakat/periods.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/zakat/periods.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/zakat/periods.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/zakat/rates.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/zakat/rates.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/zakat/rates.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/zakat/sessions/{uuid}.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/zakat/sessions/{uuid}.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/zakat/sessions/{uuid}.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |

