# OpenAPI Contract Compatibility Report

- Baseline: `published 2026.10.27-abe5a72d2ae0` (1286 operations)
- Candidate: `build b4e32aec3c7e` (1667 operations)
- Generated: 2026-11-08T13:10:36.866583+00:00

## Summary

| Category | Count |
|---|---|
| BREAKING | 1226 |
| UNKNOWN | 104 |
| NON_BREAKING | 1660 |
| DOCUMENTATION_ONLY | 282 |
| **total** | **3272** |

## Breaking changes (1226)

| Kind | Location | Detail |
|---|---|---|
| `component_schema_nullability_added` | `components.schemas.AccountantOperationalDashboardResource.properties.branch_performance.items.properties.waste_percentage` | type now also accepts/returns null |
| `component_schema_enum_value_added` | `components.schemas.AccountantOperationalDashboardResource.properties.follow_up_operations.items.properties.type` | response may now contain a value clients do not handle |
| `shared_component_removed` | `components.schemas.AdminNotificationResource` | component [schemas.AdminNotificationResource] removed — 2 operation(s) referenced it |
| `component_schema_type_changed` | `components.schemas.AssetResource.properties.depreciation_log.items` | type changed (['object'] -> ['string']) |
| `component_schema_field_removed` | `components.schemas.AssetResource.properties.depreciation_log.items.properties.accumulated` | field [accumulated] removed |
| `component_schema_field_removed` | `components.schemas.AssetResource.properties.depreciation_log.items.properties.amount` | field [amount] removed |
| `component_schema_field_removed` | `components.schemas.AssetResource.properties.depreciation_log.items.properties.book_value` | field [book_value] removed |
| `component_schema_field_removed` | `components.schemas.AssetResource.properties.depreciation_log.items.properties.period` | field [period] removed |
| `component_schema_field_removed` | `components.schemas.AssetResource.properties.depreciation_log.items.properties.recorded_at` | field [recorded_at] removed |
| `component_schema_type_changed` | `components.schemas.ClosingTaskResource.properties.attachments.items` | type changed (['object'] -> ['string']) |
| `component_schema_field_removed` | `components.schemas.ClosingTaskResource.properties.attachments.items.properties.content_sha256` | field [content_sha256] removed |
| `component_schema_field_removed` | `components.schemas.ClosingTaskResource.properties.attachments.items.properties.created_at` | field [created_at] removed |
| `component_schema_field_removed` | `components.schemas.ClosingTaskResource.properties.attachments.items.properties.file_name` | field [file_name] removed |
| `component_schema_field_removed` | `components.schemas.ClosingTaskResource.properties.attachments.items.properties.id` | field [id] removed |
| `component_schema_field_removed` | `components.schemas.ClosingTaskResource.properties.attachments.items.properties.mime_type` | field [mime_type] removed |
| `component_schema_field_removed` | `components.schemas.ClosingTaskResource.properties.attachments.items.properties.size_bytes` | field [size_bytes] removed |
| `component_schema_field_removed` | `components.schemas.ClosingTaskResource.properties.attachments.items.properties.uploaded_by_reference` | field [uploaded_by_reference] removed |
| `component_schema_type_changed` | `components.schemas.ClosingTaskResource.properties.notes.items` | type changed (['object'] -> ['string']) |
| `component_schema_field_removed` | `components.schemas.ClosingTaskResource.properties.notes.items.properties.author_reference` | field [author_reference] removed |
| `component_schema_field_removed` | `components.schemas.ClosingTaskResource.properties.notes.items.properties.body` | field [body] removed |
| `component_schema_field_removed` | `components.schemas.ClosingTaskResource.properties.notes.items.properties.created_at` | field [created_at] removed |
| `component_schema_field_removed` | `components.schemas.ClosingTaskResource.properties.notes.items.properties.id` | field [id] removed |
| `component_schema_pattern_added` | `components.schemas.CreateCustomerRequest.properties.commercial_registration_no` | pattern added |
| `component_schema_pattern_added` | `components.schemas.CreateCustomerRequest.properties.tax_number` | pattern added |
| `component_schema_constraint_narrowed` | `components.schemas.CreatePurchaseReturnRequest.properties.branch_id` | [minimum] None -> 1 |
| `component_schema_required_field_added` | `components.schemas.CreatePurchaseReturnRequest.properties.return_reason` | new REQUIRED field [return_reason] |
| `component_schema_field_became_required` | `components.schemas.CreateSupplierRequest.properties.payment_terms` | field [payment_terms] became required |
| `component_schema_nullability_removed` | `components.schemas.CreateSupplierRequest.properties.payment_terms` | type no longer accepts/returns null |
| `component_schema_enum_value_removed` | `components.schemas.CreateSupplierRequest.properties.supplier_type` | previously accepted enum value no longer accepted |
| `component_schema_field_became_required` | `components.schemas.CreateSupplierRequest.properties.supplier_type` | field [supplier_type] became required |
| `component_schema_nullability_removed` | `components.schemas.CreateSupplierRequest.properties.supplier_type` | type no longer accepts/returns null |
| `component_schema_field_became_required` | `components.schemas.CreateSupplierRequest.properties.supply_category` | field [supply_category] became required |
| `component_schema_nullability_removed` | `components.schemas.CreateSupplierRequest.properties.supply_category` | type no longer accepts/returns null |
| `component_schema_type_changed` | `components.schemas.DirectPurchaseResource.properties.invoices.items` | type changed (['object'] -> ['string']) |
| `component_schema_field_removed` | `components.schemas.DirectPurchaseResource.properties.invoices.items.properties.document` | field [document] removed |
| `component_schema_field_removed` | `components.schemas.DirectPurchaseResource.properties.invoices.items.properties.invoice_date` | field [invoice_date] removed |
| `component_schema_field_removed` | `components.schemas.DirectPurchaseResource.properties.invoices.items.properties.invoice_number` | field [invoice_number] removed |
| `component_schema_field_removed` | `components.schemas.DirectPurchaseResource.properties.invoices.items.properties.reference` | field [reference] removed |
| `component_schema_field_removed` | `components.schemas.DirectPurchaseResource.properties.invoices.items.properties.total_amount` | field [total_amount] removed |
| `component_schema_field_removed` | `components.schemas.DirectPurchaseResource.properties.invoices.items.properties.uploaded_by_reference` | field [uploaded_by_reference] removed |
| `component_schema_type_changed` | `components.schemas.DirectPurchaseResource.properties.lines.items` | type changed (['object'] -> ['string']) |
| `component_schema_field_removed` | `components.schemas.DirectPurchaseResource.properties.lines.items.properties.inventory_item_reference` | field [inventory_item_reference] removed |
| `component_schema_field_removed` | `components.schemas.DirectPurchaseResource.properties.lines.items.properties.is_stock` | field [is_stock] removed |
| `component_schema_field_removed` | `components.schemas.DirectPurchaseResource.properties.lines.items.properties.item_description` | field [item_description] removed |
| `component_schema_field_removed` | `components.schemas.DirectPurchaseResource.properties.lines.items.properties.line_number` | field [line_number] removed |
| `component_schema_field_removed` | `components.schemas.DirectPurchaseResource.properties.lines.items.properties.line_total` | field [line_total] removed |
| `component_schema_field_removed` | `components.schemas.DirectPurchaseResource.properties.lines.items.properties.quantity` | field [quantity] removed |
| `component_schema_field_removed` | `components.schemas.DirectPurchaseResource.properties.lines.items.properties.received_quantity` | field [received_quantity] removed |
| `component_schema_field_removed` | `components.schemas.DirectPurchaseResource.properties.lines.items.properties.reference` | field [reference] removed |
| `component_schema_field_removed` | `components.schemas.DirectPurchaseResource.properties.lines.items.properties.stock_movement_reference` | field [stock_movement_reference] removed |
| `component_schema_field_removed` | `components.schemas.DirectPurchaseResource.properties.lines.items.properties.unit` | field [unit] removed |
| `component_schema_field_removed` | `components.schemas.DirectPurchaseResource.properties.lines.items.properties.unit_price` | field [unit_price] removed |
| `component_schema_type_changed` | `components.schemas.GoodsReceiptResource.properties.lines.items` | type changed (['object'] -> ['string']) |
| `component_schema_field_removed` | `components.schemas.GoodsReceiptResource.properties.lines.items.properties.inventory_item_reference` | field [inventory_item_reference] removed |
| `component_schema_field_removed` | `components.schemas.GoodsReceiptResource.properties.lines.items.properties.line_reference` | field [line_reference] removed |
| `component_schema_field_removed` | `components.schemas.GoodsReceiptResource.properties.lines.items.properties.received_quantity` | field [received_quantity] removed |
| `component_schema_field_removed` | `components.schemas.GoodsReceiptResource.properties.lines.items.properties.reference` | field [reference] removed |
| `component_schema_field_removed` | `components.schemas.GoodsReceiptResource.properties.lines.items.properties.stock_movement_reference` | field [stock_movement_reference] removed |
| `component_schema_field_removed` | `components.schemas.GoodsReceiptResource.properties.lines.items.properties.unit_cost` | field [unit_cost] removed |
| `component_schema_required_field_added` | `components.schemas.JournalEntry.properties.created_by_reference` | new REQUIRED field [created_by_reference] |
| `component_schema_required_field_added` | `components.schemas.JournalEntry.properties.entry_number` | new REQUIRED field [entry_number] |
| `component_schema_required_field_added` | `components.schemas.OwnerDashboardResource.properties.low_stock_items` | new REQUIRED field [low_stock_items] |
| `component_schema_type_changed` | `components.schemas.PayrollRunReviewResource.properties.lines.items` | type changed (['object'] -> ['string']) |
| `component_schema_field_removed` | `components.schemas.PayrollRunReviewResource.properties.lines.items.properties.basic_salary` | field [basic_salary] removed |
| `component_schema_field_removed` | `components.schemas.PayrollRunReviewResource.properties.lines.items.properties.employee_name` | field [employee_name] removed |
| `component_schema_field_removed` | `components.schemas.PayrollRunReviewResource.properties.lines.items.properties.employee_reference` | field [employee_reference] removed |
| `component_schema_field_removed` | `components.schemas.PayrollRunReviewResource.properties.lines.items.properties.id` | field [id] removed |
| `component_schema_field_removed` | `components.schemas.PayrollRunReviewResource.properties.lines.items.properties.net_salary` | field [net_salary] removed |
| `component_schema_field_removed` | `components.schemas.PayrollRunReviewResource.properties.lines.items.properties.status` | field [status] removed |
| `component_schema_field_removed` | `components.schemas.PayrollRunReviewResource.properties.lines.items.properties.status_label` | field [status_label] removed |
| `component_schema_field_removed` | `components.schemas.PayrollRunReviewResource.properties.lines.items.properties.total_allowances` | field [total_allowances] removed |
| `component_schema_field_removed` | `components.schemas.PayrollRunReviewResource.properties.lines.items.properties.total_deductions` | field [total_deductions] removed |
| `shared_component_removed` | `components.schemas.PricingSession` | component [schemas.PricingSession] removed — 3 operation(s) referenced it |
| `component_schema_type_changed` | `components.schemas.PurchaseOrderDeliveryResource.properties.attempts.items` | type changed (['object'] -> ['string']) |
| `component_schema_field_removed` | `components.schemas.PurchaseOrderDeliveryResource.properties.attempts.items.properties.attempt_number` | field [attempt_number] removed |
| `component_schema_field_removed` | `components.schemas.PurchaseOrderDeliveryResource.properties.attempts.items.properties.attempted_at` | field [attempted_at] removed |
| `component_schema_field_removed` | `components.schemas.PurchaseOrderDeliveryResource.properties.attempts.items.properties.channel_key` | field [channel_key] removed |
| `component_schema_field_removed` | `components.schemas.PurchaseOrderDeliveryResource.properties.attempts.items.properties.error_code` | field [error_code] removed |
| `component_schema_field_removed` | `components.schemas.PurchaseOrderDeliveryResource.properties.attempts.items.properties.outcome` | field [outcome] removed |
| `component_schema_field_removed` | `components.schemas.PurchaseOrderDeliveryResource.properties.attempts.items.properties.provider_message_reference` | field [provider_message_reference] removed |
| `component_schema_type_changed` | `components.schemas.PurchaseOrderResource.properties.actions.properties.edit` | type changed (['boolean'] -> ['string']) |
| `component_schema_type_changed` | `components.schemas.PurchaseOrderResource.properties.actions.properties.send` | type changed (['boolean'] -> ['string']) |
| `component_schema_type_changed` | `components.schemas.PurchaseOrderResource.properties.invoices.items` | type changed (['object'] -> ['string']) |
| `component_schema_field_removed` | `components.schemas.PurchaseOrderResource.properties.invoices.items.properties.invoice_amount` | field [invoice_amount] removed |
| `component_schema_field_removed` | `components.schemas.PurchaseOrderResource.properties.invoices.items.properties.invoice_number` | field [invoice_number] removed |
| `component_schema_field_removed` | `components.schemas.PurchaseOrderResource.properties.invoices.items.properties.locked` | field [locked] removed |
| `component_schema_field_removed` | `components.schemas.PurchaseOrderResource.properties.invoices.items.properties.purchase_order_number` | field [purchase_order_number] removed |
| `component_schema_field_removed` | `components.schemas.PurchaseOrderResource.properties.invoices.items.properties.supplier_invoice_reference` | field [supplier_invoice_reference] removed |
| `component_schema_field_removed` | `components.schemas.PurchaseOrderResource.properties.invoices.items.properties.supplier_reference` | field [supplier_reference] removed |
| `component_schema_field_removed` | `components.schemas.PurchaseOrderResource.properties.invoices.items.properties.uploaded_by_kind` | field [uploaded_by_kind] removed |
| `component_schema_type_changed` | `components.schemas.PurchaseOrderResource.properties.lines.items` | type changed (['object'] -> ['string']) |
| `component_schema_field_removed` | `components.schemas.PurchaseOrderResource.properties.lines.items.properties.inventory_item_reference` | field [inventory_item_reference] removed |
| `component_schema_field_removed` | `components.schemas.PurchaseOrderResource.properties.lines.items.properties.item_description` | field [item_description] removed |
| `component_schema_field_removed` | `components.schemas.PurchaseOrderResource.properties.lines.items.properties.line_number` | field [line_number] removed |
| `component_schema_field_removed` | `components.schemas.PurchaseOrderResource.properties.lines.items.properties.line_total` | field [line_total] removed |
| `component_schema_field_removed` | `components.schemas.PurchaseOrderResource.properties.lines.items.properties.quantity` | field [quantity] removed |
| `component_schema_field_removed` | `components.schemas.PurchaseOrderResource.properties.lines.items.properties.received_quantity` | field [received_quantity] removed |
| `component_schema_field_removed` | `components.schemas.PurchaseOrderResource.properties.lines.items.properties.reference` | field [reference] removed |
| `component_schema_field_removed` | `components.schemas.PurchaseOrderResource.properties.lines.items.properties.remaining_quantity` | field [remaining_quantity] removed |
| `component_schema_field_removed` | `components.schemas.PurchaseOrderResource.properties.lines.items.properties.unit` | field [unit] removed |
| `component_schema_field_removed` | `components.schemas.PurchaseOrderResource.properties.lines.items.properties.unit_price` | field [unit_price] removed |
| `component_schema_field_became_required` | `components.schemas.RecordCustomerCollectionRequest.properties.payment_method` | field [payment_method] became required |
| `component_schema_nullability_removed` | `components.schemas.RecordCustomerCollectionRequest.properties.payment_method` | type no longer accepts/returns null |
| `component_schema_field_became_required` | `components.schemas.RegisterApplicationRequest.properties.accept_terms` | field [accept_terms] became required |
| `component_schema_field_became_required` | `components.schemas.RegisterApplicationRequest.properties.phone` | field [phone] became required |
| `component_schema_nullability_removed` | `components.schemas.RegisterApplicationRequest.properties.phone` | type no longer accepts/returns null |
| `component_schema_pattern_changed` | `components.schemas.RegisterApplicationRequest.properties.phone` | pattern replaced (inclusion cannot be proven) |
| `shared_component_removed` | `components.schemas.SelectPackageRequest` | component [schemas.SelectPackageRequest] removed — 2 operation(s) referenced it |
| `shared_component_removed` | `components.schemas.StockBalance` | component [schemas.StockBalance] removed — 2 operation(s) referenced it |
| `component_schema_field_became_required` | `components.schemas.StoreAccountantTaskRequest.properties.company_id` | field [company_id] became required |
| `component_schema_nullability_removed` | `components.schemas.StoreAccountantTaskRequest.properties.company_id` | type no longer accepts/returns null |
| `component_schema_required_field_added` | `components.schemas.StoreAssetRequest.properties.acquisition_source` | new REQUIRED field [acquisition_source] |
| `component_schema_constraint_narrowed` | `components.schemas.StoreBranchRequest.properties.phone` | [maxLength] 255 -> 20 |
| `component_schema_pattern_added` | `components.schemas.StoreBranchRequest.properties.phone` | pattern added |
| `component_schema_constraint_narrowed` | `components.schemas.StoreCatalogProductRequest.properties.tax_percentage` | [maximum] None -> 100 |
| `component_schema_enum_added` | `components.schemas.StoreIntegrationConnectionRequest.properties.provider` | enum constraint added |
| `shared_component_removed` | `components.schemas.StoreIntegrationSyncRunRequest` | component [schemas.StoreIntegrationSyncRunRequest] removed — 3 operation(s) referenced it |
| `component_schema_constraint_narrowed` | `components.schemas.StoreSubscriptionPackageRequest.properties.duration_in_days` | [maximum] None -> 3660 |
| `component_schema_required_field_added` | `components.schemas.StoreSubscriptionPackageRequest.properties.modules` | new REQUIRED field [modules] |
| `component_schema_constraint_narrowed` | `components.schemas.StoreSubscriptionPackageRequest.properties.subscription_fee` | [maximum] None -> 999999999 |
| `component_schema_type_removed` | `components.schemas.SupplierResource.properties.invoice_number` | type removed (['string'] -> any) |
| `component_schema_type_changed` | `components.schemas.SupplierResource.properties.invoices.items` | type changed (['object'] -> ['string']) |
| `component_schema_field_removed` | `components.schemas.SupplierResource.properties.invoices.items.properties.due_date` | field [due_date] removed |
| `component_schema_field_removed` | `components.schemas.SupplierResource.properties.invoices.items.properties.invoice_date` | field [invoice_date] removed |
| `component_schema_field_removed` | `components.schemas.SupplierResource.properties.invoices.items.properties.paid_amount` | field [paid_amount] removed |
| `component_schema_field_removed` | `components.schemas.SupplierResource.properties.invoices.items.properties.payments` | field [payments] removed |
| `component_schema_field_removed` | `components.schemas.SupplierResource.properties.invoices.items.properties.po_reference` | field [po_reference] removed |
| `component_schema_field_removed` | `components.schemas.SupplierResource.properties.invoices.items.properties.reference` | field [reference] removed |
| `component_schema_field_removed` | `components.schemas.SupplierResource.properties.invoices.items.properties.remaining_amount` | field [remaining_amount] removed |
| `component_schema_field_removed` | `components.schemas.SupplierResource.properties.invoices.items.properties.status` | field [status] removed |
| `component_schema_field_removed` | `components.schemas.SupplierResource.properties.invoices.items.properties.total_amount` | field [total_amount] removed |
| `component_schema_constraint_narrowed` | `components.schemas.UpdateBranchRequest.properties.phone` | [maxLength] 255 -> 20 |
| `component_schema_pattern_added` | `components.schemas.UpdateBranchRequest.properties.phone` | pattern added |
| `component_schema_constraint_narrowed` | `components.schemas.UpdateCatalogProductRequest.properties.tax_percentage` | [maximum] None -> 100 |
| `component_schema_pattern_added` | `components.schemas.UpdateCustomerRequest.properties.commercial_registration_no` | pattern added |
| `component_schema_pattern_added` | `components.schemas.UpdateCustomerRequest.properties.tax_number` | pattern added |
| `shared_component_removed` | `components.schemas.UpdateIntegrationSyncRunRequest` | component [schemas.UpdateIntegrationSyncRunRequest] removed — 6 operation(s) referenced it |
| `component_schema_pattern_added` | `components.schemas.UpdateOrganizationRequest.properties.landline` | pattern added |
| `component_schema_pattern_added` | `components.schemas.UpdateOrganizationRequest.properties.phone` | pattern added |
| `component_schema_constraint_narrowed` | `components.schemas.UpdateSubscriptionPackageRequest.properties.duration_in_days` | [maximum] None -> 3660 |
| `component_schema_constraint_narrowed` | `components.schemas.UpdateSubscriptionPackageRequest.properties.subscription_fee` | [maximum] None -> 999999999 |
| `component_schema_pattern_changed` | `components.schemas.UpdateZakatItemRequest.properties.amount` | pattern replaced (inclusion cannot be proven) |
| `component_schema_type_changed` | `components.schemas.VatReturnPreparationResource.properties.lines.items` | type changed (['object'] -> ['string']) |
| `component_schema_field_removed` | `components.schemas.VatReturnPreparationResource.properties.lines.items.properties.amount` | field [amount] removed |
| `component_schema_field_removed` | `components.schemas.VatReturnPreparationResource.properties.lines.items.properties.document_count` | field [document_count] removed |
| `component_schema_field_removed` | `components.schemas.VatReturnPreparationResource.properties.lines.items.properties.line_type` | field [line_type] removed |
| `component_schema_field_removed` | `components.schemas.VatReturnPreparationResource.properties.lines.items.properties.tax_amount` | field [tax_amount] removed |
| `component_schema_type_changed` | `components.schemas.VatSummaryResource.properties.lines.items` | type changed (['object'] -> ['string']) |
| `component_schema_field_removed` | `components.schemas.VatSummaryResource.properties.lines.items.properties.amount_before_tax` | field [amount_before_tax] removed |
| `component_schema_field_removed` | `components.schemas.VatSummaryResource.properties.lines.items.properties.branch_id` | field [branch_id] removed |
| `component_schema_field_removed` | `components.schemas.VatSummaryResource.properties.lines.items.properties.direction` | field [direction] removed |
| `component_schema_field_removed` | `components.schemas.VatSummaryResource.properties.lines.items.properties.invoice_date` | field [invoice_date] removed |
| `component_schema_field_removed` | `components.schemas.VatSummaryResource.properties.lines.items.properties.invoice_number` | field [invoice_number] removed |
| `component_schema_field_removed` | `components.schemas.VatSummaryResource.properties.lines.items.properties.original_invoice_reference` | field [original_invoice_reference] removed |
| `component_schema_field_removed` | `components.schemas.VatSummaryResource.properties.lines.items.properties.source_reference` | field [source_reference] removed |
| `component_schema_field_removed` | `components.schemas.VatSummaryResource.properties.lines.items.properties.source_type` | field [source_type] removed |
| `component_schema_field_removed` | `components.schemas.VatSummaryResource.properties.lines.items.properties.tax_document_reference` | field [tax_document_reference] removed |
| `component_schema_field_removed` | `components.schemas.VatSummaryResource.properties.lines.items.properties.vat_amount` | field [vat_amount] removed |
| `component_schema_type_changed` | `components.schemas.ZakatSessionResource.properties.items.items` | type changed (['object'] -> ['string']) |
| `component_schema_field_removed` | `components.schemas.ZakatSessionResource.properties.items.items.properties.amount` | field [amount] removed |
| `component_schema_field_removed` | `components.schemas.ZakatSessionResource.properties.items.items.properties.description` | field [description] removed |
| `component_schema_field_removed` | `components.schemas.ZakatSessionResource.properties.items.items.properties.id` | field [id] removed |
| `component_schema_field_removed` | `components.schemas.ZakatSessionResource.properties.items.items.properties.is_manual` | field [is_manual] removed |
| `component_schema_field_removed` | `components.schemas.ZakatSessionResource.properties.items.items.properties.original_amount` | field [original_amount] removed |
| `component_schema_field_removed` | `components.schemas.ZakatSessionResource.properties.items.items.properties.source_id` | field [source_id] removed |
| `component_schema_field_removed` | `components.schemas.ZakatSessionResource.properties.items.items.properties.source_type` | field [source_type] removed |
| `component_schema_field_removed` | `components.schemas.ZakatSessionResource.properties.items.items.properties.type` | field [type] removed |
| `request_media_type_removed` | `paths./api/accountant/accounting/assets.post.requestBody.content.application/json` | request media type [application/json] removed |
| `response_schema_type_changed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items` | type changed (['object'] -> ['string']) |
| `response_schema_field_removed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.assigned_accountant_reference` | field [assigned_accountant_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.assigned_by_reference` | field [assigned_by_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.attachments` | field [attachments] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.blocks_close` | field [blocks_close] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.company_id` | field [company_id] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.completed_at` | field [completed_at] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.completed_by_reference` | field [completed_by_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.created_at` | field [created_at] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.definition` | field [definition] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.description` | field [description] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.display_status` | field [display_status] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.due_date` | field [due_date] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.fiscal_period_reference` | field [fiscal_period_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.id` | field [id] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.is_overdue` | field [is_overdue] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.name` | field [name] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.notes` | field [notes] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.priority` | field [priority] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.related` | field [related] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.source` | field [source] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.started_at` | field [started_at] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.status` | field [status] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.task_type` | field [task_type] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.version` | field [version] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.waiting_reason` | field [waiting_reason] removed |
| `request_schema_field_became_required` | `paths./api/accountant/accounting/journal-entries.post.requestBody.content.application/json.schema.properties.description` | field [description] became required |
| `request_schema_nullability_removed` | `paths./api/accountant/accounting/journal-entries.post.requestBody.content.application/json.schema.properties.description` | type no longer accepts/returns null |
| `request_schema_pattern_added` | `paths./api/accountant/accounting/journal-entries.post.requestBody.content.application/json.schema.properties.lines.items.properties.credit` | pattern added |
| `request_schema_type_changed` | `paths./api/accountant/accounting/journal-entries.post.requestBody.content.application/json.schema.properties.lines.items.properties.credit` | type changed (['number'] -> ['string']) |
| `request_schema_pattern_added` | `paths./api/accountant/accounting/journal-entries.post.requestBody.content.application/json.schema.properties.lines.items.properties.debit` | pattern added |
| `request_schema_type_changed` | `paths./api/accountant/accounting/journal-entries.post.requestBody.content.application/json.schema.properties.lines.items.properties.debit` | type changed (['number'] -> ['string']) |
| `response_status_removed` | `paths./api/accountant/accounting/journal-entries.post.responses.201` | response [201] removed from the contract |
| `request_schema_field_became_required` | `paths./api/accountant/accounting/journal-entries/{reference}.put.requestBody.content.application/json.schema.properties.description` | field [description] became required |
| `request_schema_nullability_removed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.requestBody.content.application/json.schema.properties.description` | type no longer accepts/returns null |
| `request_schema_pattern_added` | `paths./api/accountant/accounting/journal-entries/{reference}.put.requestBody.content.application/json.schema.properties.lines.items.properties.credit` | pattern added |
| `request_schema_type_changed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.requestBody.content.application/json.schema.properties.lines.items.properties.credit` | type changed (['number'] -> ['string']) |
| `request_schema_pattern_added` | `paths./api/accountant/accounting/journal-entries/{reference}.put.requestBody.content.application/json.schema.properties.lines.items.properties.debit` | pattern added |
| `request_schema_type_changed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.requestBody.content.application/json.schema.properties.lines.items.properties.debit` | type changed (['number'] -> ['string']) |
| `response_schema_type_removed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data` | type removed (['object'] -> any) |
| `response_schema_field_removed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.amount` | field [amount] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments` | field [attachments] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branch_id` | field [branch_id] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.can_amend` | field [can_amend] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.can_approve` | field [can_approve] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.company_id` | field [company_id] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.created_at` | field [created_at] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.description` | field [description] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.document_date` | field [document_date] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.fiscal_period_id` | field [fiscal_period_id] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.lines` | field [lines] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.owner_requests` | field [owner_requests] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.posting_date` | field [posting_date] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.public_reference` | field [public_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.ref_id` | field [ref_id] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.ref_type` | field [ref_type] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.source_reference` | field [source_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.source_type` | field [source_type] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | field [status] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status_category` | field [status_category] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total_credit` | field [total_credit] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total_debit` | field [total_debit] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.transaction_type` | field [transaction_type] removed |
| `response_schema_type_changed` | `paths./api/accountant/accounting/posting-mappings.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items` | type changed (['object'] -> ['string']) |
| `response_schema_field_removed` | `paths./api/accountant/accounting/posting-mappings.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.account` | field [account] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/posting-mappings.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.assigned_at` | field [assigned_at] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/posting-mappings.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.assigned_by` | field [assigned_by] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/posting-mappings.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.effective_from` | field [effective_from] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/posting-mappings.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.effective_to` | field [effective_to] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/posting-mappings.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.end_reason` | field [end_reason] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/posting-mappings.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.ended_at` | field [ended_at] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/posting-mappings.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.ended_by` | field [ended_by] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/posting-mappings.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.id` | field [id] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/posting-mappings.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.role` | field [role] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/posting-mappings.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.status` | field [status] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/posting-mappings.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.version` | field [version] removed |
| `response_schema_type_changed` | `paths./api/accountant/accounting/reconciliation/bank-accounts.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items` | type changed (['object'] -> ['string']) |
| `response_schema_field_removed` | `paths./api/accountant/accounting/reconciliation/bank-accounts.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.account_holder` | field [account_holder] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/reconciliation/bank-accounts.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.account_number` | field [account_number] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/reconciliation/bank-accounts.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.bank_name` | field [bank_name] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/reconciliation/bank-accounts.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.branch_id` | field [branch_id] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/reconciliation/bank-accounts.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.currency` | field [currency] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/reconciliation/bank-accounts.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.iban` | field [iban] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/reconciliation/bank-accounts.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.id` | field [id] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/reconciliation/bank-accounts.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.is_default` | field [is_default] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/reconciliation/bank-accounts.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.ledger_account_reference` | field [ledger_account_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/reconciliation/bank-accounts.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.name` | field [name] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/reconciliation/bank-accounts.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.status` | field [status] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/reconciliation/bank-accounts.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.swift_code` | field [swift_code] removed |
| `response_schema_field_removed` | `paths./api/accountant/accounting/reconciliation/bank-accounts.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.version` | field [version] removed |
| `request_schema_field_removed` | `paths./api/accountant/accounting/reconciliation/bank-statements.post.requestBody.content.multipart/form-data.schema.properties.bank_account_id` | field [bank_account_id] removed |
| `request_schema_field_removed` | `paths./api/accountant/accounting/reconciliation/bank-statements.post.requestBody.content.multipart/form-data.schema.properties.file` | field [file] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.account_reference` | field [account_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.accountant_reference` | field [accountant_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.amount_before_tax` | field [amount_before_tax] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.approved_at` | field [approved_at] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.approved_version` | field [approved_version] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branch_id` | field [branch_id] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.classification_review_reason` | field [classification_review_reason] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.classification_status` | field [classification_status] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.description` | field [description] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.document_path` | field [document_path] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.document_url` | field [document_url] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.due_date` | field [due_date] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.expense_category` | field [expense_category] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.invoice_date` | field [invoice_date] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.invoice_number` | field [invoice_number] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.journal_entry_reference` | field [journal_entry_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.journal_posted_at` | field [journal_posted_at] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.notes` | field [notes] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.operation_type` | field [operation_type] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.payment_method` | field [payment_method] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.payment_status` | field [payment_status] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.posting_requested_at` | field [posting_requested_at] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.public_reference` | field [public_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.source` | field [source] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | field [status] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.suggested_expense_category` | field [suggested_expense_category] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.suggested_operation_type` | field [suggested_operation_type] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.supplier_reference` | field [supplier_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.suspicion_reason` | field [suspicion_reason] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total_amount` | field [total_amount] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.vat_amount` | field [vat_amount] removed |
| `response_schema_field_removed` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.version` | field [version] removed |
| `response_schema_type_changed` | `paths./api/accountant/general/closing-tasks/{taskId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments.items` | type changed (['object'] -> ['string']) |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments.items.properties.content_sha256` | field [content_sha256] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments.items.properties.created_at` | field [created_at] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments.items.properties.file_name` | field [file_name] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments.items.properties.id` | field [id] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments.items.properties.mime_type` | field [mime_type] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments.items.properties.size_bytes` | field [size_bytes] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments.items.properties.uploaded_by_reference` | field [uploaded_by_reference] removed |
| `response_schema_type_changed` | `paths./api/accountant/general/closing-tasks/{taskId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.notes.items` | type changed (['object'] -> ['string']) |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.notes.items.properties.author_reference` | field [author_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.notes.items.properties.body` | field [body] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.notes.items.properties.created_at` | field [created_at] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.notes.items.properties.id` | field [id] removed |
| `response_schema_type_changed` | `paths./api/accountant/general/closing-tasks/{taskId}.patch.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments.items` | type changed (['object'] -> ['string']) |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}.patch.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments.items.properties.content_sha256` | field [content_sha256] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}.patch.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments.items.properties.created_at` | field [created_at] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}.patch.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments.items.properties.file_name` | field [file_name] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}.patch.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments.items.properties.id` | field [id] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}.patch.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments.items.properties.mime_type` | field [mime_type] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}.patch.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments.items.properties.size_bytes` | field [size_bytes] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}.patch.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments.items.properties.uploaded_by_reference` | field [uploaded_by_reference] removed |
| `response_schema_type_changed` | `paths./api/accountant/general/closing-tasks/{taskId}.patch.responses.200.content.application/json.schema.allOf[1].properties.data.properties.notes.items` | type changed (['object'] -> ['string']) |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}.patch.responses.200.content.application/json.schema.allOf[1].properties.data.properties.notes.items.properties.author_reference` | field [author_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}.patch.responses.200.content.application/json.schema.allOf[1].properties.data.properties.notes.items.properties.body` | field [body] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}.patch.responses.200.content.application/json.schema.allOf[1].properties.data.properties.notes.items.properties.created_at` | field [created_at] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}.patch.responses.200.content.application/json.schema.allOf[1].properties.data.properties.notes.items.properties.id` | field [id] removed |
| `response_schema_type_changed` | `paths./api/accountant/general/closing-tasks/{taskId}/complete.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments.items` | type changed (['object'] -> ['string']) |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}/complete.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments.items.properties.content_sha256` | field [content_sha256] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}/complete.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments.items.properties.created_at` | field [created_at] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}/complete.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments.items.properties.file_name` | field [file_name] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}/complete.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments.items.properties.id` | field [id] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}/complete.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments.items.properties.mime_type` | field [mime_type] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}/complete.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments.items.properties.size_bytes` | field [size_bytes] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}/complete.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments.items.properties.uploaded_by_reference` | field [uploaded_by_reference] removed |
| `response_schema_type_changed` | `paths./api/accountant/general/closing-tasks/{taskId}/complete.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.notes.items` | type changed (['object'] -> ['string']) |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}/complete.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.notes.items.properties.author_reference` | field [author_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}/complete.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.notes.items.properties.body` | field [body] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}/complete.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.notes.items.properties.created_at` | field [created_at] removed |
| `response_schema_field_removed` | `paths./api/accountant/general/closing-tasks/{taskId}/complete.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.notes.items.properties.id` | field [id] removed |
| `response_schema_const_removed` | `paths./api/accountant/general/vat-returns/{vatReturn}/export.post.responses.200.content.application/json.schema.properties.message` | const removed (value set widened) |
| `request_body_removed` | `paths./api/accountant/integrations/integrations/sync-runs.post.requestBody` | request body removed from the contract |
| `response_status_removed` | `paths./api/accountant/integrations/integrations/sync-runs.post.responses.201` | response [201] removed from the contract |
| `request_body_removed` | `paths./api/accountant/integrations/integrations/sync-runs/{syncRun}.patch.requestBody` | request body removed from the contract |
| `response_media_type_removed` | `paths./api/accountant/integrations/integrations/sync-runs/{syncRun}.patch.responses.200.content.application/json` | response media type [application/json] removed |
| `request_body_removed` | `paths./api/accountant/integrations/integrations/sync-runs/{syncRun}.put.requestBody` | request body removed from the contract |
| `response_media_type_removed` | `paths./api/accountant/integrations/integrations/sync-runs/{syncRun}.put.responses.200.content.application/json` | response media type [application/json] removed |
| `response_schema_type_changed` | `paths./api/accountant/inventory/catalog-products/{catalogProduct}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.recipe.items` | type changed (['object'] -> ['string']) |
| `response_schema_field_removed` | `paths./api/accountant/inventory/catalog-products/{catalogProduct}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.recipe.items.properties.inventory_item_reference` | field [inventory_item_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/inventory/catalog-products/{catalogProduct}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.recipe.items.properties.quantity` | field [quantity] removed |
| `response_schema_enum_removed` | `paths./api/accountant/inventory/waste/records/{wasteRecord}.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[1].properties.inventory_movement.properties.status` | enum constraint removed |
| `response_schema_enum_removed` | `paths./api/accountant/inventory/waste/records/{wasteRecord}/confirm.post.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[1].properties.inventory_movement.properties.status` | enum constraint removed |
| `response_schema_enum_removed` | `paths./api/accountant/notifications/notifications/{uuid}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.target` | enum constraint removed |
| `response_schema_type_changed` | `paths./api/accountant/pricing/pricing/finalize-price.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.materials.items` | type changed (['object'] -> ['string']) |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/finalize-price.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.materials.items.properties.component_reference` | field [component_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/finalize-price.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.materials.items.properties.id` | field [id] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/finalize-price.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.materials.items.properties.quantity` | field [quantity] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/finalize-price.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.materials.items.properties.supplier_reference` | field [supplier_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/finalize-price.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.materials.items.properties.total_cost` | field [total_cost] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/finalize-price.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.materials.items.properties.unit_cost` | field [unit_cost] removed |
| `response_schema_type_changed` | `paths./api/accountant/pricing/pricing/finalize-price.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.operating_items.items` | type changed (['object'] -> ['string']) |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/finalize-price.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.operating_items.items.properties.cost_item_name` | field [cost_item_name] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/finalize-price.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.operating_items.items.properties.unit_share` | field [unit_share] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.active_lock` | field [active_lock] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branch_id` | field [branch_id] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.company_id` | field [company_id] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.created_at` | field [created_at] removed |
| `response_schema_format_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.finalized_at` | format changed ('date-time' -> None) |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.finalized_by` | field [finalized_by] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.idx_branch_id` | field [idx_branch_id] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.idx_tenant_id` | field [idx_tenant_id] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.owner_decision` | field [owner_decision] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.prepared_at` | field [prepared_at] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.prepared_by` | field [prepared_by] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.proposal_basis` | field [proposal_basis] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.proposed_at` | field [proposed_at] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.proposed_by` | field [proposed_by] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.proposed_margin_rate` | field [proposed_margin_rate] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.public_reference` | field [public_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.reviewed_at` | field [reviewed_at] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.reviewed_by` | field [reviewed_by] removed |
| `response_schema_format_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.submitted_at` | format changed ('date-time' -> None) |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.tenant_id` | field [tenant_id] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total_operating_cost` | field [total_operating_cost] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.updated_at` | field [updated_at] removed |
| `response_schema_type_changed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}/operating-cost-allocation.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items` | type changed (['object'] -> ['string']) |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}/operating-cost-allocation.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.allocation_basis_units` | field [allocation_basis_units] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}/operating-cost-allocation.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.cost_item_name` | field [cost_item_name] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}/operating-cost-allocation.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.period_amount` | field [period_amount] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}/operating-cost-allocation.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.period_end` | field [period_end] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}/operating-cost-allocation.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.period_start` | field [period_start] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}/operating-cost-allocation.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.recorded_at` | field [recorded_at] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}/operating-cost-allocation.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.recorded_by` | field [recorded_by] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}/operating-cost-allocation.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.reference` | field [reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}/operating-cost-allocation.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.source_reference` | field [source_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}/operating-cost-allocation.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.unit_share` | field [unit_share] removed |
| `response_schema_type_changed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}/submit-to-owner.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.materials.items` | type changed (['object'] -> ['string']) |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}/submit-to-owner.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.materials.items.properties.component_reference` | field [component_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}/submit-to-owner.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.materials.items.properties.id` | field [id] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}/submit-to-owner.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.materials.items.properties.quantity` | field [quantity] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}/submit-to-owner.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.materials.items.properties.supplier_reference` | field [supplier_reference] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}/submit-to-owner.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.materials.items.properties.total_cost` | field [total_cost] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}/submit-to-owner.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.materials.items.properties.unit_cost` | field [unit_cost] removed |
| `response_schema_type_changed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}/submit-to-owner.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.operating_items.items` | type changed (['object'] -> ['string']) |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}/submit-to-owner.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.operating_items.items.properties.cost_item_name` | field [cost_item_name] removed |
| `response_schema_field_removed` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}/submit-to-owner.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.operating_items.items.properties.unit_share` | field [unit_share] removed |
| `response_schema_type_removed` | `paths./api/accountant/purchases/purchase-orders.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.low_stock.items.properties.quantity` | type removed (['string'] -> any) |
| `response_schema_items_changed` | `paths./api/accountant/purchases/purchase-orders/{reference}/supplier-invoice.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.invoices.items` | array items schema removed or added |
| `response_schema_type_changed` | `paths./api/accountant/purchases/purchase-orders/{reference}/supplier-invoice.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.invoices.items` | type changed (['array'] -> ['string']) |

_… and 826 more (see the JSON report)._

## Unclassified changes (fail closed) (104)

| Kind | Location | Detail |
|---|---|---|
| `response_schema_anyOf_changed` | `paths./api/accountant/accounting/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `request_schema_allOf_changed` | `paths./api/accountant/accounting/reconciliation/bank-statements.post.requestBody.content.multipart/form-data.schema` | allOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/accountant/expenses/expenses/{reference}.put.responses.200.content.application/json.schema` | allOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/accountant/inventory/waste/records.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/accountant/purchases/direct-purchases.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/accountant/purchases/purchase-orders.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.low_stock.items.properties.quantity` | anyOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/accountant/reports/financial-analysis.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta` | allOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/accountant/tax/tax/periods/{period}/input-invoices.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta` | allOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/accountant/tax/tax/periods/{period}/invoices.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta` | allOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/admin/notifications.get.responses.200.content.application/json.schema` | allOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/admin/subscriptions/{userId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subscription` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/admin/subscriptions/{userId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.user` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/account.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[1].properties.subscription.properties.usage` | anyOf composition added or removed |
| `response_schema_prefixItems_changed` | `paths./api/auth/account.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[1].properties.subscription.properties.usage` | prefixItems added, removed or resized (positions cannot be paired) |
| `response_schema_anyOf_changed` | `paths./api/auth/accountant/meetings/{meetingReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.classification` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.code` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.id` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.name` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.parent_id` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.status` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.subtype` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.type` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.version` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.classification` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.code` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.name` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.parent_id` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subtype` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.type` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.version` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.classification` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.code` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.name` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.parent_id` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subtype` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.type` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/accounts/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.version` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/bootstrap.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.detail.properties.caps` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/auth/login.post.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition changed (unclassified rewrite) |
| `response_schema_anyOf_changed` | `paths./api/auth/onboarding/applications.post.responses.201.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/auth/password-recovery/send-code.post.responses.200.content.application/json.schema` | allOf composition added or removed |
| `response_schema_prefixItems_changed` | `paths./api/owner/general/account/subscription/history.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | prefixItems added, removed or resized (positions cannot be paired) |
| `response_schema_anyOf_changed` | `paths./api/owner/general/subscriptions.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/owner/inventory/waste/records.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/owner/payroll/payroll/runs/{id}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | allOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/owner/reports/financial-analysis.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta` | allOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/owner/sales/invoices/{id}.get.responses.200.content.application/json.schema` | allOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/owner/tax/tax/periods/{period}/input-invoices.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta` | allOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/owner/tax/tax/periods/{period}/invoices.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta` | allOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/owner/tax/tax/periods/{period}/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/account.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[1].properties.subscription.properties.usage` | anyOf composition added or removed |
| `response_schema_prefixItems_changed` | `paths./api/v1/account.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[1].properties.subscription.properties.usage` | prefixItems added, removed or resized (positions cannot be paired) |
| `response_schema_prefixItems_changed` | `paths./api/v1/account/subscription/history.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | prefixItems added, removed or resized (positions cannot be paired) |
| `response_schema_anyOf_changed` | `paths./api/v1/accountant/meetings/{meetingReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.classification` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.code` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.id` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.name` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.parent_id` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.status` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.subtype` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.type` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.version` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.classification` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.code` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.name` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.parent_id` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subtype` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.type` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.version` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.classification` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.code` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.name` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.parent_id` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subtype` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.type` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/accounts/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.version` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/auth/login.post.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition changed (unclassified rewrite) |
| `response_schema_anyOf_changed` | `paths./api/v1/bootstrap.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.detail.properties.caps` | anyOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/v1/expenses/{reference}.put.responses.200.content.application/json.schema` | allOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/v1/financial-analysis.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta` | allOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/v1/identity/password-recovery/send-code.post.responses.200.content.application/json.schema` | allOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/v1/invoices/{id}.get.responses.200.content.application/json.schema` | allOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/journal-entries/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/onboarding/applications.post.responses.201.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/v1/payroll/runs/{id}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | allOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/v1/platform/notifications.get.responses.200.content.application/json.schema` | allOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/platform/subscriptions/{userId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subscription` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/platform/subscriptions/{userId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.user` | anyOf composition added or removed |
| `request_schema_allOf_changed` | `paths./api/v1/reconciliation/bank-statements.post.requestBody.content.multipart/form-data.schema` | allOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/subscriptions.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/v1/tax/periods/{period}/input-invoices.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta` | allOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/v1/tax/periods/{period}/invoices.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta` | allOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/tax/periods/{period}/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/waste/records.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |

## Non-breaking changes (1660)

| Kind | Location | Detail |
|---|---|---|
| `component_schema_required_field_added` | `components.schemas.AccountantAssignmentResource.properties.status` | new REQUIRED field [status] |
| `component_schema_required_field_added` | `components.schemas.AccountantOperationalDashboardResource.properties.alerts` | new REQUIRED field [alerts] |
| `component_schema_required_field_added` | `components.schemas.AccountantOperationalDashboardResource.properties.analytics` | new REQUIRED field [analytics] |
| `component_schema_field_added` | `components.schemas.AccountantOperationalDashboardResource.properties.branch_scope` | new optional field [branch_scope] |
| `component_schema_required_field_added` | `components.schemas.AccountantOperationalDashboardResource.properties.company` | new REQUIRED field [company] |
| `component_schema_required_field_added` | `components.schemas.AccountantOperationalDashboardResource.properties.company_name` | new REQUIRED field [company_name] |
| `component_schema_required_field_added` | `components.schemas.AccountantOperationalDashboardResource.properties.financial_indicators_exact` | new REQUIRED field [financial_indicators_exact] |
| `component_schema_constraint_widened` | `components.schemas.AddPricingMaterialRequest.properties.unit_cost` | [minimum] 0 -> None |
| `component_schema_enum_value_added` | `components.schemas.AdminNotificationType` | newly accepted enum value |
| `component_schema_required_field_added` | `components.schemas.AssetDepreciationEntry.properties.posting_source_reference` | new REQUIRED field [posting_source_reference] |
| `component_schema_required_field_added` | `components.schemas.AssetResource.properties.acquisition_journal_reference` | new REQUIRED field [acquisition_journal_reference] |
| `component_schema_required_field_added` | `components.schemas.AssetResource.properties.acquisition_source` | new REQUIRED field [acquisition_source] |
| `component_schema_required_field_added` | `components.schemas.AssetResource.properties.disposal_gain_loss` | new REQUIRED field [disposal_gain_loss] |
| `component_schema_required_field_added` | `components.schemas.AssetResource.properties.disposal_value` | new REQUIRED field [disposal_value] |
| `component_schema_required_field_added` | `components.schemas.AssetResource.properties.disposed_at` | new REQUIRED field [disposed_at] |
| `component_schema_required_field_added` | `components.schemas.AssetResource.properties.purchase_document_url` | new REQUIRED field [purchase_document_url] |
| `shared_component_added` | `components.schemas.BankStatementLineRuleSet` | component [schemas.BankStatementLineRuleSet] added |
| `component_schema_required_field_added` | `components.schemas.ClosingTaskResource.properties.action_link` | new REQUIRED field [action_link] |
| `component_schema_field_added` | `components.schemas.CollectSalesInvoiceRequest.properties.proof_reference` | new optional field [proof_reference] |
| `shared_component_added` | `components.schemas.ConfirmImportMappingRequest` | component [schemas.ConfirmImportMappingRequest] added |
| `component_schema_field_added` | `components.schemas.ConfirmSupplementalTaxDocumentRequest.properties.tax_treatment` | new optional field [tax_treatment] |
| `component_schema_constraint_widened` | `components.schemas.CreateCustomerRequest.properties.commercial_registration_no` | [maxLength] 50 -> None |
| `component_schema_constraint_widened` | `components.schemas.CreateCustomerRequest.properties.tax_number` | [maxLength] 50 -> None |
| `shared_component_added` | `components.schemas.CreateExportRequest` | component [schemas.CreateExportRequest] added |
| `component_schema_field_added` | `components.schemas.CreateOrganizationUserRequest.properties.permissions` | new optional field [permissions] |
| `component_schema_field_added` | `components.schemas.CreatePurchaseReturnRequest.properties.lines.items.properties.direct_purchase_line_reference` | new optional field [direct_purchase_line_reference] |
| `component_schema_field_added` | `components.schemas.CreatePurchaseReturnRequest.properties.lines.items.properties.goods_receipt_line_reference` | new optional field [goods_receipt_line_reference] |
| `component_schema_field_became_optional` | `components.schemas.CreatePurchaseReturnRequest.properties.lines.items.properties.product_id` | field [product_id] became optional |
| `component_schema_nullability_added` | `components.schemas.CreatePurchaseReturnRequest.properties.lines.items.properties.product_id` | type now also accepts/returns null |
| `component_schema_field_became_optional` | `components.schemas.CreatePurchaseReturnRequest.properties.lines.items.properties.unit_price` | field [unit_price] became optional |
| `component_schema_nullability_added` | `components.schemas.CreatePurchaseReturnRequest.properties.lines.items.properties.unit_price` | type now also accepts/returns null |
| `component_schema_field_added` | `components.schemas.CreatePurchaseReturnRequest.properties.notes` | new optional field [notes] |
| `component_schema_required_field_added` | `components.schemas.DepreciationRunResource.properties.journal_preview` | new REQUIRED field [journal_preview] |
| `shared_component_added` | `components.schemas.ExpenseStatus` | component [schemas.ExpenseStatus] added |
| `component_schema_field_became_optional` | `components.schemas.InitializeZakatSessionRequest.properties.items` | field [items] became optional |
| `component_schema_required_field_added` | `components.schemas.IntegrationConnectionResource.properties.auto_create_products` | new REQUIRED field [auto_create_products] |
| `component_schema_required_field_added` | `components.schemas.IntegrationConnectionResource.properties.auto_map_branches` | new REQUIRED field [auto_map_branches] |
| `component_schema_field_added` | `components.schemas.IssueTokenRequest.properties.device_token` | new optional field [device_token] |
| `component_schema_required_field_added` | `components.schemas.JournalEntryDTO.properties.amended` | new REQUIRED field [amended] |
| `component_schema_required_field_added` | `components.schemas.JournalEntryDTO.properties.created_by_reference` | new REQUIRED field [created_by_reference] |
| `component_schema_required_field_added` | `components.schemas.JournalEntryDTO.properties.entry_number` | new REQUIRED field [entry_number] |
| `component_schema_required_field_added` | `components.schemas.JournalEntryDTO.properties.files` | new REQUIRED field [files] |
| `component_schema_required_field_added` | `components.schemas.JournalEntryDTO.properties.id` | new REQUIRED field [id] |
| `component_schema_required_field_added` | `components.schemas.JournalEntryDTO.properties.pending_amendment` | new REQUIRED field [pending_amendment] |
| `component_schema_required_field_added` | `components.schemas.JournalEntryDTO.properties.posted_at` | new REQUIRED field [posted_at] |
| `component_schema_required_field_added` | `components.schemas.JournalEntryDTO.properties.posted_by_reference` | new REQUIRED field [posted_by_reference] |
| `component_schema_required_field_added` | `components.schemas.JournalEntryDTO.properties.reversal_of_id` | new REQUIRED field [reversal_of_id] |
| `component_schema_required_field_added` | `components.schemas.JournalEntryDTO.properties.reversal_reference` | new REQUIRED field [reversal_reference] |
| `component_schema_required_field_added` | `components.schemas.JournalEntryDTO.properties.updated_at` | new REQUIRED field [updated_at] |
| `component_schema_required_field_added` | `components.schemas.JournalEntryDTO.properties.version` | new REQUIRED field [version] |
| `component_schema_constraint_widened` | `components.schemas.LoginRequest.properties.device_token` | [maxLength] 255 -> 512 |
| `component_schema_required_field_added` | `components.schemas.OrganizationResource.properties.fiscal_year_start_month` | new REQUIRED field [fiscal_year_start_month] |
| `component_schema_type_changed` | `components.schemas.OrganizationResource.properties.logo_url` | type changed (['null', 'string'] -> ['null']) |
| `component_schema_required_field_added` | `components.schemas.OrganizationResource.properties.vat_filing_frequency` | new REQUIRED field [vat_filing_frequency] |
| `shared_component_added` | `components.schemas.OverrideEffect` | component [schemas.OverrideEffect] added |
| `shared_component_added` | `components.schemas.OwnerDashboardAnalyticsResource` | component [schemas.OwnerDashboardAnalyticsResource] added |
| `component_schema_field_added` | `components.schemas.OwnerDashboardResource.properties.branch_scope` | new optional field [branch_scope] |
| `component_schema_required_field_added` | `components.schemas.Package.properties.duration_unit` | new REQUIRED field [duration_unit] |
| `component_schema_required_field_added` | `components.schemas.Package.properties.duration_value` | new REQUIRED field [duration_value] |
| `component_schema_required_field_added` | `components.schemas.PaginationMeta.properties.max_per_page` | new REQUIRED field [max_per_page] |
| `component_schema_required_field_added` | `components.schemas.PaginationMeta.properties.per_page` | new REQUIRED field [per_page] |
| `component_schema_field_became_optional` | `components.schemas.PaySupplierInvoiceRequest.properties.proof` | field [proof] became optional |
| `component_schema_nullability_added` | `components.schemas.PaySupplierInvoiceRequest.properties.proof` | type now also accepts/returns null |
| `component_schema_field_added` | `components.schemas.PaySupplierInvoiceRequest.properties.proof_reference` | new optional field [proof_reference] |
| `component_schema_field_added` | `components.schemas.PayrollRunResource.properties.gosi` | new optional field [gosi] |
| `component_schema_required_field_added` | `components.schemas.PayrollRunResource.properties.lines.items.properties.gosi_employee_amount` | new REQUIRED field [gosi_employee_amount] |
| `component_schema_nullability_removed` | `components.schemas.PayrollRunResource.properties.lines.items.properties.notes` | type no longer accepts/returns null |
| `component_schema_field_added` | `components.schemas.PayrollRunReviewResource.properties.gosi` | new optional field [gosi] |
| `component_schema_required_field_added` | `components.schemas.PortfolioCompanyResource.properties.closing` | new REQUIRED field [closing] |
| `component_schema_field_added` | `components.schemas.PostMovementRequest.properties.offset_role` | new optional field [offset_role] |
| `component_schema_field_added` | `components.schemas.ProcessExternalSaleRequest.properties.external_sale_id` | new optional field [external_sale_id] |
| `component_schema_field_added` | `components.schemas.ProcessExternalSaleRequest.properties.items.items.properties.external_line_key` | new optional field [external_line_key] |
| `component_schema_field_added` | `components.schemas.ProcessExternalSaleRequest.properties.provider` | new optional field [provider] |
| `component_schema_required_field_added` | `components.schemas.PurchaseReturnResource.properties.accounting_posting` | new REQUIRED field [accounting_posting] |
| `component_schema_required_field_added` | `components.schemas.PurchaseReturnResource.properties.applied_to_invoice_amount` | new REQUIRED field [applied_to_invoice_amount] |
| `component_schema_required_field_added` | `components.schemas.PurchaseReturnResource.properties.approved_at` | new REQUIRED field [approved_at] |
| `component_schema_required_field_added` | `components.schemas.PurchaseReturnResource.properties.approved_by` | new REQUIRED field [approved_by] |
| `component_schema_required_field_added` | `components.schemas.PurchaseReturnResource.properties.created_by` | new REQUIRED field [created_by] |
| `component_schema_required_field_added` | `components.schemas.PurchaseReturnResource.properties.inventory_dispositions` | new REQUIRED field [inventory_dispositions] |
| `component_schema_required_field_added` | `components.schemas.PurchaseReturnResource.properties.notes` | new REQUIRED field [notes] |
| `component_schema_required_field_added` | `components.schemas.PurchaseReturnResource.properties.return_reason` | new REQUIRED field [return_reason] |
| `component_schema_required_field_added` | `components.schemas.PurchaseReturnResource.properties.supplier_credit_amount` | new REQUIRED field [supplier_credit_amount] |
| `component_schema_field_added` | `components.schemas.RecordAccountantCommentaryRequest.properties.custom_sections` | new optional field [custom_sections] |
| `component_schema_field_added` | `components.schemas.RecordAccountantCommentaryRequest.properties.section_order` | new optional field [section_order] |
| `component_schema_field_added` | `components.schemas.RecordCustomerCollectionRequest.properties.proof` | new optional field [proof] |
| `component_schema_field_added` | `components.schemas.RecordCustomerCollectionRequest.properties.proof_reference` | new optional field [proof_reference] |
| `shared_component_added` | `components.schemas.RecordExpensePaymentRequest` | component [schemas.RecordExpensePaymentRequest] added |
| `shared_component_added` | `components.schemas.RecordManualVatFilingRequest` | component [schemas.RecordManualVatFilingRequest] added |
| `component_schema_constraint_widened` | `components.schemas.RegisterApplicationRequest.properties.password` | [minLength] 8 -> None |
| `component_schema_field_became_optional` | `components.schemas.RegisterApplicationRequest.properties.password` | field [password] became optional |
| `component_schema_nullability_added` | `components.schemas.RegisterApplicationRequest.properties.password` | type now also accepts/returns null |
| `component_schema_constraint_widened` | `components.schemas.RegisterApplicationRequest.properties.password_confirmation` | [minLength] 8 -> None |
| `component_schema_field_became_optional` | `components.schemas.RegisterApplicationRequest.properties.password_confirmation` | field [password_confirmation] became optional |
| `component_schema_nullability_added` | `components.schemas.RegisterApplicationRequest.properties.password_confirmation` | type now also accepts/returns null |
| `component_schema_required_field_added` | `components.schemas.RegistrationApplication.properties.terms_version` | new REQUIRED field [terms_version] |
| `shared_component_added` | `components.schemas.RejectRegistrationApplicationRequest` | component [schemas.RejectRegistrationApplicationRequest] added |
| `component_schema_field_added` | `components.schemas.RenewSubscriptionRequest.properties.proof_reference` | new optional field [proof_reference] |
| `component_schema_constraint_widened` | `components.schemas.ResetPasswordRequest.properties.password` | [minLength] 8 -> None |
| `component_schema_constraint_widened` | `components.schemas.ResetPasswordRequest.properties.password_confirmation` | [minLength] 8 -> None |
| `component_schema_field_added` | `components.schemas.ResubmitExpenseRequest.properties.document_reference` | new optional field [document_reference] |
| `component_schema_required_field_added` | `components.schemas.ReturnNoteResource.anyOf[0].properties.is_tax_document` | new REQUIRED field [is_tax_document] |
| `component_schema_required_field_added` | `components.schemas.ReturnNoteResource.anyOf[0].properties.return_reason` | new REQUIRED field [return_reason] |
| `component_schema_required_field_added` | `components.schemas.ReturnNoteResource.anyOf[0].properties.status` | new REQUIRED field [status] |
| `component_schema_required_field_added` | `components.schemas.ReturnNoteResource.anyOf[0].properties.tax_document_number` | new REQUIRED field [tax_document_number] |
| `component_schema_required_field_added` | `components.schemas.ReturnNoteResource.anyOf[1].properties.is_tax_document` | new REQUIRED field [is_tax_document] |
| `component_schema_required_field_added` | `components.schemas.ReturnNoteResource.anyOf[1].properties.return_reason` | new REQUIRED field [return_reason] |
| `component_schema_required_field_added` | `components.schemas.ReturnNoteResource.anyOf[1].properties.status` | new REQUIRED field [status] |
| `component_schema_required_field_added` | `components.schemas.ReturnNoteResource.anyOf[1].properties.tax_document_number` | new REQUIRED field [tax_document_number] |
| `component_schema_required_field_added` | `components.schemas.SalesReturnResource.properties.accounting_posting` | new REQUIRED field [accounting_posting] |
| `component_schema_required_field_added` | `components.schemas.SalesReturnResource.properties.approved_at` | new REQUIRED field [approved_at] |
| `component_schema_required_field_added` | `components.schemas.SalesReturnResource.properties.approved_by` | new REQUIRED field [approved_by] |
| `component_schema_required_field_added` | `components.schemas.SalesReturnResource.properties.branch_id` | new REQUIRED field [branch_id] |
| `component_schema_required_field_added` | `components.schemas.SalesReturnResource.properties.cancelled_at` | new REQUIRED field [cancelled_at] |
| `component_schema_required_field_added` | `components.schemas.SalesReturnResource.properties.cancelled_by` | new REQUIRED field [cancelled_by] |
| `component_schema_required_field_added` | `components.schemas.SalesReturnResource.properties.created_by` | new REQUIRED field [created_by] |
| `component_schema_required_field_added` | `components.schemas.SalesReturnResource.properties.customer_credit_amount` | new REQUIRED field [customer_credit_amount] |
| `component_schema_required_field_added` | `components.schemas.SalesReturnResource.properties.receivable_adjustment_amount` | new REQUIRED field [receivable_adjustment_amount] |
| `shared_component_added` | `components.schemas.SavePlatformPageVersionRequest` | component [schemas.SavePlatformPageVersionRequest] added |
| `shared_component_added` | `components.schemas.SendAnnouncementRequest` | component [schemas.SendAnnouncementRequest] added |
| `component_schema_field_added` | `components.schemas.SetExpensePaymentStatusRequest.properties.payment_date` | new optional field [payment_date] |
| `component_schema_field_added` | `components.schemas.SetExpensePaymentStatusRequest.properties.proof_reference` | new optional field [proof_reference] |
| `component_schema_field_added` | `components.schemas.SetExpensePaymentStatusRequest.properties.transfer_reference` | new optional field [transfer_reference] |
| `component_schema_required_field_added` | `components.schemas.StockMovement.properties.offset_role` | new REQUIRED field [offset_role] |
| `component_schema_field_became_optional` | `components.schemas.StoreAccountantRequest.properties.password` | field [password] became optional |
| `component_schema_nullability_added` | `components.schemas.StoreAccountantRequest.properties.password` | type now also accepts/returns null |
| `component_schema_enum_value_added` | `components.schemas.StoreAccountantRequest.properties.status` | newly accepted enum value |
| `component_schema_field_became_optional` | `components.schemas.StoreAccountantRequest.properties.status` | field [status] became optional |
| `component_schema_nullability_added` | `components.schemas.StoreAccountantRequest.properties.status` | type now also accepts/returns null |
| `component_schema_field_added` | `components.schemas.StoreAssetRequest.properties.acquisition_offset_role` | new optional field [acquisition_offset_role] |
| `component_schema_field_added` | `components.schemas.StoreAssetRequest.properties.acquisition_posting_date` | new optional field [acquisition_posting_date] |
| `component_schema_field_added` | `components.schemas.StoreAssetRequest.properties.purchase_document` | new optional field [purchase_document] |
| `component_schema_field_added` | `components.schemas.StoreBranchRequest.properties.status` | new optional field [status] |
| `component_schema_field_added` | `components.schemas.StoreExpenseRequest.properties.document_reference` | new optional field [document_reference] |
| `shared_component_added` | `components.schemas.StorePlatformRoleRequest` | component [schemas.StorePlatformRoleRequest] added |
| `component_schema_field_became_optional` | `components.schemas.StoreSubscriptionPackageRequest.properties.duration_in_days` | field [duration_in_days] became optional |
| `component_schema_field_added` | `components.schemas.StoreSubscriptionPackageRequest.properties.duration_unit` | new optional field [duration_unit] |
| `component_schema_field_added` | `components.schemas.StoreSubscriptionPackageRequest.properties.duration_value` | new optional field [duration_value] |
| `component_schema_field_added` | `components.schemas.StoreSubscriptionPackageRequest.properties.max_branches` | new optional field [max_branches] |
| `component_schema_field_added` | `components.schemas.StoreSubscriptionPackageRequest.properties.max_users` | new optional field [max_users] |
| `component_schema_required_field_added` | `components.schemas.SubscriptionPackageResource.properties.duration_unit` | new REQUIRED field [duration_unit] |
| `component_schema_required_field_added` | `components.schemas.SubscriptionPackageResource.properties.duration_value` | new REQUIRED field [duration_value] |
| `component_schema_required_field_added` | `components.schemas.SupplementalTaxDocumentResource.properties.tax_treatment` | new REQUIRED field [tax_treatment] |
| `component_schema_required_field_added` | `components.schemas.SupplementalTaxDocumentResource.properties.vat_rate_review_required` | new REQUIRED field [vat_rate_review_required] |
| `component_schema_required_field_added` | `components.schemas.SupplementalTaxDocumentResource.properties.vat_review_threshold` | new REQUIRED field [vat_review_threshold] |
| `component_schema_required_field_added` | `components.schemas.SupplierAdminResource.properties.can_edit` | new REQUIRED field [can_edit] |
| `component_schema_required_field_added` | `components.schemas.SupplierAdminResource.properties.is_operator` | new REQUIRED field [is_operator] |
| `component_schema_required_field_added` | `components.schemas.SupplierAdminResource.properties.tenant_name` | new REQUIRED field [tenant_name] |
| `component_schema_required_field_added` | `components.schemas.SupplierInvoice.properties.branch_id` | new REQUIRED field [branch_id] |
| `component_schema_required_field_added` | `components.schemas.SupplierInvoice.properties.price_variance_amount` | new REQUIRED field [price_variance_amount] |
| `component_schema_required_field_added` | `components.schemas.SupplierResource.properties.creation_source` | new REQUIRED field [creation_source] |
| `component_schema_field_added` | `components.schemas.SupplierResource.properties.paid_invoices_count` | new optional field [paid_invoices_count] |
| `component_schema_field_added` | `components.schemas.SupplierResource.properties.partially_paid_invoices_count` | new optional field [partially_paid_invoices_count] |
| `component_schema_type_added` | `components.schemas.SupplierResource.properties.supplied_items.items` | type added (any -> ['string']) |
| `component_schema_field_added` | `components.schemas.SupplierResource.properties.unpaid_invoices_count` | new optional field [unpaid_invoices_count] |
| `component_schema_required_field_added` | `components.schemas.TaxInvoiceResource.properties.invoice_date` | new REQUIRED field [invoice_date] |
| `component_schema_field_added` | `components.schemas.UpdateBranchRequest.properties.version` | new optional field [version] |
| `component_schema_constraint_widened` | `components.schemas.UpdateCustomerRequest.properties.commercial_registration_no` | [maxLength] 50 -> None |
| `component_schema_constraint_widened` | `components.schemas.UpdateCustomerRequest.properties.tax_number` | [maxLength] 50 -> None |
| `component_schema_field_added` | `components.schemas.UpdateIntegrationConnectionRequest.properties.auto_create_products` | new optional field [auto_create_products] |
| `component_schema_field_added` | `components.schemas.UpdateIntegrationConnectionRequest.properties.auto_map_branches` | new optional field [auto_map_branches] |
| `component_schema_field_added` | `components.schemas.UpdateOrganizationRequest.properties.fiscal_year_start_month` | new optional field [fiscal_year_start_month] |
| `component_schema_field_added` | `components.schemas.UpdateOrganizationRequest.properties.vat_filing_frequency` | new optional field [vat_filing_frequency] |
| `component_schema_field_added` | `components.schemas.UpdateSubscriptionPackageRequest.properties.duration_unit` | new optional field [duration_unit] |
| `component_schema_field_added` | `components.schemas.UpdateSubscriptionPackageRequest.properties.duration_value` | new optional field [duration_value] |
| `component_schema_enum_value_added` | `components.schemas.UpdateSupplierStatusRequest.properties.status` | newly accepted enum value |
| `shared_component_added` | `components.schemas.UploadImportRequest` | component [schemas.UploadImportRequest] added |
| `component_schema_required_field_added` | `components.schemas.VatReturnPreparationResource.properties.totals.properties.net_position` | new REQUIRED field [net_position] |
| `component_schema_required_field_added` | `components.schemas.VatReturnResource.properties.net_position` | new REQUIRED field [net_position] |
| `component_schema_required_field_added` | `components.schemas.VatSummaryResource.properties.net_position` | new REQUIRED field [net_position] |
| `component_schema_field_added` | `components.schemas.VerifyRegistrationPaymentRequest.properties.force` | new optional field [force] |
| `shared_component_added` | `components.schemas.ZakatAccountMappingRuleSet` | component [schemas.ZakatAccountMappingRuleSet] added |
| `component_schema_required_field_added` | `components.schemas.ZakatSessionResource.properties.posting_requested_at` | new REQUIRED field [posting_requested_at] |
| `request_media_type_added` | `paths./api/accountant/accounting/assets.post.requestBody.content.multipart/form-data` | request media type [multipart/form-data] added |
| `operation_added` | `paths./api/accountant/accounting/assets/{asset}/dispose.post` | POST /api/accountant/accounting/assets/{asset}/dispose added to the contract |
| `operation_added` | `paths./api/accountant/accounting/assets/{asset}/link-acquisition.post` | POST /api/accountant/accounting/assets/{asset}/link-acquisition added to the contract |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.max_per_page` | new REQUIRED field [max_per_page] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.per_page` | new REQUIRED field [per_page] |
| `operation_added` | `paths./api/accountant/accounting/financial-periods/open.get` | GET /api/accountant/accounting/financial-periods/open added to the contract |
| `response_schema_type_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.amended` | new REQUIRED field [amended] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.amount` | new REQUIRED field [amount] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.attachments` | new REQUIRED field [attachments] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.branch_id` | new REQUIRED field [branch_id] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.can_amend` | new REQUIRED field [can_amend] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.can_approve` | new REQUIRED field [can_approve] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.company_id` | new REQUIRED field [company_id] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.created_at` | new REQUIRED field [created_at] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.created_by_reference` | new REQUIRED field [created_by_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.description` | new REQUIRED field [description] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.document_date` | new REQUIRED field [document_date] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.entry_number` | new REQUIRED field [entry_number] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.files` | new REQUIRED field [files] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.fiscal_period_id` | new REQUIRED field [fiscal_period_id] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.lines` | new REQUIRED field [lines] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.owner_requests` | new REQUIRED field [owner_requests] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.pending_amendment` | new REQUIRED field [pending_amendment] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.posted_at` | new REQUIRED field [posted_at] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.posted_by_reference` | new REQUIRED field [posted_by_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.posting_date` | new REQUIRED field [posting_date] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.public_reference` | new REQUIRED field [public_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.ref_id` | new REQUIRED field [ref_id] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.ref_type` | new REQUIRED field [ref_type] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.reversal_of_id` | new REQUIRED field [reversal_of_id] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.reversal_reference` | new REQUIRED field [reversal_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.source_reference` | new REQUIRED field [source_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.source_type` | new REQUIRED field [source_type] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.status` | new REQUIRED field [status] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.status_category` | new REQUIRED field [status_category] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.total_credit` | new REQUIRED field [total_credit] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.total_debit` | new REQUIRED field [total_debit] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.transaction_type` | new REQUIRED field [transaction_type] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.updated_at` | new REQUIRED field [updated_at] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.version` | new REQUIRED field [version] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.max_per_page` | new REQUIRED field [max_per_page] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.per_page` | new REQUIRED field [per_page] |
| `request_schema_constraint_widened` | `paths./api/accountant/accounting/journal-entries.post.requestBody.content.application/json.schema.properties.lines.items.properties.credit` | [minimum] 0 -> None |
| `request_schema_constraint_widened` | `paths./api/accountant/accounting/journal-entries.post.requestBody.content.application/json.schema.properties.lines.items.properties.debit` | [minimum] 0 -> None |
| `response_status_added` | `paths./api/accountant/accounting/journal-entries.post.responses.200` | response [200] added to the contract |
| `operation_added` | `paths./api/accountant/accounting/journal-entries/{id}/amendments/{amendment_id}/reject.post` | POST /api/accountant/accounting/journal-entries/{id}/amendments/{amendment_id}/reject added to the contract |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/approve.post.responses.200.content.application/json.schema.properties.data.properties.amended` | new REQUIRED field [amended] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/approve.post.responses.200.content.application/json.schema.properties.data.properties.created_by_reference` | new REQUIRED field [created_by_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/approve.post.responses.200.content.application/json.schema.properties.data.properties.entry_number` | new REQUIRED field [entry_number] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/approve.post.responses.200.content.application/json.schema.properties.data.properties.files` | new REQUIRED field [files] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/approve.post.responses.200.content.application/json.schema.properties.data.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/approve.post.responses.200.content.application/json.schema.properties.data.properties.pending_amendment` | new REQUIRED field [pending_amendment] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/approve.post.responses.200.content.application/json.schema.properties.data.properties.posted_at` | new REQUIRED field [posted_at] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/approve.post.responses.200.content.application/json.schema.properties.data.properties.posted_by_reference` | new REQUIRED field [posted_by_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/approve.post.responses.200.content.application/json.schema.properties.data.properties.reversal_of_id` | new REQUIRED field [reversal_of_id] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/approve.post.responses.200.content.application/json.schema.properties.data.properties.reversal_reference` | new REQUIRED field [reversal_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/approve.post.responses.200.content.application/json.schema.properties.data.properties.updated_at` | new REQUIRED field [updated_at] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/approve.post.responses.200.content.application/json.schema.properties.data.properties.version` | new REQUIRED field [version] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/cancel.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.amended` | new REQUIRED field [amended] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/cancel.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.created_by_reference` | new REQUIRED field [created_by_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/cancel.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.entry_number` | new REQUIRED field [entry_number] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/cancel.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.files` | new REQUIRED field [files] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/cancel.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/cancel.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.pending_amendment` | new REQUIRED field [pending_amendment] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/cancel.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.posted_at` | new REQUIRED field [posted_at] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/cancel.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.posted_by_reference` | new REQUIRED field [posted_by_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/cancel.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.reversal_of_id` | new REQUIRED field [reversal_of_id] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/cancel.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.reversal_reference` | new REQUIRED field [reversal_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/cancel.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.updated_at` | new REQUIRED field [updated_at] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/cancel.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.version` | new REQUIRED field [version] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/review.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.amended` | new REQUIRED field [amended] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/review.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.created_by_reference` | new REQUIRED field [created_by_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/review.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.entry_number` | new REQUIRED field [entry_number] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/review.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.files` | new REQUIRED field [files] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/review.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/review.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.pending_amendment` | new REQUIRED field [pending_amendment] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/review.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.posted_at` | new REQUIRED field [posted_at] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/review.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.posted_by_reference` | new REQUIRED field [posted_by_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/review.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.reversal_of_id` | new REQUIRED field [reversal_of_id] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/review.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.reversal_reference` | new REQUIRED field [reversal_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/review.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.updated_at` | new REQUIRED field [updated_at] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/review.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.version` | new REQUIRED field [version] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.amended` | new REQUIRED field [amended] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.created_by_reference` | new REQUIRED field [created_by_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.entry_number` | new REQUIRED field [entry_number] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.files` | new REQUIRED field [files] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.pending_amendment` | new REQUIRED field [pending_amendment] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.posted_at` | new REQUIRED field [posted_at] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.posted_by_reference` | new REQUIRED field [posted_by_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.reversal_of_id` | new REQUIRED field [reversal_of_id] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.reversal_reference` | new REQUIRED field [reversal_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.updated_at` | new REQUIRED field [updated_at] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.version` | new REQUIRED field [version] |
| `request_schema_constraint_widened` | `paths./api/accountant/accounting/journal-entries/{reference}.put.requestBody.content.application/json.schema.properties.lines.items.properties.credit` | [minimum] 0 -> None |
| `request_schema_constraint_widened` | `paths./api/accountant/accounting/journal-entries/{reference}.put.requestBody.content.application/json.schema.properties.lines.items.properties.debit` | [minimum] 0 -> None |
| `request_schema_field_added` | `paths./api/accountant/accounting/journal-entries/{reference}.put.requestBody.content.application/json.schema.properties.version` | new optional field [version] |
| `operation_added` | `paths./api/accountant/accounting/journal-entries/{reference}/files.get` | GET /api/accountant/accounting/journal-entries/{reference}/files added to the contract |
| `operation_added` | `paths./api/accountant/accounting/journal-entries/{reference}/files.post` | POST /api/accountant/accounting/journal-entries/{reference}/files added to the contract |
| `operation_added` | `paths./api/accountant/accounting/journal-entries/{reference}/files/{fileReference}.get` | GET /api/accountant/accounting/journal-entries/{reference}/files/{fileReference} added to the contract |
| `operation_added` | `paths./api/accountant/accounting/journal-entries/{reference}/reverse.post` | POST /api/accountant/accounting/journal-entries/{reference}/reverse added to the contract |
| `optional_parameter_added` | `paths./api/accountant/accounting/posting-requests.get.parameters.source_reference` | optional parameter [source_reference] (in query) added |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/posting-requests/reprocess.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.outbox_failed` | new REQUIRED field [outbox_failed] |
| `request_schema_type_removed` | `paths./api/accountant/accounting/reconciliation/bank-statements.post.requestBody.content.multipart/form-data.schema` | type removed (['object'] -> any) |
| `request_body_became_optional` | `paths./api/accountant/accounting/reconciliation/bank-statements.post.requestBody.required` | request body became optional |
| `operation_added` | `paths./api/accountant/dashboard/accountant/notifications.get` | GET /api/accountant/dashboard/accountant/notifications added to the contract |
| `optional_parameter_added` | `paths./api/accountant/dashboard/accountant/operational.get.parameters.branch_reference` | optional parameter [branch_reference] (in query) added |
| `optional_parameter_added` | `paths./api/accountant/dashboard/accountant/operational.get.parameters.branch_scope` | optional parameter [branch_scope] (in query) added |
| `operation_added` | `paths./api/accountant/dashboard/actions.get` | GET /api/accountant/dashboard/actions added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/exports.get` | GET /api/accountant/data-exchange/exports added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/exports.post` | POST /api/accountant/data-exchange/exports added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/exports/catalogue.get` | GET /api/accountant/data-exchange/exports/catalogue added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/exports/preview.post` | POST /api/accountant/data-exchange/exports/preview added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/exports/{export}.get` | GET /api/accountant/data-exchange/exports/{export} added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/exports/{export}/approve.post` | POST /api/accountant/data-exchange/exports/{export}/approve added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/exports/{export}/cancel.post` | POST /api/accountant/data-exchange/exports/{export}/cancel added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/exports/{export}/download.get` | GET /api/accountant/data-exchange/exports/{export}/download added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/exports/{export}/metrics.get` | GET /api/accountant/data-exchange/exports/{export}/metrics added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/exports/{export}/progress.get` | GET /api/accountant/data-exchange/exports/{export}/progress added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/exports/{export}/reject.post` | POST /api/accountant/data-exchange/exports/{export}/reject added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/exports/{export}/retry.post` | POST /api/accountant/data-exchange/exports/{export}/retry added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/imports.get` | GET /api/accountant/data-exchange/imports added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/imports.post` | POST /api/accountant/data-exchange/imports added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/imports/targets.get` | GET /api/accountant/data-exchange/imports/targets added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/imports/{import}.get` | GET /api/accountant/data-exchange/imports/{import} added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/imports/{import}/analysis.get` | GET /api/accountant/data-exchange/imports/{import}/analysis added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/imports/{import}/analyze.post` | POST /api/accountant/data-exchange/imports/{import}/analyze added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/imports/{import}/approve.post` | POST /api/accountant/data-exchange/imports/{import}/approve added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/imports/{import}/cancel.post` | POST /api/accountant/data-exchange/imports/{import}/cancel added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/imports/{import}/correction-file.get` | GET /api/accountant/data-exchange/imports/{import}/correction-file added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/imports/{import}/errors.get` | GET /api/accountant/data-exchange/imports/{import}/errors added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/imports/{import}/execute.post` | POST /api/accountant/data-exchange/imports/{import}/execute added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/imports/{import}/impact.get` | GET /api/accountant/data-exchange/imports/{import}/impact added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/imports/{import}/mapping.get` | GET /api/accountant/data-exchange/imports/{import}/mapping added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/imports/{import}/mapping.put` | PUT /api/accountant/data-exchange/imports/{import}/mapping added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/imports/{import}/metrics.get` | GET /api/accountant/data-exchange/imports/{import}/metrics added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/imports/{import}/preview.get` | GET /api/accountant/data-exchange/imports/{import}/preview added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/imports/{import}/progress.get` | GET /api/accountant/data-exchange/imports/{import}/progress added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/imports/{import}/reject.post` | POST /api/accountant/data-exchange/imports/{import}/reject added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/imports/{import}/retry.post` | POST /api/accountant/data-exchange/imports/{import}/retry added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/imports/{import}/rollback.post` | POST /api/accountant/data-exchange/imports/{import}/rollback added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/imports/{import}/submit.post` | POST /api/accountant/data-exchange/imports/{import}/submit added to the contract |
| `operation_added` | `paths./api/accountant/data-exchange/imports/{import}/validate.post` | POST /api/accountant/data-exchange/imports/{import}/validate added to the contract |
| `optional_parameter_added` | `paths./api/accountant/expenses/expenses.get.parameters.page` | optional parameter [page] (in query) added |
| `optional_parameter_added` | `paths./api/accountant/expenses/expenses.get.parameters.per_page` | optional parameter [per_page] (in query) added |
| `optional_parameter_added` | `paths./api/accountant/expenses/expenses.get.parameters.status` | optional parameter [status] (in query) added |
| `response_schema_field_added` | `paths./api/accountant/expenses/expenses.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta` | new optional field [meta] |
| `operation_added` | `paths./api/accountant/expenses/expenses/payments/{payment}/approve.post` | POST /api/accountant/expenses/expenses/payments/{payment}/approve added to the contract |
| `operation_added` | `paths./api/accountant/expenses/expenses/payments/{payment}/proof.get` | GET /api/accountant/expenses/expenses/payments/{payment}/proof added to the contract |
| `operation_added` | `paths./api/accountant/expenses/expenses/payments/{payment}/reject.post` | POST /api/accountant/expenses/expenses/payments/{payment}/reject added to the contract |
| `response_schema_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | new optional field [items] |
| `request_schema_field_added` | `paths./api/accountant/expenses/expenses/{reference}.put.requestBody.content.application/json.schema.properties.invoice_date` | new optional field [invoice_date] |
| `request_schema_field_added` | `paths./api/accountant/expenses/expenses/{reference}.put.requestBody.content.application/json.schema.properties.invoice_number` | new optional field [invoice_number] |
| `request_schema_field_became_optional` | `paths./api/accountant/expenses/expenses/{reference}.put.requestBody.content.application/json.schema.properties.total_amount` | field [total_amount] became optional |
| `request_schema_nullability_added` | `paths./api/accountant/expenses/expenses/{reference}.put.requestBody.content.application/json.schema.properties.total_amount` | type now also accepts/returns null |
| `request_schema_field_became_optional` | `paths./api/accountant/expenses/expenses/{reference}.put.requestBody.content.application/json.schema.properties.vat_amount` | field [vat_amount] became optional |
| `request_schema_nullability_added` | `paths./api/accountant/expenses/expenses/{reference}.put.requestBody.content.application/json.schema.properties.vat_amount` | type now also accepts/returns null |
| `response_schema_type_added` | `paths./api/accountant/expenses/expenses/{reference}.put.responses.200.content.application/json.schema` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.put.responses.200.content.application/json.schema.properties.data` | new REQUIRED field [data] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.put.responses.200.content.application/json.schema.properties.message` | new REQUIRED field [message] |
| `operation_added` | `paths./api/accountant/expenses/expenses/{reference}/correct-approved.post` | POST /api/accountant/expenses/expenses/{reference}/correct-approved added to the contract |
| `operation_added` | `paths./api/accountant/expenses/expenses/{reference}/payments.get` | GET /api/accountant/expenses/expenses/{reference}/payments added to the contract |
| `operation_added` | `paths./api/accountant/expenses/expenses/{reference}/payments.post` | POST /api/accountant/expenses/expenses/{reference}/payments added to the contract |
| `operation_added` | `paths./api/accountant/expenses/expenses/{reference}/restore-correction.post` | POST /api/accountant/expenses/expenses/{reference}/restore-correction added to the contract |
| `response_schema_required_field_added` | `paths./api/accountant/general/closing-tasks/{taskId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.action_link` | new REQUIRED field [action_link] |
| `response_schema_required_field_added` | `paths./api/accountant/general/closing-tasks/{taskId}.patch.responses.200.content.application/json.schema.allOf[1].properties.data.properties.action_link` | new REQUIRED field [action_link] |
| `operation_added` | `paths./api/accountant/general/closing-tasks/{taskId}/assign.post` | POST /api/accountant/general/closing-tasks/{taskId}/assign added to the contract |
| `response_schema_required_field_added` | `paths./api/accountant/general/closing-tasks/{taskId}/complete.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.action_link` | new REQUIRED field [action_link] |
| `operation_added` | `paths./api/accountant/general/depreciation-runs.get` | GET /api/accountant/general/depreciation-runs added to the contract |
| `operation_added` | `paths./api/accountant/general/depreciation-runs/{publicReference}/cancel.post` | POST /api/accountant/general/depreciation-runs/{publicReference}/cancel added to the contract |
| `operation_added` | `paths./api/accountant/general/depreciation-runs/{publicReference}/reopen.post` | POST /api/accountant/general/depreciation-runs/{publicReference}/reopen added to the contract |
| `response_schema_required_field_added` | `paths./api/accountant/general/return-notes.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.anyOf[0].properties.is_tax_document` | new REQUIRED field [is_tax_document] |
| `response_schema_required_field_added` | `paths./api/accountant/general/return-notes.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.anyOf[0].properties.return_reason` | new REQUIRED field [return_reason] |
| `response_schema_required_field_added` | `paths./api/accountant/general/return-notes.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.anyOf[0].properties.status` | new REQUIRED field [status] |
| `response_schema_required_field_added` | `paths./api/accountant/general/return-notes.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.anyOf[0].properties.tax_document_number` | new REQUIRED field [tax_document_number] |
| `response_schema_required_field_added` | `paths./api/accountant/general/return-notes.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.anyOf[1].properties.is_tax_document` | new REQUIRED field [is_tax_document] |
| `response_schema_required_field_added` | `paths./api/accountant/general/return-notes.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.anyOf[1].properties.return_reason` | new REQUIRED field [return_reason] |
| `response_schema_required_field_added` | `paths./api/accountant/general/return-notes.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.anyOf[1].properties.status` | new REQUIRED field [status] |
| `response_schema_required_field_added` | `paths./api/accountant/general/return-notes.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.anyOf[1].properties.tax_document_number` | new REQUIRED field [tax_document_number] |
| `response_schema_required_field_added` | `paths./api/accountant/general/return-notes.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.max_per_page` | new REQUIRED field [max_per_page] |
| `response_schema_required_field_added` | `paths./api/accountant/general/return-notes.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.per_page` | new REQUIRED field [per_page] |
| `operation_added` | `paths./api/accountant/general/vat-returns/{vatReturn}/correction-assessment.get` | GET /api/accountant/general/vat-returns/{vatReturn}/correction-assessment added to the contract |
| `operation_added` | `paths./api/accountant/general/vat-returns/{vatReturn}/manual-filing.post` | POST /api/accountant/general/vat-returns/{vatReturn}/manual-filing added to the contract |
| `operation_added` | `paths./api/accountant/integrations/integrations/connections/{connection}/branches/{branchReference}.put` | PUT /api/accountant/integrations/integrations/connections/{connection}/branches/{branchReference} added to the contract |
| `response_status_added` | `paths./api/accountant/integrations/integrations/sync-runs.post.responses.200` | response [200] added to the contract |
| `operation_added` | `paths./api/accountant/integrations/integrations/{provider}/branches.get` | GET /api/accountant/integrations/integrations/{provider}/branches added to the contract |
| `operation_added` | `paths./api/accountant/integrations/integrations/{provider}/oauth/status.get` | GET /api/accountant/integrations/integrations/{provider}/oauth/status added to the contract |
| `operation_added` | `paths./api/accountant/inventory/inventory/failed-movements.get` | GET /api/accountant/inventory/inventory/failed-movements added to the contract |
| `optional_parameter_added` | `paths./api/accountant/inventory/inventory/items.get.parameters.branch_scope` | optional parameter [branch_scope] (in query) added |
| `optional_parameter_added` | `paths./api/accountant/inventory/inventory/items.get.parameters.integration` | optional parameter [integration] (in query) added |
| `optional_parameter_added` | `paths./api/accountant/inventory/inventory/items.get.parameters.per_page` | optional parameter [per_page] (in query) added |
| `response_schema_type_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.categories.items` | type added (any -> ['string']) |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.branch_id` | new REQUIRED field [branch_id] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.branch_name` | new REQUIRED field [branch_name] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.category` | new REQUIRED field [category] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.code` | new REQUIRED field [code] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.integration` | new REQUIRED field [integration] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.kind` | new REQUIRED field [kind] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.last_sync` | new REQUIRED field [last_sync] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.min_qty` | new REQUIRED field [min_qty] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.name` | new REQUIRED field [name] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.provider_code` | new REQUIRED field [provider_code] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.qty` | new REQUIRED field [qty] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.selling_price` | new REQUIRED field [selling_price] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.status` | new REQUIRED field [status] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.sub_category` | new REQUIRED field [sub_category] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.supplier_id` | new REQUIRED field [supplier_id] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.supplier_name` | new REQUIRED field [supplier_name] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.target_qty` | new REQUIRED field [target_qty] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.unit` | new REQUIRED field [unit] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.unit_code` | new REQUIRED field [unit_code] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.unit_cost` | new REQUIRED field [unit_cost] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.updated_at` | new REQUIRED field [updated_at] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.value` | new REQUIRED field [value] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.vat_rate` | new REQUIRED field [vat_rate] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.max_per_page` | new REQUIRED field [max_per_page] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.per_page` | new REQUIRED field [per_page] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.available_count` | new REQUIRED field [available_count] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.available_value` | new REQUIRED field [available_value] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.branch_label` | new REQUIRED field [branch_label] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.integrations` | new REQUIRED field [integrations] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.items_count` | new REQUIRED field [items_count] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.low_count` | new REQUIRED field [low_count] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.out_count` | new REQUIRED field [out_count] |
| `response_schema_required_field_added` | `paths./api/accountant/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.total_value` | new REQUIRED field [total_value] |

_… and 1260 more (see the JSON report)._

## Documentation-only changes (282)

| Kind | Location | Detail |
|---|---|---|
| `component_schema_documentation` | `components.schemas.AccountantOperationalDashboardResource.properties.branch_performance` | description changed |
| `component_schema_documentation` | `components.schemas.AddPricingMaterialRequest.properties.unit_cost` | description changed |
| `component_schema_documentation` | `components.schemas.AdminNotificationType` | description changed |
| `component_schema_documentation` | `components.schemas.CollectSalesInvoiceRequest` | description changed |
| `component_schema_documentation` | `components.schemas.CollectSalesInvoiceRequest.properties.proof` | description changed |
| `component_schema_documentation` | `components.schemas.CreateCustomerRequest.properties.is_government_entity` | description changed |
| `component_schema_documentation` | `components.schemas.CreateSupplierRequest.properties.person` | description changed |
| `component_schema_reference_shape` | `components.schemas.CreateSupplierRequest.properties.supplier_type` | schema moved between $ref and inline definition (same effective shape) |
| `component_schema_documentation` | `components.schemas.CreateSupplierRequest.properties.whatsapp` | description changed |
| `component_schema_documentation` | `components.schemas.InitializeZakatSessionRequest.properties.fiscal_period_id` | description changed |
| `component_schema_documentation` | `components.schemas.InitializeZakatSessionRequest.properties.items` | description changed |
| `component_schema_documentation` | `components.schemas.PaySupplierInvoiceRequest.properties.proof` | description changed |
| `component_schema_documentation` | `components.schemas.PurchaseOrderResource.properties.actions.properties.send` | description changed |
| `component_schema_documentation` | `components.schemas.RecordStockCountRequest.properties.counted_quantity` | description changed |
| `component_schema_documentation` | `components.schemas.RegisterApplicationRequest` | description changed |
| `component_schema_documentation` | `components.schemas.RegisterApplicationRequest.properties.password` | description changed |
| `component_schema_documentation` | `components.schemas.RegisterApplicationRequest.properties.phone` | description changed |
| `component_schema_documentation` | `components.schemas.ResolveReconciliationItemRequest.properties.bank_ledger_account_reference` | description changed |
| `component_schema_documentation` | `components.schemas.ResubmitExpenseRequest.properties.tax_treatment` | description changed |
| `component_schema_documentation` | `components.schemas.StoreAccountantTaskRequest.properties.company_id` | description changed |
| `component_schema_documentation` | `components.schemas.StoreBranchRequest.properties.phone` | description changed |
| `component_schema_documentation` | `components.schemas.StoreExpenseRequest.properties.tax_treatment` | description changed |
| `component_schema_documentation` | `components.schemas.StoreSubscriptionPackageRequest.properties.duration_in_days` | description changed |
| `component_schema_documentation` | `components.schemas.SupplierResource.properties.invoice_number` | description changed |
| `component_schema_documentation` | `components.schemas.UpdateBranchRequest.properties.phone` | description changed |
| `component_schema_documentation` | `components.schemas.UpdateCustomerRequest.properties.tax_number` | description changed |
| `component_schema_documentation` | `components.schemas.UpdateOrganizationRequest.properties.phone` | description changed |
| `component_schema_documentation` | `components.schemas.UpdateOrganizationRequest.properties.status` | description changed |
| `component_schema_documentation` | `components.schemas.UpdateSubscriptionPackageRequest.properties.duration_in_days` | description changed |
| `component_schema_documentation` | `components.schemas.VerifyRegistrationPaymentRequest` | description changed |
| `response_description_changed` | `paths./api/accountant/accounting/journal-entries.get.responses.200.description` | response description changed |
| `request_schema_documentation` | `paths./api/accountant/accounting/journal-entries/{reference}.put.requestBody.content.application/json.schema.properties.description` | description changed |
| `response_status_added` | `paths./api/accountant/expenses/expenses.get.responses.422` | response [422] added to the contract |
| `response_schema_documentation` | `paths./api/accountant/expenses/expenses/{expense_reference}/duplicate-decision.post.responses.200.content.application/json.schema.allOf[1].properties.data` | description changed |
| `request_schema_documentation` | `paths./api/accountant/expenses/expenses/{reference}.put.requestBody.content.application/json.schema.properties.vat_amount` | description changed |
| `operation_documentation` | `paths./api/accountant/expenses/expenses/{reference}/return.post.summary` | summary changed |
| `response_description_changed` | `paths./api/accountant/integrations/integrations/sync-runs/{syncRun}.patch.responses.200.description` | response description changed |
| `response_description_changed` | `paths./api/accountant/integrations/integrations/sync-runs/{syncRun}.put.responses.200.description` | response description changed |
| `operation_documentation` | `paths./api/accountant/inventory/inventory/items.get.description` | description changed |
| `operation_documentation` | `paths./api/accountant/inventory/inventory/items.get.summary` | summary changed |
| `response_status_added` | `paths./api/accountant/inventory/waste/records.get.responses.422` | response [422] added to the contract |
| `response_schema_documentation` | `paths./api/accountant/notifications/notifications/{uuid}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meeting_link` | description changed |
| `response_schema_documentation` | `paths./api/accountant/notifications/notifications/{uuid}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.target` | description changed |
| `response_schema_documentation` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_documentation` | `paths./api/accountant/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.submitted_by` | description changed |
| `response_description_changed` | `paths./api/accountant/purchases/direct-purchases.get.responses.200.description` | response description changed |
| `response_status_added` | `paths./api/accountant/purchases/suppliers/payment-schedule.get.responses.422` | response [422] added to the contract |
| `response_schema_documentation` | `paths./api/accountant/purchases/suppliers/payments.get.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/accountant/purchases/suppliers/payments.get.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/accountant/sales/customers/{reference}/collections.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.invoices.items.properties.paid_amount` | description changed |
| `response_status_added` | `paths./api/accountant/sales/customers/{reference}/collections.get.responses.422` | response [422] added to the contract |
| `response_schema_documentation` | `paths./api/accountant/tax/tax/periods/{period}/input-invoices.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.output_tax_total` | description changed |
| `operation_documentation` | `paths./api/admin/clients/registration-requests/{id}/approve.post.summary` | summary changed |
| `request_schema_documentation` | `paths./api/admin/clients/registration-requests/{id}/reject.post.requestBody.content.application/json.schema` | description changed |
| `request_schema_documentation` | `paths./api/admin/clients/registration-requests/{id}/reject.post.requestBody.content.application/json.schema` | title changed |
| `request_schema_reference_shape` | `paths./api/admin/clients/registration-requests/{id}/reject.post.requestBody.content.application/json.schema` | schema moved between $ref and inline definition (same effective shape) |
| `request_schema_documentation` | `paths./api/admin/clients/registration-requests/{id}/reject.post.requestBody.content.application/json.schema.properties.reason` | description changed |
| `operation_documentation` | `paths./api/admin/clients/registration-requests/{id}/reject.post.summary` | summary changed |
| `response_description_changed` | `paths./api/admin/dashboard.get.responses.200.description` | response description changed |
| `response_status_added` | `paths./api/admin/dashboard.get.responses.422` | response [422] added to the contract |
| `response_schema_documentation` | `paths./api/admin/packages.post.responses.201.content.application/json.schema.properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/admin/packages.post.responses.201.content.application/json.schema.properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_status_added` | `paths./api/admin/reports/subscriptions.get.responses.422` | response [422] added to the contract |
| `response_description_changed` | `paths./api/admin/suppliers.get.responses.200.description` | response description changed |
| `response_schema_documentation` | `paths./api/auth/accounts.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.subtype` | description changed |
| `response_schema_documentation` | `paths./api/auth/accounts/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subtype` | description changed |
| `response_schema_documentation` | `paths./api/auth/accounts/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subtype` | description changed |
| `operation_documentation` | `paths./api/auth/bootstrap.get.description` | description changed |
| `operation_documentation` | `paths./api/auth/login/send-code.post.description` | description changed |
| `operation_documentation` | `paths./api/auth/onboarding/applications/send-code.post.summary` | summary changed |
| `response_schema_documentation` | `paths./api/owner/accounting/assets.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/owner/accounting/financial-statements/{statement}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/owner/accounting/general-ledger.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/owner/accounting/journal-book.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/owner/accounting/journal-entries.get.responses.200.description` | response description changed |
| `response_schema_documentation` | `paths./api/owner/accounting/reports/trial-balance.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/owner/dashboard/owner.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/owner/expenses/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/owner/general/account/subscription.get.responses.200.description` | response description changed |
| `response_schema_documentation` | `paths./api/owner/general/account/subscription/payments/{reference}/proof.post.responses.201.content.application/json.schema.properties.data.properties.payment.properties.plan_change` | description changed |
| `response_description_changed` | `paths./api/owner/general/account/subscription/renew.post.responses.200.description` | response description changed |
| `operation_documentation` | `paths./api/owner/general/account/subscription/renew.post.summary` | summary changed |
| `response_schema_documentation` | `paths./api/owner/general/packages.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/owner/integrations/integrations/sync-runs/{syncRun}.patch.responses.200.description` | response description changed |
| `response_description_changed` | `paths./api/owner/integrations/integrations/sync-runs/{syncRun}.put.responses.200.description` | response description changed |
| `response_schema_documentation` | `paths./api/owner/inventory/catalog/products/{productReference}/recipe-components.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/owner/inventory/inventory/balances.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items` | title changed |
| `response_schema_reference_shape` | `paths./api/owner/inventory/inventory/balances.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items` | schema moved between $ref and inline definition (same effective shape) |
| `operation_documentation` | `paths./api/owner/inventory/inventory/items.get.description` | description changed |
| `operation_documentation` | `paths./api/owner/inventory/inventory/items.get.summary` | summary changed |
| `request_schema_documentation` | `paths./api/owner/inventory/inventory/items/{item}/stock.put.requestBody.content.application/json.schema.properties.counted_quantity` | description changed |
| `response_status_added` | `paths./api/owner/inventory/waste/records.get.responses.422` | response [422] added to the contract |
| `response_schema_documentation` | `paths./api/owner/notifications/notifications.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_documentation` | `paths./api/owner/notifications/notifications/{uuid}.delete.summary` | summary changed |
| `response_schema_documentation` | `paths./api/owner/notifications/notifications/{uuid}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/owner/payroll/payroll/employees.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/owner/payroll/payroll/runs/{id}.get.responses.200.description` | response description changed |
| `response_schema_documentation` | `paths./api/owner/pricing/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/owner/pricing/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/owner/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_documentation` | `paths./api/owner/pricing/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.submitted_by` | description changed |
| `request_schema_documentation` | `paths./api/owner/purchases/procurement/purchase-requirements.post.requestBody.content.application/json.schema.properties.current_balance` | description changed |
| `response_schema_documentation` | `paths./api/owner/purchases/purchase-orders.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/owner/purchases/suppliers.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_status_added` | `paths./api/owner/purchases/suppliers/debt-aging/suppliers.get.responses.422` | response [422] added to the contract |
| `operation_documentation` | `paths./api/owner/purchases/suppliers/payment-scan.post.summary` | summary changed |
| `response_status_added` | `paths./api/owner/purchases/suppliers/payment-schedule.get.responses.422` | response [422] added to the contract |
| `response_schema_documentation` | `paths./api/owner/purchases/suppliers/payments.get.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/owner/purchases/suppliers/payments.get.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/owner/purchases/suppliers/{id}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/owner/sales/customers/{reference}/collections.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.invoices.items.properties.paid_amount` | description changed |
| `response_status_added` | `paths./api/owner/sales/customers/{reference}/collections.get.responses.422` | response [422] added to the contract |
| `response_description_changed` | `paths./api/owner/sales/invoices.get.responses.200.description` | response description changed |
| `operation_documentation` | `paths./api/owner/sales/invoices/collection-scan.post.summary` | summary changed |
| `response_description_changed` | `paths./api/owner/sales/invoices/form-options.get.responses.200.description` | response description changed |
| `response_description_changed` | `paths./api/owner/sales/invoices/{id}.get.responses.200.description` | response description changed |
| `operation_documentation` | `paths./api/owner/sales/invoices/{reference}/collections.post.summary` | summary changed |
| `operation_documentation` | `paths./api/owner/sales/quotes/{reference}/pdf.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/owner/settings/branches/selectable.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/owner/settings/identity/roles.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/owner/settings/organizations/current.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/owner/tax/tax/periods/{period}/input-invoices.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.output_tax_total` | description changed |
| `response_schema_documentation` | `paths./api/owner/tax/tax/periods/{period}/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/owner/tax/tax/periods/{period}/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_description_changed` | `paths./api/owner/tax/tax/periods/{period}/summary.get.responses.200.description` | response description changed |
| `response_status_added` | `paths./api/owner/tax/zakat/calculations/{uuid}/submit.post.responses.502` | response [502] added to the contract |
| `operation_documentation` | `paths./api/public/general/packages.get.description` | description changed |
| `response_description_changed` | `paths./api/v1/account/subscription.get.responses.200.description` | response description changed |
| `response_schema_documentation` | `paths./api/v1/account/subscription/payments/{reference}/proof.post.responses.201.content.application/json.schema.properties.data.properties.payment.properties.plan_change` | description changed |
| `response_description_changed` | `paths./api/v1/account/subscription/renew.post.responses.200.description` | response description changed |
| `operation_documentation` | `paths./api/v1/account/subscription/renew.post.summary` | summary changed |
| `operation_documentation` | `paths./api/v1/accounting/financial-periods.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/accounting/financial-periods.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/accounting/financial-periods.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `response_schema_documentation` | `paths./api/v1/accounting/financial-statements/{statement}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/v1/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/v1/accounting/reports/trial-balance.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/v1/accounts.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.subtype` | description changed |
| `response_schema_documentation` | `paths./api/v1/accounts/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subtype` | description changed |
| `response_schema_documentation` | `paths./api/v1/accounts/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subtype` | description changed |
| `response_schema_documentation` | `paths./api/v1/assets.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_documentation` | `paths./api/v1/assets.post.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/assets.post.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/assets.post.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/assets/{asset}.patch.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/assets/{asset}.patch.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/assets/{asset}.patch.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/assets/{asset}/status.patch.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/assets/{asset}/status.patch.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/assets/{asset}/status.patch.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/auth/login/send-code.post.description` | description changed |
| `operation_documentation` | `paths./api/v1/bootstrap.get.description` | description changed |
| `response_schema_documentation` | `paths./api/v1/branches/selectable.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/v1/catalog/products/{productReference}/recipe-components.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_documentation` | `paths./api/v1/customers.post.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/customers.post.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/customers.post.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/customers/{id}.put.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/customers/{id}.put.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/customers/{id}.put.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `response_schema_documentation` | `paths./api/v1/customers/{reference}/collections.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.invoices.items.properties.paid_amount` | description changed |
| `response_status_added` | `paths./api/v1/customers/{reference}/collections.get.responses.422` | response [422] added to the contract |
| `response_schema_documentation` | `paths./api/v1/dashboards/owner.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_documentation` | `paths./api/v1/depreciation-runs/{publicReference}.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/depreciation-runs/{publicReference}.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/depreciation-runs/{publicReference}.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `response_schema_documentation` | `paths./api/v1/erp/notifications.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_documentation` | `paths./api/v1/erp/notifications/{uuid}.delete.summary` | summary changed |
| `response_schema_documentation` | `paths./api/v1/erp/notifications/{uuid}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/v1/expense-register.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_status_added` | `paths./api/v1/expenses.get.responses.422` | response [422] added to the contract |
| `response_schema_documentation` | `paths./api/v1/expenses/{expense_reference}/duplicate-decision.post.responses.200.content.application/json.schema.allOf[1].properties.data` | description changed |
| `request_schema_documentation` | `paths./api/v1/expenses/{reference}.put.requestBody.content.application/json.schema.properties.vat_amount` | description changed |
| `operation_documentation` | `paths./api/v1/expenses/{reference}/return.post.summary` | summary changed |
| `operation_documentation` | `paths./api/v1/financial-periods/{periodId}/closing/history.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/financial-periods/{periodId}/closing/history.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/financial-periods/{periodId}/closing/history.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/financial-periods/{periodId}/closing/reopen.post.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/financial-periods/{periodId}/closing/reopen.post.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/financial-periods/{periodId}/closing/reopen.post.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `response_schema_documentation` | `paths./api/v1/general-ledger.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/v1/identity/roles.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/v1/integrations/sync-runs/{syncRun}.patch.responses.200.description` | response description changed |
| `response_description_changed` | `paths./api/v1/integrations/sync-runs/{syncRun}.put.responses.200.description` | response description changed |
| `response_schema_documentation` | `paths./api/v1/inventory/balances.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items` | title changed |
| `response_schema_reference_shape` | `paths./api/v1/inventory/balances.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items` | schema moved between $ref and inline definition (same effective shape) |
| `operation_documentation` | `paths./api/v1/inventory/items.get.description` | description changed |
| `operation_documentation` | `paths./api/v1/inventory/items.get.summary` | summary changed |
| `request_schema_documentation` | `paths./api/v1/inventory/items/{item}/stock.put.requestBody.content.application/json.schema.properties.counted_quantity` | description changed |
| `operation_documentation` | `paths./api/v1/invoices.get.description` | description changed |
| `response_description_changed` | `paths./api/v1/invoices.get.responses.200.description` | response description changed |
| `operation_tags_changed` | `paths./api/v1/invoices.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/invoices.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/invoices/collection-scan.post.summary` | summary changed |
| `response_description_changed` | `paths./api/v1/invoices/form-options.get.responses.200.description` | response description changed |
| `operation_documentation` | `paths./api/v1/invoices/{id}.get.description` | description changed |
| `response_description_changed` | `paths./api/v1/invoices/{id}.get.responses.200.description` | response description changed |
| `operation_tags_changed` | `paths./api/v1/invoices/{id}.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/invoices/{id}.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/invoices/{reference}/collections.post.summary` | summary changed |
| `response_description_changed` | `paths./api/v1/journal-entries.get.responses.200.description` | response description changed |
| `operation_documentation` | `paths./api/v1/journal-entries/{id}/amend.post.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/journal-entries/{id}/amend.post.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/journal-entries/{id}/amend.post.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/journal-entries/{id}/cancel.post.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/journal-entries/{id}/cancel.post.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/journal-entries/{id}/cancel.post.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `request_schema_documentation` | `paths./api/v1/journal-entries/{reference}.put.requestBody.content.application/json.schema.properties.description` | description changed |
| `operation_documentation` | `paths./api/v1/monthly-reports/{reportId}/review.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/monthly-reports/{reportId}/review.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/monthly-reports/{reportId}/review.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/onboarding/applications/send-code.post.summary` | summary changed |
| `response_schema_documentation` | `paths./api/v1/organizations/current.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/v1/packages.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/v1/payroll/employees.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/v1/payroll/runs/{id}.get.responses.200.description` | response description changed |
| `operation_documentation` | `paths./api/v1/platform/clients/registration-requests/{id}/approve.post.summary` | summary changed |
| `request_schema_documentation` | `paths./api/v1/platform/clients/registration-requests/{id}/reject.post.requestBody.content.application/json.schema` | description changed |
| `request_schema_documentation` | `paths./api/v1/platform/clients/registration-requests/{id}/reject.post.requestBody.content.application/json.schema` | title changed |
| `request_schema_reference_shape` | `paths./api/v1/platform/clients/registration-requests/{id}/reject.post.requestBody.content.application/json.schema` | schema moved between $ref and inline definition (same effective shape) |
| `request_schema_documentation` | `paths./api/v1/platform/clients/registration-requests/{id}/reject.post.requestBody.content.application/json.schema.properties.reason` | description changed |
| `operation_documentation` | `paths./api/v1/platform/clients/registration-requests/{id}/reject.post.summary` | summary changed |
| `response_description_changed` | `paths./api/v1/platform/dashboard.get.responses.200.description` | response description changed |
| `response_status_added` | `paths./api/v1/platform/dashboard.get.responses.422` | response [422] added to the contract |
| `response_schema_documentation` | `paths./api/v1/platform/packages.post.responses.201.content.application/json.schema.properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/v1/platform/packages.post.responses.201.content.application/json.schema.properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_status_added` | `paths./api/v1/platform/reports/subscriptions.get.responses.422` | response [422] added to the contract |
| `response_description_changed` | `paths./api/v1/platform/suppliers.get.responses.200.description` | response description changed |
| `response_schema_documentation` | `paths./api/v1/pricing/register.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/v1/pricing/register/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/v1/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_documentation` | `paths./api/v1/pricing/sessions/{product_reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.submitted_by` | description changed |
| `request_schema_documentation` | `paths./api/v1/procurement/purchase-requirements.post.requestBody.content.application/json.schema.properties.current_balance` | description changed |
| `operation_documentation` | `paths./api/v1/public/packages.get.description` | description changed |
| `response_schema_documentation` | `paths./api/v1/purchase-orders.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_documentation` | `paths./api/v1/quotes/{reference}/pdf.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/v1/suppliers.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_documentation` | `paths./api/v1/suppliers.post.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/suppliers.post.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/suppliers.post.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/suppliers/debt-aging/suppliers.get.description` | description changed |
| `response_status_added` | `paths./api/v1/suppliers/debt-aging/suppliers.get.responses.422` | response [422] added to the contract |
| `operation_tags_changed` | `paths./api/v1/suppliers/debt-aging/suppliers.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/suppliers/debt-aging/suppliers.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/suppliers/pay.post.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/suppliers/pay.post.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/suppliers/pay.post.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/suppliers/payment-scan.post.description` | description changed |
| `operation_documentation` | `paths./api/v1/suppliers/payment-scan.post.summary` | summary changed |
| `operation_tags_changed` | `paths./api/v1/suppliers/payment-scan.post.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/suppliers/payment-scan.post.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `response_status_added` | `paths./api/v1/suppliers/payment-schedule.get.responses.422` | response [422] added to the contract |
| `response_schema_documentation` | `paths./api/v1/suppliers/payments.get.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/v1/suppliers/payments.get.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/v1/suppliers/{id}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_documentation` | `paths./api/v1/suppliers/{supplier_public_reference}/invoices/pending.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/suppliers/{supplier_public_reference}/invoices/pending.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/suppliers/{supplier_public_reference}/invoices/pending.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/suppliers/{supplier_public_reference}/invoices/{invoice_public_reference}/payments.post.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/suppliers/{supplier_public_reference}/invoices/{invoice_public_reference}/payments.post.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/suppliers/{supplier_public_reference}/invoices/{invoice_public_reference}/payments.post.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `response_schema_documentation` | `paths./api/v1/tax/periods/{period}/input-invoices.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.output_tax_total` | description changed |
| `response_schema_documentation` | `paths./api/v1/tax/periods/{period}/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/v1/tax/periods/{period}/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_description_changed` | `paths./api/v1/tax/periods/{period}/summary.get.responses.200.description` | response description changed |
| `operation_documentation` | `paths./api/v1/tax/vat-returns/export.post.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/tax/vat-returns/export.post.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/tax/vat-returns/export.post.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `response_status_added` | `paths./api/v1/waste/records.get.responses.422` | response [422] added to the contract |
| `operation_documentation` | `paths./api/v1/waste/records.post.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/waste/records.post.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/waste/records.post.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/waste/records/{wasteRecord}/confirm.post.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/waste/records/{wasteRecord}/confirm.post.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/waste/records/{wasteRecord}/confirm.post.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/zakat/calculations/{uuid}/submit.post.description` | description changed |
| `response_status_added` | `paths./api/v1/zakat/calculations/{uuid}/submit.post.responses.502` | response [502] added to the contract |
| `operation_tags_changed` | `paths./api/v1/zakat/calculations/{uuid}/submit.post.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/zakat/calculations/{uuid}/submit.post.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/zakat/sessions/{uuid}/worksheet.post.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/zakat/sessions/{uuid}/worksheet.post.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/zakat/sessions/{uuid}/worksheet.post.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |

> **Fail closed:** unclassified changes require an explicit
> compatibility decision before this contract may be approved.

