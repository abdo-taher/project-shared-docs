# OpenAPI Contract Compatibility Report

- Baseline: `published 2026.10.18-06d388692794` (1028 operations)
- Candidate: `build 9d5502f689ae` (1244 operations)
- Generated: 2026-10-21T11:10:39.084855+00:00

## Summary

| Category | Count |
|---|---|
| BREAKING | 602 |
| UNKNOWN | 32 |
| NON_BREAKING | 1887 |
| DOCUMENTATION_ONLY | 389 |
| **total** | **2910** |

## Breaking changes (602)

| Kind | Location | Detail |
|---|---|---|
| `component_schema_nullability_added` | `components.schemas.AccountantOperationalDashboardResource.properties.branch_id` | type now also accepts/returns null |
| `component_schema_items_changed` | `components.schemas.AccountantOperationalDashboardResource.properties.branch_performance` | array items schema removed or added |
| `component_schema_type_changed` | `components.schemas.AccountantOperationalDashboardResource.properties.branch_performance` | type changed (['string'] -> ['array']) |
| `component_schema_type_changed` | `components.schemas.AccountantOperationalDashboardResource.properties.financial_indicators` | type changed (['string'] -> ['object']) |
| `component_schema_items_changed` | `components.schemas.AccountantOperationalDashboardResource.properties.follow_up_operations` | array items schema removed or added |
| `component_schema_type_changed` | `components.schemas.AccountantOperationalDashboardResource.properties.follow_up_operations` | type changed (['string'] -> ['array']) |
| `component_schema_items_changed` | `components.schemas.AccountantOperationalDashboardResource.properties.monthly_closing_tasks` | array items schema removed or added |
| `component_schema_type_changed` | `components.schemas.AccountantOperationalDashboardResource.properties.monthly_closing_tasks` | type changed (['string'] -> ['array']) |
| `shared_component_removed` | `components.schemas.App.ERP.Core.Organization.Models.Branch` | component [schemas.App.ERP.Core.Organization.Models.Branch] removed — 4 operation(s) referenced it |
| `shared_component_removed` | `components.schemas.ExpenseResource` | component [schemas.ExpenseResource] removed — 2 operation(s) referenced it |
| `shared_component_removed` | `components.schemas.ExpenseStatus` | component [schemas.ExpenseStatus] removed — 2 operation(s) referenced it |
| `component_schema_required_field_added` | `components.schemas.ExternalSyncRunResource.properties.last_sync` | new REQUIRED field [last_sync] |
| `component_schema_constraint_narrowed` | `components.schemas.InitiatePaymentRequest.properties.payment_data.properties.transfer_receipt_path` | [maxLength] None -> 500 |
| `shared_component_removed` | `components.schemas.InventoryItem` | component [schemas.InventoryItem] removed — 2 operation(s) referenced it |
| `component_schema_field_removed` | `components.schemas.IssueTokenRequest.properties.device_token` | field [device_token] removed |
| `shared_component_removed` | `components.schemas.PayrollPaymentFileResource` | component [schemas.PayrollPaymentFileResource] removed — 2 operation(s) referenced it |
| `shared_component_removed` | `components.schemas.PurchaseOrderStatus` | component [schemas.PurchaseOrderStatus] removed — 2 operation(s) referenced it |
| `component_schema_nullability_added` | `components.schemas.RegistrationApplication.properties.email` | type now also accepts/returns null |
| `component_schema_nullability_added` | `components.schemas.RegistrationApplication.properties.phone` | type now also accepts/returns null |
| `component_schema_enum_value_added` | `components.schemas.RegistrationApplication.properties.status` | response may now contain a value clients do not handle |
| `component_schema_nullability_added` | `components.schemas.RegistrationApplication.properties.updated_at` | type now also accepts/returns null |
| `component_schema_enum_value_added` | `components.schemas.RegistrationApplicationStatus` | response may now contain a value clients do not handle |
| `component_schema_required_field_added` | `components.schemas.RenewAdminSubscriptionRequest.properties.amount` | new REQUIRED field [amount] |
| `component_schema_required_field_added` | `components.schemas.RenewAdminSubscriptionRequest.properties.currency` | new REQUIRED field [currency] |
| `component_schema_required_field_added` | `components.schemas.RenewAdminSubscriptionRequest.properties.evidence_reference` | new REQUIRED field [evidence_reference] |
| `component_schema_required_field_added` | `components.schemas.RenewAdminSubscriptionRequest.properties.payment_reference` | new REQUIRED field [payment_reference] |
| `component_schema_enum_added` | `components.schemas.StoreExpenseRequest.properties.payment_method` | enum constraint added |
| `component_schema_enum_value_added` | `components.schemas.Subscription.properties.status` | response may now contain a value clients do not handle |
| `component_schema_nullability_added` | `components.schemas.Subscription.properties.status` | type now also accepts/returns null |
| `component_schema_nullability_added` | `components.schemas.SubscriptionPackageResource.properties.uuid` | type now also accepts/returns null |
| `component_schema_field_became_required` | `components.schemas.UpdateAccountProfileRequest.properties.email` | field [email] became required |
| `component_schema_nullability_removed` | `components.schemas.UpdateAccountProfileRequest.properties.email` | type no longer accepts/returns null |
| `component_schema_field_removed` | `components.schemas.UpdateAccountProfileRequest.properties.job_title` | field [job_title] removed |
| `component_schema_field_became_required` | `components.schemas.UpdateAccountProfileRequest.properties.mobile` | field [mobile] became required |
| `component_schema_nullability_removed` | `components.schemas.UpdateAccountProfileRequest.properties.mobile` | type no longer accepts/returns null |
| `component_schema_field_became_required` | `components.schemas.UpdateAccountProfileRequest.properties.name` | field [name] became required |
| `component_schema_nullability_removed` | `components.schemas.UpdateAccountProfileRequest.properties.name` | type no longer accepts/returns null |
| `component_schema_field_became_required` | `components.schemas.UpdateBranchRequest.properties.name` | field [name] became required |
| `security_scheme_changed` | `components.securitySchemes.sanctumSession` | security scheme [sanctumSession] changed — authentication semantics may differ |
| `response_schema_const_changed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.confirmation.properties.message` | const constraint changed |
| `response_schema_type_changed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.post.responses.200.content.application/json.schema.allOf[1].properties.data` | type changed (['string'] -> ['object']) |
| `response_schema_type_changed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data` | type changed (['string'] -> ['object']) |
| `response_schema_type_changed` | `paths./api/accountant/reports/monthly-reports.post.responses.200.content.application/json.schema.allOf[1].properties.data` | type changed (['string'] -> ['object']) |
| `response_schema_nullability_added` | `paths./api/accountant/reports/monthly-reports/{reportId}/commentary.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.indicators.items.properties.provenance` | type now also accepts/returns null |
| `response_schema_nullability_added` | `paths./api/accountant/reports/monthly-reports/{reportId}/commentary.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.indicators.items.properties.source_module` | type now also accepts/returns null |
| `response_schema_type_changed` | `paths./api/accountant/reports/monthly-reports/{reportId}/commentary.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.sections` | type changed (['string'] -> ['object']) |
| `response_schema_type_changed` | `paths./api/accountant/reports/monthly-reports/{reportId}/publish.post.responses.200.content.application/json.schema.allOf[1].properties.data` | type changed (['string'] -> ['object']) |
| `response_schema_nullability_added` | `paths./api/accountant/reports/monthly-reports/{reportId}/ready.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.indicators.items.properties.provenance` | type now also accepts/returns null |
| `response_schema_nullability_added` | `paths./api/accountant/reports/monthly-reports/{reportId}/ready.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.indicators.items.properties.source_module` | type now also accepts/returns null |
| `response_schema_type_changed` | `paths./api/accountant/reports/monthly-reports/{reportId}/ready.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.sections` | type changed (['string'] -> ['object']) |
| `response_schema_nullability_added` | `paths./api/accountant/reports/monthly-reports/{reportId}/refresh-draft.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.indicators.items.properties.provenance` | type now also accepts/returns null |
| `response_schema_nullability_added` | `paths./api/accountant/reports/monthly-reports/{reportId}/refresh-draft.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.indicators.items.properties.source_module` | type now also accepts/returns null |
| `response_schema_type_changed` | `paths./api/accountant/reports/monthly-reports/{reportId}/refresh-draft.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.changed` | type changed (['string'] -> ['boolean']) |
| `response_schema_type_changed` | `paths./api/accountant/reports/monthly-reports/{reportId}/refresh-draft.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.sections` | type changed (['string'] -> ['object']) |
| `response_schema_field_removed` | `paths./api/admin/clients/registration-requests/{id}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | field [items] removed |
| `request_schema_required_field_added` | `paths./api/admin/clients/registration-requests/{id}/payment/verify.post.requestBody.content.application/json.schema.properties.amount` | new REQUIRED field [amount] |
| `request_schema_required_field_added` | `paths./api/admin/clients/registration-requests/{id}/payment/verify.post.requestBody.content.application/json.schema.properties.currency` | new REQUIRED field [currency] |
| `request_body_became_required` | `paths./api/admin/clients/registration-requests/{id}/payment/verify.post.requestBody.required` | request body became required |
| `response_schema_type_changed` | `paths./api/admin/clients/registration-requests/{id}/payment/verify.post.responses.200.content.application/json.schema.allOf[1].properties.data` | type changed (['object'] -> ['array', 'string']) |
| `response_schema_field_removed` | `paths./api/admin/clients/registration-requests/{id}/payment/verify.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | field [items] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-assignments.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.current_page` | field [current_page] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-assignments.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.data` | field [data] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-assignments.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.first_page_url` | field [first_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-assignments.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.from` | field [from] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-assignments.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.last_page` | field [last_page] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-assignments.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.last_page_url` | field [last_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-assignments.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.links` | field [links] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-assignments.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.next_page_url` | field [next_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-assignments.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.path` | field [path] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-assignments.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.per_page` | field [per_page] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-assignments.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.prev_page_url` | field [prev_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-assignments.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.to` | field [to] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-assignments.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total` | field [total] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-workload.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.current_page` | field [current_page] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-workload.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.data` | field [data] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-workload.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.first_page_url` | field [first_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-workload.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.from` | field [from] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-workload.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.last_page` | field [last_page] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-workload.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.last_page_url` | field [last_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-workload.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.links` | field [links] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-workload.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.next_page_url` | field [next_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-workload.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.path` | field [path] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-workload.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.per_page` | field [per_page] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-workload.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.prev_page_url` | field [prev_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-workload.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.to` | field [to] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/accountant-workload.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total` | field [total] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/clients.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.current_page` | field [current_page] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/clients.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.data` | field [data] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/clients.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.first_page_url` | field [first_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/clients.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.from` | field [from] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/clients.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.last_page` | field [last_page] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/clients.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.last_page_url` | field [last_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/clients.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.links` | field [links] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/clients.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.next_page_url` | field [next_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/clients.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.path` | field [path] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/clients.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.per_page` | field [per_page] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/clients.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.prev_page_url` | field [prev_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/clients.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.to` | field [to] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/clients.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total` | field [total] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/renewals.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.current_page` | field [current_page] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/renewals.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.data` | field [data] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/renewals.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.first_page_url` | field [first_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/renewals.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.from` | field [from] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/renewals.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.last_page` | field [last_page] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/renewals.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.last_page_url` | field [last_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/renewals.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.links` | field [links] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/renewals.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.next_page_url` | field [next_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/renewals.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.path` | field [path] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/renewals.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.per_page` | field [per_page] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/renewals.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.prev_page_url` | field [prev_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/renewals.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.to` | field [to] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/renewals.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total` | field [total] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/subscriptions.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.current_page` | field [current_page] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/subscriptions.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.data` | field [data] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/subscriptions.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.first_page_url` | field [first_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/subscriptions.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.from` | field [from] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/subscriptions.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.last_page` | field [last_page] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/subscriptions.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.last_page_url` | field [last_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/subscriptions.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.links` | field [links] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/subscriptions.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.next_page_url` | field [next_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/subscriptions.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.path` | field [path] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/subscriptions.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.per_page` | field [per_page] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/subscriptions.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.prev_page_url` | field [prev_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/subscriptions.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.to` | field [to] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/subscriptions.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total` | field [total] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/suppliers.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.current_page` | field [current_page] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/suppliers.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.data` | field [data] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/suppliers.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.first_page_url` | field [first_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/suppliers.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.from` | field [from] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/suppliers.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.last_page` | field [last_page] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/suppliers.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.last_page_url` | field [last_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/suppliers.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.links` | field [links] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/suppliers.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.next_page_url` | field [next_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/suppliers.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.path` | field [path] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/suppliers.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.per_page` | field [per_page] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/suppliers.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.prev_page_url` | field [prev_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/suppliers.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.to` | field [to] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/suppliers.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total` | field [total] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.current_page` | field [current_page] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.data` | field [data] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.first_page_url` | field [first_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.from` | field [from] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.last_page` | field [last_page] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.last_page_url` | field [last_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.links` | field [links] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.next_page_url` | field [next_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.path` | field [path] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.per_page` | field [per_page] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.prev_page_url` | field [prev_page_url] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.to` | field [to] removed |
| `response_schema_field_removed` | `paths./api/admin/reports/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total` | field [total] removed |
| `response_schema_type_removed` | `paths./api/admin/subscriptions/{userId}/renew.post.responses.200.content.application/json.schema.allOf[1].properties.data` | type removed (['null', 'object'] -> any) |
| `response_schema_field_removed` | `paths./api/auth/account.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[1].properties.profile.properties.job_title` | field [job_title] removed |
| `response_schema_type_changed` | `paths./api/auth/account.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[1].properties.profile.properties.password_changed_at` | type changed (['null'] -> ['string']) |
| `request_body_became_required` | `paths./api/auth/account/profile.post.requestBody.required` | request body became required |
| `response_schema_field_removed` | `paths./api/auth/account/profile.post.responses.200.content.application/json.schema.properties.data.properties.job_title` | field [job_title] removed |
| `response_schema_type_changed` | `paths./api/auth/account/profile/send-code.post.responses.200.content.application/json.schema.properties.data` | type changed (['null'] -> ['object']) |
| `response_schema_field_removed` | `paths./api/auth/account/profile/send-code.post.responses.200.content.application/json.schema.properties.meta` | field [meta] removed |
| `request_schema_field_removed` | `paths./api/auth/login.post.requestBody.content.application/json.schema.properties.device_name` | field [device_name] removed |
| `request_schema_constraint_narrowed` | `paths./api/auth/login.post.requestBody.content.application/json.schema.properties.device_token` | [maxLength] 512 -> 255 |
| `response_status_removed` | `paths./api/auth/login.post.responses.201` | response [201] removed from the contract |
| `response_schema_field_removed` | `paths./api/auth/onboarding/applications.post.responses.201.content.application/json.schema.allOf[1].properties.data.anyOf[1].properties.city` | field [city] removed |
| `response_schema_type_changed` | `paths./api/auth/onboarding/applications/send-code.post.responses.200.content.application/json.schema.properties.data` | type changed (['null'] -> ['object']) |
| `response_schema_field_removed` | `paths./api/auth/onboarding/applications/send-code.post.responses.200.content.application/json.schema.properties.meta` | field [meta] removed |
| `required_request_body_added` | `paths./api/auth/onboarding/applications/verify.post.requestBody` | request body added and REQUIRED |
| `response_schema_field_removed` | `paths./api/auth/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.available_payment_methods` | field [available_payment_methods] removed |
| `response_schema_field_removed` | `paths./api/auth/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.duration_months` | field [duration_months] removed |
| `response_schema_field_removed` | `paths./api/auth/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.package_name` | field [package_name] removed |
| `response_schema_field_removed` | `paths./api/auth/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subscription_value` | field [subscription_value] removed |
| `response_schema_field_removed` | `paths./api/auth/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total_amount` | field [total_amount] removed |
| `response_schema_field_removed` | `paths./api/auth/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.vat_value` | field [vat_value] removed |
| `response_schema_type_changed` | `paths./api/auth/profile.get.responses.200.content.application/json.schema.properties.data.properties.image` | type changed (['null'] -> ['null', 'string']) |
| `response_schema_type_changed` | `paths./api/auth/settings.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.categories.items.properties.is_enabled` | type changed (['string'] -> ['boolean']) |
| `response_schema_type_changed` | `paths./api/auth/settings.post.responses.200.content.application/json.schema.properties.data.properties.categories.items.properties.is_enabled` | type changed (['string'] -> ['boolean']) |
| `response_schema_type_changed` | `paths./api/auth/subscriptions/registration-request.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.business_email` | type changed (['null'] -> ['null', 'string']) |
| `response_schema_type_changed` | `paths./api/auth/subscriptions/registration-request.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.business_phone` | type changed (['null'] -> ['null', 'string']) |
| `response_schema_type_changed` | `paths./api/auth/subscriptions/registration-request.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.city.properties.id` | type changed (['null'] -> ['null', 'string']) |
| `response_schema_nullability_added` | `paths./api/auth/subscriptions/registration-request.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.email` | type now also accepts/returns null |
| `response_schema_type_changed` | `paths./api/auth/subscriptions/registration-request.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.number` | type changed (['null'] -> ['string']) |
| `response_schema_enum_value_added` | `paths./api/auth/subscriptions/registration-request.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | response may now contain a value clients do not handle |
| `response_schema_type_removed` | `paths./api/auth/subscriptions/registration/resubmit.post.responses.200.content.application/json.schema.allOf[1].properties.data` | type removed (['object'] -> any) |
| `response_schema_field_removed` | `paths./api/auth/subscriptions/registration/resubmit.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.success` | field [success] removed |
| `response_schema_type_changed` | `paths./api/auth/tokens.post.responses.201.content.application/json.schema.allOf[1].properties.data.anyOf[1].properties.image` | type changed (['null'] -> ['null', 'string']) |
| `response_schema_changed` | `paths./api/owner/accounting/general-ledger.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.account.properties.type` | schema value changed incompatibly |
| `response_schema_items_changed` | `paths./api/owner/accounting/general-ledger.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.accounts` | array items schema removed or added |
| `response_schema_type_changed` | `paths./api/owner/expenses/expenses.post.responses.200.content.application/json.schema.allOf[1].properties.data` | type changed (['object'] -> ['string']) |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.amount_before_tax` | field [amount_before_tax] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.due_date` | field [due_date] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.expense_date` | field [expense_date] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.expense_number` | field [expense_number] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | field [id] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.public_reference` | field [public_reference] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.purchase_order_reference` | field [purchase_order_reference] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | field [status] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.tax_amount` | field [tax_amount] removed |
| `response_schema_field_removed` | `paths./api/owner/expenses/expenses.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total_amount` | field [total_amount] removed |
| `response_schema_type_removed` | `paths./api/owner/general/account/subscription/renew.post.responses.200.content.application/json.schema` | type removed (['object'] -> any) |
| `response_schema_field_removed` | `paths./api/owner/general/account/subscription/renew.post.responses.200.content.application/json.schema.properties.data` | field [data] removed |
| `response_schema_field_removed` | `paths./api/owner/general/account/subscription/renew.post.responses.200.content.application/json.schema.properties.message` | field [message] removed |
| `response_schema_format_removed` | `paths./api/owner/general/admin/roles/{roleReference}/permissions.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.created_at` | format changed ('date-time' -> None) |
| `response_schema_format_removed` | `paths./api/owner/general/admin/roles/{roleReference}/permissions.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.updated_at` | format changed ('date-time' -> None) |
| `response_schema_nullability_added` | `paths./api/owner/general/subscriptions.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | type now also accepts/returns null |
| `response_schema_type_changed` | `paths./api/owner/inventory/catalog-products.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.products.items.properties.category_id` | type changed (['integer', 'null'] -> ['null', 'string']) |
| `response_schema_type_changed` | `paths./api/owner/inventory/catalog-products.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.products.items.properties.id` | type changed (['integer', 'null'] -> ['null', 'string']) |
| `response_schema_type_changed` | `paths./api/owner/inventory/catalog-products.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.products.items.properties.sub_category_id` | type changed (['integer', 'null'] -> ['null', 'string']) |
| `response_schema_type_changed` | `paths./api/owner/inventory/catalog-products/{catalogProduct}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.category_id` | type changed (['integer', 'null'] -> ['null', 'string']) |
| `response_schema_type_changed` | `paths./api/owner/inventory/catalog-products/{catalogProduct}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | type changed (['integer', 'null'] -> ['null', 'string']) |
| `response_schema_type_changed` | `paths./api/owner/inventory/catalog-products/{catalogProduct}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.sub_category_id` | type changed (['integer', 'null'] -> ['null', 'string']) |
| `response_schema_type_removed` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items` | type removed (['object'] -> any) |
| `response_schema_field_removed` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.canonical_uom_reference` | field [canonical_uom_reference] removed |
| `response_schema_field_removed` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.company_id` | field [company_id] removed |
| `response_schema_field_removed` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.created_at` | field [created_at] removed |
| `response_schema_field_removed` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.id` | field [id] removed |
| `response_schema_field_removed` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.kind` | field [kind] removed |
| `response_schema_field_removed` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.name` | field [name] removed |
| `response_schema_field_removed` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.product_reference` | field [product_reference] removed |
| `response_schema_field_removed` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.public_reference` | field [public_reference] removed |
| `response_schema_field_removed` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.sku` | field [sku] removed |
| `response_schema_field_removed` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.unit` | field [unit] removed |
| `response_schema_field_removed` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.updated_at` | field [updated_at] removed |
| `required_request_body_added` | `paths./api/owner/meetings/meetings/availability/{public_reference}/book.post.requestBody` | request body added and REQUIRED |
| `response_schema_field_removed` | `paths./api/owner/payroll/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.content` | field [content] removed |
| `response_schema_field_removed` | `paths./api/owner/payroll/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.content_sha256` | field [content_sha256] removed |
| `response_schema_field_removed` | `paths./api/owner/payroll/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.document_type` | field [document_type] removed |
| `response_schema_field_removed` | `paths./api/owner/payroll/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.employee_count` | field [employee_count] removed |
| `response_schema_field_removed` | `paths./api/owner/payroll/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.file_format` | field [file_format] removed |
| `response_schema_field_removed` | `paths./api/owner/payroll/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.file_name` | field [file_name] removed |
| `response_schema_field_removed` | `paths./api/owner/payroll/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.generated_at` | field [generated_at] removed |
| `response_schema_field_removed` | `paths./api/owner/payroll/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.generated_by` | field [generated_by] removed |
| `response_schema_field_removed` | `paths./api/owner/payroll/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.generated_by_kind` | field [generated_by_kind] removed |
| `response_schema_field_removed` | `paths./api/owner/payroll/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.lines` | field [lines] removed |
| `response_schema_field_removed` | `paths./api/owner/payroll/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.payroll_run_reference` | field [payroll_run_reference] removed |
| `response_schema_field_removed` | `paths./api/owner/payroll/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.period_month` | field [period_month] removed |
| `response_schema_field_removed` | `paths./api/owner/payroll/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.period_year` | field [period_year] removed |
| `response_schema_field_removed` | `paths./api/owner/payroll/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.public_reference` | field [public_reference] removed |
| `response_schema_field_removed` | `paths./api/owner/payroll/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.run_status` | field [run_status] removed |
| `response_schema_field_removed` | `paths./api/owner/payroll/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.run_version` | field [run_version] removed |
| `response_schema_field_removed` | `paths./api/owner/payroll/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | field [status] removed |
| `response_schema_field_removed` | `paths./api/owner/payroll/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.template_version` | field [template_version] removed |
| `response_schema_field_removed` | `paths./api/owner/payroll/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total_net_amount` | field [total_net_amount] removed |
| `request_schema_type_changed` | `paths./api/owner/payroll/payroll/employees.post.requestBody.content.application/json.schema.properties.basic_salary` | type changed (['string'] -> ['number']) |
| `request_schema_type_changed` | `paths./api/owner/payroll/payroll/employees/{publicReference}.patch.requestBody.content.application/json.schema.properties.basic_salary` | type changed (['null', 'string'] -> ['null', 'number']) |
| `request_schema_type_changed` | `paths./api/owner/payroll/payroll/runs/{runId}/lines/{lineId}.patch.requestBody.content.application/json.schema.properties.deduction_days` | type changed (['null', 'string'] -> ['null', 'number']) |
| `request_schema_type_changed` | `paths./api/owner/payroll/payroll/runs/{runId}/lines/{lineId}.patch.requestBody.content.application/json.schema.properties.other_allowances` | type changed (['null', 'string'] -> ['null', 'number']) |
| `request_schema_type_changed` | `paths./api/owner/payroll/payroll/runs/{runId}/lines/{lineId}.patch.requestBody.content.application/json.schema.properties.other_deductions` | type changed (['null', 'string'] -> ['null', 'number']) |
| `request_schema_type_changed` | `paths./api/owner/payroll/payroll/runs/{runId}/lines/{lineId}.patch.requestBody.content.application/json.schema.properties.overtime_hours` | type changed (['null', 'string'] -> ['null', 'number']) |
| `request_schema_type_changed` | `paths./api/owner/payroll/payroll/runs/{runId}/lines/{lineId}.patch.requestBody.content.application/json.schema.properties.overtime_rate` | type changed (['null', 'string'] -> ['null', 'number']) |
| `response_schema_type_changed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.document_url` | type changed (['null'] -> ['null', 'string']) |
| `response_schema_nullability_added` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.indicators.items.properties.provenance` | type now also accepts/returns null |
| `response_schema_nullability_added` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.indicators.items.properties.source_module` | type now also accepts/returns null |
| `response_schema_type_changed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.sections` | type changed (['string'] -> ['object']) |
| `parameter_schema_constraint_narrowed` | `paths./api/owner/reports/owner/reporting/financial.get.parameters.expense_category_id.schema` | [maxLength] None -> 64 |
| `parameter_schema_type_changed` | `paths./api/owner/reports/owner/reporting/financial.get.parameters.expense_category_id.schema` | type changed (['integer', 'null'] -> ['null', 'string']) |
| `response_schema_field_removed` | `paths./api/owner/reports/owner/reporting/financial.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.expenses_by_category` | field [expenses_by_category] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/owner/reporting/financial.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.net_profit_loss` | field [net_profit_loss] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/owner/reporting/financial.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.previous_period` | field [previous_period] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/owner/reporting/financial.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total_expenses` | field [total_expenses] removed |
| `response_schema_field_removed` | `paths./api/owner/reports/owner/reporting/financial.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total_revenue` | field [total_revenue] removed |
| `response_schema_type_removed` | `paths./api/owner/settings/audit-log.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.log.items.properties.user_id` | type removed (['string'] -> any) |
| `response_schema_field_removed` | `paths./api/owner/settings/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.accountant_id` | field [accountant_id] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.address` | field [address] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.city` | field [city] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.code` | field [code] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.company_id` | field [company_id] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.created_at` | field [created_at] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.created_by` | field [created_by] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.email` | field [email] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.id` | field [id] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.is_main` | field [is_main] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.manager_name` | field [manager_name] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.name` | field [name] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.phone` | field [phone] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.public_reference` | field [public_reference] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.status` | field [status] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.status_changed_at` | field [status_changed_at] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.status_changed_by` | field [status_changed_by] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.tenant_id` | field [tenant_id] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.updated_at` | field [updated_at] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.updated_by` | field [updated_by] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.version` | field [version] removed |
| `request_body_became_required` | `paths./api/owner/settings/branches/{reference}.put.requestBody.required` | request body became required |
| `response_schema_field_removed` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.accountant_id` | field [accountant_id] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.address` | field [address] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.city` | field [city] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.code` | field [code] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.company_id` | field [company_id] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.created_at` | field [created_at] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.created_by` | field [created_by] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.email` | field [email] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | field [id] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.is_main` | field [is_main] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.manager_name` | field [manager_name] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.name` | field [name] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.phone` | field [phone] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.public_reference` | field [public_reference] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | field [status] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status_changed_at` | field [status_changed_at] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status_changed_by` | field [status_changed_by] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.tenant_id` | field [tenant_id] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.updated_at` | field [updated_at] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.updated_by` | field [updated_by] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.version` | field [version] removed |
| `response_schema_constraint_widened` | `paths./api/owner/settings/identity/memberships/{membershipId}/companies/{companyId}/branches.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.allowed_branches.anyOf[0]` | [minItems] 1 -> None |
| `response_schema_constraint_widened` | `paths./api/owner/settings/identity/memberships/{membershipId}/companies/{companyId}/branches.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.allowed_branches.anyOf[0]` | [maxItems] 1 -> None |
| `response_schema_type_changed` | `paths./api/owner/settings/identity/memberships/{membershipId}/companies/{companyId}/branches.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.allowed_branches.anyOf[0]` | type changed (['array'] -> ['object']) |
| `response_schema_items_changed` | `paths./api/owner/settings/identity/memberships/{membershipId}/companies/{companyId}/branches.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.allowed_branches.anyOf[1]` | array items schema removed or added |
| `response_schema_field_removed` | `paths./api/owner/settings/identity/users/{userReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.email` | field [email] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/identity/users/{userReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.mobile` | field [mobile] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/identity/users/{userReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.name` | field [name] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/identity/users/{userReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.public_reference` | field [public_reference] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/identity/users/{userReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | field [status] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/identity/users/{userReference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.version` | field [version] removed |
| `response_schema_items_changed` | `paths./api/owner/settings/organizations/current.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.log` | array items schema removed or added |
| `request_media_type_removed` | `paths./api/owner/settings/organizations/current.patch.requestBody.content.application/json` | request media type [application/json] removed |
| `response_schema_field_removed` | `paths./api/owner/settings/users.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items` | field [items] removed |
| `response_schema_type_changed` | `paths./api/owner/settings/users/form-options.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.roles.items.properties.denied` | type changed (['null'] -> ['string']) |
| `response_schema_constraint_widened` | `paths./api/owner/tax/tax/vat-returns/summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.completeness.properties.needs_review_count` | [minimum] 0 -> None |
| `response_schema_type_removed` | `paths./api/owner/tax/zakat/history.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.period_label` | type removed (['null'] -> any) |
| `parameter_schema_enum_added` | `paths./api/public/support/page.get.parameters.type.schema` | enum constraint added |
| `response_schema_field_removed` | `paths./api/v1/account.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[1].properties.profile.properties.job_title` | field [job_title] removed |
| `response_schema_type_changed` | `paths./api/v1/account.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[1].properties.profile.properties.password_changed_at` | type changed (['null'] -> ['string']) |
| `request_body_became_required` | `paths./api/v1/account/profile.post.requestBody.required` | request body became required |
| `response_schema_field_removed` | `paths./api/v1/account/profile.post.responses.200.content.application/json.schema.properties.data.properties.job_title` | field [job_title] removed |
| `response_schema_type_changed` | `paths./api/v1/account/profile/send-code.post.responses.200.content.application/json.schema.properties.data` | type changed (['null'] -> ['object']) |
| `response_schema_field_removed` | `paths./api/v1/account/profile/send-code.post.responses.200.content.application/json.schema.properties.meta` | field [meta] removed |
| `response_schema_type_removed` | `paths./api/v1/account/subscription/renew.post.responses.200.content.application/json.schema` | type removed (['object'] -> any) |
| `response_schema_field_removed` | `paths./api/v1/account/subscription/renew.post.responses.200.content.application/json.schema.properties.data` | field [data] removed |
| `response_schema_field_removed` | `paths./api/v1/account/subscription/renew.post.responses.200.content.application/json.schema.properties.message` | field [message] removed |
| `response_schema_format_removed` | `paths./api/v1/admin/roles/{roleReference}/permissions.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.created_at` | format changed ('date-time' -> None) |
| `response_schema_format_removed` | `paths./api/v1/admin/roles/{roleReference}/permissions.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.updated_at` | format changed ('date-time' -> None) |
| `response_schema_type_removed` | `paths./api/v1/audit-log.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.log.items.properties.user_id` | type removed (['string'] -> any) |
| `request_schema_field_removed` | `paths./api/v1/auth/login.post.requestBody.content.application/json.schema.properties.device_name` | field [device_name] removed |
| `request_schema_constraint_narrowed` | `paths./api/v1/auth/login.post.requestBody.content.application/json.schema.properties.device_token` | [maxLength] 512 -> 255 |
| `response_status_removed` | `paths./api/v1/auth/login.post.responses.201` | response [201] removed from the contract |
| `request_body_removed` | `paths./api/v1/auth/logout.post.requestBody` | request body removed from the contract |
| `response_schema_type_changed` | `paths./api/v1/auth/profile.get.responses.200.content.application/json.schema.properties.data.properties.image` | type changed (['null'] -> ['null', 'string']) |
| `response_schema_type_changed` | `paths./api/v1/auth/tokens.post.responses.201.content.application/json.schema.allOf[1].properties.data.anyOf[1].properties.image` | type changed (['null'] -> ['null', 'string']) |
| `response_schema_field_removed` | `paths./api/v1/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.accountant_id` | field [accountant_id] removed |
| `response_schema_field_removed` | `paths./api/v1/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.address` | field [address] removed |
| `response_schema_field_removed` | `paths./api/v1/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.city` | field [city] removed |
| `response_schema_field_removed` | `paths./api/v1/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.code` | field [code] removed |
| `response_schema_field_removed` | `paths./api/v1/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.company_id` | field [company_id] removed |
| `response_schema_field_removed` | `paths./api/v1/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.created_at` | field [created_at] removed |
| `response_schema_field_removed` | `paths./api/v1/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.created_by` | field [created_by] removed |
| `response_schema_field_removed` | `paths./api/v1/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.email` | field [email] removed |
| `response_schema_field_removed` | `paths./api/v1/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.id` | field [id] removed |
| `response_schema_field_removed` | `paths./api/v1/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.is_main` | field [is_main] removed |
| `response_schema_field_removed` | `paths./api/v1/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.manager_name` | field [manager_name] removed |
| `response_schema_field_removed` | `paths./api/v1/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.name` | field [name] removed |
| `response_schema_field_removed` | `paths./api/v1/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.phone` | field [phone] removed |
| `response_schema_field_removed` | `paths./api/v1/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.public_reference` | field [public_reference] removed |
| `response_schema_field_removed` | `paths./api/v1/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.status` | field [status] removed |
| `response_schema_field_removed` | `paths./api/v1/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.status_changed_at` | field [status_changed_at] removed |
| `response_schema_field_removed` | `paths./api/v1/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.status_changed_by` | field [status_changed_by] removed |
| `response_schema_field_removed` | `paths./api/v1/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.tenant_id` | field [tenant_id] removed |
| `response_schema_field_removed` | `paths./api/v1/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.updated_at` | field [updated_at] removed |
| `response_schema_field_removed` | `paths./api/v1/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.updated_by` | field [updated_by] removed |
| `response_schema_field_removed` | `paths./api/v1/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data.properties.version` | field [version] removed |
| `request_body_became_required` | `paths./api/v1/branches/{reference}.put.requestBody.required` | request body became required |
| `response_schema_field_removed` | `paths./api/v1/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.accountant_id` | field [accountant_id] removed |
| `response_schema_field_removed` | `paths./api/v1/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.address` | field [address] removed |
| `response_schema_field_removed` | `paths./api/v1/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.city` | field [city] removed |
| `response_schema_field_removed` | `paths./api/v1/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.code` | field [code] removed |
| `response_schema_field_removed` | `paths./api/v1/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.company_id` | field [company_id] removed |
| `response_schema_field_removed` | `paths./api/v1/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.created_at` | field [created_at] removed |
| `response_schema_field_removed` | `paths./api/v1/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.created_by` | field [created_by] removed |
| `response_schema_field_removed` | `paths./api/v1/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.email` | field [email] removed |
| `response_schema_field_removed` | `paths./api/v1/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | field [id] removed |
| `response_schema_field_removed` | `paths./api/v1/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.is_main` | field [is_main] removed |
| `response_schema_field_removed` | `paths./api/v1/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.manager_name` | field [manager_name] removed |
| `response_schema_field_removed` | `paths./api/v1/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.name` | field [name] removed |
| `response_schema_field_removed` | `paths./api/v1/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.phone` | field [phone] removed |
| `response_schema_field_removed` | `paths./api/v1/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.public_reference` | field [public_reference] removed |
| `response_schema_field_removed` | `paths./api/v1/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | field [status] removed |
| `response_schema_field_removed` | `paths./api/v1/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status_changed_at` | field [status_changed_at] removed |
| `response_schema_field_removed` | `paths./api/v1/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status_changed_by` | field [status_changed_by] removed |
| `response_schema_field_removed` | `paths./api/v1/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.tenant_id` | field [tenant_id] removed |
| `response_schema_field_removed` | `paths./api/v1/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.updated_at` | field [updated_at] removed |
| `response_schema_field_removed` | `paths./api/v1/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.updated_by` | field [updated_by] removed |
| `response_schema_field_removed` | `paths./api/v1/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data.properties.version` | field [version] removed |
| `response_schema_type_changed` | `paths./api/v1/catalog-products.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.products.items.properties.category_id` | type changed (['integer', 'null'] -> ['null', 'string']) |
| `response_schema_type_changed` | `paths./api/v1/catalog-products.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.products.items.properties.id` | type changed (['integer', 'null'] -> ['null', 'string']) |
| `response_schema_type_changed` | `paths./api/v1/catalog-products.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.products.items.properties.sub_category_id` | type changed (['integer', 'null'] -> ['null', 'string']) |
| `response_schema_type_changed` | `paths./api/v1/catalog-products/{catalogProduct}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.category_id` | type changed (['integer', 'null'] -> ['null', 'string']) |
| `response_schema_type_changed` | `paths./api/v1/catalog-products/{catalogProduct}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | type changed (['integer', 'null'] -> ['null', 'string']) |
| `response_schema_type_changed` | `paths./api/v1/catalog-products/{catalogProduct}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.sub_category_id` | type changed (['integer', 'null'] -> ['null', 'string']) |
| `parameter_schema_enum_added` | `paths./api/v1/content/support/page.get.parameters.type.schema` | enum constraint added |
| `response_schema_field_removed` | `paths./api/v1/erp/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.available_payment_methods` | field [available_payment_methods] removed |
| `response_schema_field_removed` | `paths./api/v1/erp/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.duration_months` | field [duration_months] removed |
| `response_schema_field_removed` | `paths./api/v1/erp/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.package_name` | field [package_name] removed |
| `response_schema_field_removed` | `paths./api/v1/erp/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.subscription_value` | field [subscription_value] removed |
| `response_schema_field_removed` | `paths./api/v1/erp/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total_amount` | field [total_amount] removed |
| `response_schema_field_removed` | `paths./api/v1/erp/onboarding/applications/{reference}/subscription-summary.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.vat_value` | field [vat_value] removed |
| `response_schema_type_changed` | `paths./api/v1/expenses.post.responses.200.content.application/json.schema.allOf[1].properties.data` | type changed (['object'] -> ['string']) |
| `response_schema_field_removed` | `paths./api/v1/expenses.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.amount_before_tax` | field [amount_before_tax] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.due_date` | field [due_date] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.expense_date` | field [expense_date] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.expense_number` | field [expense_number] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | field [id] removed |
| `response_schema_field_removed` | `paths./api/v1/expenses.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.public_reference` | field [public_reference] removed |

_… and 202 more (see the JSON report)._

## Unclassified changes (fail closed) (32)

| Kind | Location | Detail |
|---|---|---|
| `response_schema_anyOf_changed` | `paths./api/admin/clients/registration-requests/{id}/approve.post.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/admin/clients/registration-requests/{id}/reject.post.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/admin/clients/registration-requests/{id}/request-info.post.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/admin/subscriptions/{userId}/renew.post.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_keyword_changed` | `paths./api/auth/account.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[1].properties.subscription.properties.usage` | unrecognized schema keyword [prefixItems] changed |
| `response_schema_anyOf_changed` | `paths./api/auth/onboarding/applications/{reference}/subscription-payment.post.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition changed (unclassified rewrite) |
| `response_schema_anyOf_changed` | `paths./api/auth/subscriptions/registration/resubmit.post.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_keyword_changed` | `paths./api/owner/general/account/subscription.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[1].properties.subscription.properties.usage` | unrecognized schema keyword [prefixItems] changed |
| `response_schema_allOf_changed` | `paths./api/owner/general/account/subscription/renew.post.responses.200.content.application/json.schema` | allOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/owner/inventory/waste/analytics.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/owner/meetings/meetings/availability/{public_reference}/book.post.responses.200.content.application/json.schema` | allOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/owner/payroll/payroll/runs.post.responses.201.content.application/json.schema.allOf[1].properties.data` | allOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.view` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/owner/settings/audit-log.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.log.items.properties.user_id` | anyOf composition added or removed |
| `response_schema_keyword_changed` | `paths./api/owner/settings/identity/memberships/{membershipId}/companies/{companyId}/branches.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.allowed_branches.anyOf[0]` | unrecognized schema keyword [prefixItems] changed |
| `response_schema_keyword_changed` | `paths./api/owner/settings/identity/memberships/{membershipId}/companies/{companyId}/branches.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.allowed_branches.anyOf[1]` | unrecognized schema keyword [prefixItems] changed |
| `response_schema_keyword_changed` | `paths./api/v1/account.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[1].properties.subscription.properties.usage` | unrecognized schema keyword [prefixItems] changed |
| `response_schema_keyword_changed` | `paths./api/v1/account/subscription.get.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[1].properties.subscription.properties.usage` | unrecognized schema keyword [prefixItems] changed |
| `response_schema_allOf_changed` | `paths./api/v1/account/subscription/renew.post.responses.200.content.application/json.schema` | allOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/audit-log.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.log.items.properties.user_id` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/erp/onboarding/applications/{reference}/subscription-payment.post.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition changed (unclassified rewrite) |
| `response_schema_keyword_changed` | `paths./api/v1/identity/memberships/{membershipId}/companies/{companyId}/branches.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.allowed_branches.anyOf[0]` | unrecognized schema keyword [prefixItems] changed |
| `response_schema_keyword_changed` | `paths./api/v1/identity/memberships/{membershipId}/companies/{companyId}/branches.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.allowed_branches.anyOf[1]` | unrecognized schema keyword [prefixItems] changed |
| `response_schema_allOf_changed` | `paths./api/v1/meetings/availability/{public_reference}/book.post.responses.200.content.application/json.schema` | allOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.view` | anyOf composition added or removed |
| `response_schema_allOf_changed` | `paths./api/v1/payroll/runs.post.responses.201.content.application/json.schema.allOf[1].properties.data` | allOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/platform/clients/registration-requests/{id}/approve.post.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/platform/clients/registration-requests/{id}/reject.post.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/platform/clients/registration-requests/{id}/request-info.post.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/platform/subscriptions/{userId}/renew.post.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/subscriptions/registration/resubmit.post.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |
| `response_schema_anyOf_changed` | `paths./api/v1/waste/analytics.get.responses.200.content.application/json.schema.allOf[1].properties.data` | anyOf composition added or removed |

## Non-breaking changes (1887)

| Kind | Location | Detail |
|---|---|---|
| `shared_component_added` | `components.parameters.ContextBranch` | component [parameters.ContextBranch] added |
| `shared_component_added` | `components.parameters.ContextBranchRequired` | component [parameters.ContextBranchRequired] added |
| `shared_component_added` | `components.parameters.ContextCompany` | component [parameters.ContextCompany] added |
| `shared_component_added` | `components.parameters.ContextTenant` | component [parameters.ContextTenant] added |
| `shared_component_added` | `components.parameters.ContextTenantRequired` | component [parameters.ContextTenantRequired] added |
| `component_schema_required_field_added` | `components.schemas.AccountantDetailsResource.properties.id` | new REQUIRED field [id] |
| `shared_component_added` | `components.schemas.AccountantMeetingSlotRequest` | component [schemas.AccountantMeetingSlotRequest] added |
| `component_schema_required_field_added` | `components.schemas.AccountantOperationalDashboardResource.properties.financial_indicators.properties.net_profit` | new REQUIRED field [net_profit] |
| `component_schema_required_field_added` | `components.schemas.AccountantOperationalDashboardResource.properties.financial_indicators.properties.profit_margin` | new REQUIRED field [profit_margin] |
| `component_schema_required_field_added` | `components.schemas.AccountantOperationalDashboardResource.properties.financial_indicators.properties.total_expenses` | new REQUIRED field [total_expenses] |
| `component_schema_required_field_added` | `components.schemas.AccountantOperationalDashboardResource.properties.financial_indicators.properties.total_revenue` | new REQUIRED field [total_revenue] |
| `component_schema_required_field_added` | `components.schemas.AccountantResource.properties.id` | new REQUIRED field [id] |
| `component_schema_required_field_added` | `components.schemas.AccountantTaskResource.properties.version` | new REQUIRED field [version] |
| `shared_component_added` | `components.schemas.ApproveVatReturnRequest` | component [schemas.ApproveVatReturnRequest] added |
| `shared_component_added` | `components.schemas.BookMeetingSlotRequest` | component [schemas.BookMeetingSlotRequest] added |
| `component_schema_required_field_added` | `components.schemas.Branch.properties.city_reference` | new REQUIRED field [city_reference] |
| `shared_component_added` | `components.schemas.CancelSalesAdjustmentNoteRequest` | component [schemas.CancelSalesAdjustmentNoteRequest] added |
| `component_schema_required_field_added` | `components.schemas.CatalogProduct.properties.is_active` | new REQUIRED field [is_active] |
| `component_schema_required_field_added` | `components.schemas.CatalogProduct.properties.status` | new REQUIRED field [status] |
| `shared_component_added` | `components.schemas.ChangeBranchStatusRequest` | component [schemas.ChangeBranchStatusRequest] added |
| `shared_component_added` | `components.schemas.ClosingTaskResource` | component [schemas.ClosingTaskResource] added |
| `component_schema_field_added` | `components.schemas.CreateCustomerRequest.properties.is_active` | new optional field [is_active] |
| `component_schema_field_added` | `components.schemas.CreateCustomerRequest.properties.is_government_entity` | new optional field [is_government_entity] |
| `component_schema_field_added` | `components.schemas.CreateRoleRequest.properties.name_ar` | new optional field [name_ar] |
| `shared_component_added` | `components.schemas.CreateSalesAdjustmentNoteRequest` | component [schemas.CreateSalesAdjustmentNoteRequest] added |
| `component_schema_field_added` | `components.schemas.CreateSupplierRequest.properties.commercial_register` | new optional field [commercial_register] |
| `component_schema_field_added` | `components.schemas.CreateSupplierRequest.properties.is_active` | new optional field [is_active] |
| `component_schema_field_became_optional` | `components.schemas.CreateSupplierRequest.properties.payment_terms` | field [payment_terms] became optional |
| `component_schema_nullability_added` | `components.schemas.CreateSupplierRequest.properties.payment_terms` | type now also accepts/returns null |
| `component_schema_field_added` | `components.schemas.CreateSupplierRequest.properties.person` | new optional field [person] |
| `component_schema_field_added` | `components.schemas.CreateSupplierRequest.properties.phone` | new optional field [phone] |
| `component_schema_enum_value_added` | `components.schemas.CreateSupplierRequest.properties.supplier_type` | newly accepted enum value |
| `component_schema_field_became_optional` | `components.schemas.CreateSupplierRequest.properties.supplier_type` | field [supplier_type] became optional |
| `component_schema_nullability_added` | `components.schemas.CreateSupplierRequest.properties.supplier_type` | type now also accepts/returns null |
| `component_schema_field_became_optional` | `components.schemas.CreateSupplierRequest.properties.supply_category` | field [supply_category] became optional |
| `component_schema_nullability_added` | `components.schemas.CreateSupplierRequest.properties.supply_category` | type now also accepts/returns null |
| `component_schema_field_added` | `components.schemas.CreateSupplierRequest.properties.vat_number` | new optional field [vat_number] |
| `component_schema_required_field_added` | `components.schemas.CustomerResource.properties.is_government_entity` | new REQUIRED field [is_government_entity] |
| `shared_component_added` | `components.schemas.FiscalPeriodStatus` | component [schemas.FiscalPeriodStatus] added |
| `component_schema_enum_value_added` | `components.schemas.InitializeZakatSessionRequest.properties.items.items.properties.type` | newly accepted enum value |
| `component_schema_field_became_optional` | `components.schemas.InitiatePaymentRequest.properties.payment_data` | field [payment_data] became optional |
| `component_schema_nullability_added` | `components.schemas.InitiatePaymentRequest.properties.payment_data.properties.transfer_receipt_path` | type now also accepts/returns null |
| `component_schema_required_field_added` | `components.schemas.InputTaxInvoiceResource.properties.attachment.properties.name` | new REQUIRED field [name] |
| `component_schema_required_field_added` | `components.schemas.InputTaxInvoiceResource.properties.attachment.properties.url` | new REQUIRED field [url] |
| `component_schema_enum_value_added` | `components.schemas.IssueTokenRequest.properties.type` | newly accepted enum value |
| `shared_component_added` | `components.schemas.LoginRequest` | component [schemas.LoginRequest] added |
| `shared_component_added` | `components.schemas.MonthlyReportStatus` | component [schemas.MonthlyReportStatus] added |
| `component_schema_required_field_added` | `components.schemas.OrganizationResource.properties.city` | new REQUIRED field [city] |
| `component_schema_required_field_added` | `components.schemas.OrganizationResource.properties.contact_name` | new REQUIRED field [contact_name] |
| `component_schema_required_field_added` | `components.schemas.OrganizationResource.properties.contact_role` | new REQUIRED field [contact_role] |
| `component_schema_required_field_added` | `components.schemas.OrganizationResource.properties.landline` | new REQUIRED field [landline] |
| `component_schema_required_field_added` | `components.schemas.OrganizationResource.properties.logo_url` | new REQUIRED field [logo_url] |
| `component_schema_required_field_added` | `components.schemas.OrganizationResource.properties.phone` | new REQUIRED field [phone] |
| `component_schema_required_field_added` | `components.schemas.OrganizationResource.properties.phone_code` | new REQUIRED field [phone_code] |
| `component_schema_required_field_added` | `components.schemas.Package.properties.legacy_subscription_package_id` | new REQUIRED field [legacy_subscription_package_id] |
| `component_schema_required_field_added` | `components.schemas.Package.properties.limits` | new REQUIRED field [limits] |
| `component_schema_required_field_added` | `components.schemas.Package.properties.modules` | new REQUIRED field [modules] |
| `component_schema_required_field_added` | `components.schemas.Package.properties.name_ar` | new REQUIRED field [name_ar] |
| `component_schema_required_field_added` | `components.schemas.Package.properties.package_definition_id` | new REQUIRED field [package_definition_id] |
| `component_schema_required_field_added` | `components.schemas.Package.properties.tag` | new REQUIRED field [tag] |
| `component_schema_required_field_added` | `components.schemas.Package.properties.uuid` | new REQUIRED field [uuid] |
| `component_schema_required_field_added` | `components.schemas.Package.properties.version` | new REQUIRED field [version] |
| `component_schema_required_field_added` | `components.schemas.PayrollRunReviewResource.properties.lines.items.properties.employee_name` | new REQUIRED field [employee_name] |
| `shared_component_added` | `components.schemas.PostingRequestStatus` | component [schemas.PostingRequestStatus] added |
| `component_schema_required_field_added` | `components.schemas.PurchaseOrderResource.properties.id` | new REQUIRED field [id] |
| `component_schema_required_field_added` | `components.schemas.PurchaseOrderResource.properties.number` | new REQUIRED field [number] |
| `shared_component_added` | `components.schemas.RecordSubscriptionPaymentRequest` | component [schemas.RecordSubscriptionPaymentRequest] added |
| `component_schema_field_added` | `components.schemas.RegisterApplicationRequest.properties.accept_terms` | new optional field [accept_terms] |
| `component_schema_field_added` | `components.schemas.RegisterApplicationRequest.properties.business_email` | new optional field [business_email] |
| `component_schema_field_added` | `components.schemas.RegisterApplicationRequest.properties.business_phone` | new optional field [business_phone] |
| `component_schema_field_added` | `components.schemas.RegisterApplicationRequest.properties.city` | new optional field [city] |
| `component_schema_field_became_optional` | `components.schemas.RegisterApplicationRequest.properties.city_id` | field [city_id] became optional |
| `component_schema_format_removed` | `components.schemas.RegisterApplicationRequest.properties.city_id` | format changed ('uuid' -> None) |
| `component_schema_nullability_added` | `components.schemas.RegisterApplicationRequest.properties.city_id` | type now also accepts/returns null |
| `component_schema_field_added` | `components.schemas.RegisterApplicationRequest.properties.device_token` | new optional field [device_token] |
| `component_schema_field_added` | `components.schemas.RegisterApplicationRequest.properties.package_id` | new optional field [package_id] |
| `component_schema_field_became_optional` | `components.schemas.RegisterApplicationRequest.properties.phone` | field [phone] became optional |
| `component_schema_nullability_added` | `components.schemas.RegisterApplicationRequest.properties.phone` | type now also accepts/returns null |
| `component_schema_field_added` | `components.schemas.RegisterApplicationRequest.properties.type` | new optional field [type] |
| `component_schema_required_field_added` | `components.schemas.RegistrationApplication.properties.abandoned_at` | new REQUIRED field [abandoned_at] |
| `component_schema_required_field_added` | `components.schemas.RegistrationApplication.properties.business_email` | new REQUIRED field [business_email] |
| `component_schema_required_field_added` | `components.schemas.RegistrationApplication.properties.business_phone` | new REQUIRED field [business_phone] |
| `component_schema_nullability_removed` | `components.schemas.RegistrationApplication.properties.city` | type no longer accepts/returns null |
| `component_schema_required_field_added` | `components.schemas.RegistrationApplication.properties.payment_proof_flag_details` | new REQUIRED field [payment_proof_flag_details] |
| `component_schema_required_field_added` | `components.schemas.RegistrationApplication.properties.payment_proof_flag_reason` | new REQUIRED field [payment_proof_flag_reason] |
| `component_schema_required_field_added` | `components.schemas.RegistrationApplication.properties.payment_proof_flagged_at` | new REQUIRED field [payment_proof_flagged_at] |
| `component_schema_required_field_added` | `components.schemas.RegistrationApplication.properties.purged_at` | new REQUIRED field [purged_at] |
| `component_schema_required_field_added` | `components.schemas.RegistrationApplication.properties.terms_accepted` | new REQUIRED field [terms_accepted] |
| `component_schema_required_field_added` | `components.schemas.RegistrationApplication.properties.terms_accepted_at` | new REQUIRED field [terms_accepted_at] |
| `shared_component_added` | `components.schemas.RejectSubscriptionPaymentRequest` | component [schemas.RejectSubscriptionPaymentRequest] added |
| `shared_component_added` | `components.schemas.ResubmitExpenseRequest` | component [schemas.ResubmitExpenseRequest] added |
| `shared_component_added` | `components.schemas.ResubmitRegistrationRequest` | component [schemas.ResubmitRegistrationRequest] added |
| `component_schema_required_field_added` | `components.schemas.Role.properties.name_ar` | new REQUIRED field [name_ar] |
| `component_schema_field_added` | `components.schemas.SendRegistrationCodeRequest.properties.email` | new optional field [email] |
| `component_schema_field_became_optional` | `components.schemas.SendRegistrationCodeRequest.properties.phone` | field [phone] became optional |
| `component_schema_nullability_added` | `components.schemas.SendRegistrationCodeRequest.properties.phone` | type now also accepts/returns null |
| `component_schema_field_added` | `components.schemas.StoreBranchRequest.properties.city_id` | new optional field [city_id] |
| `component_schema_field_added` | `components.schemas.StoreCatalogProductRequest.properties.is_active` | new optional field [is_active] |
| `component_schema_field_added` | `components.schemas.StoreExpenseRequest.properties.branch_id` | new optional field [branch_id] |
| `component_schema_field_added` | `components.schemas.StoreExpenseRequest.properties.category_id` | new optional field [category_id] |
| `component_schema_field_added` | `components.schemas.StoreExpenseRequest.properties.operation_type` | new optional field [operation_type] |
| `component_schema_field_added` | `components.schemas.StoreExpenseRequest.properties.payment_status` | new optional field [payment_status] |
| `component_schema_field_added` | `components.schemas.StoreExpenseRequest.properties.po_number` | new optional field [po_number] |
| `component_schema_field_added` | `components.schemas.StoreExpenseRequest.properties.tax_treatment` | new optional field [tax_treatment] |
| `component_schema_field_added` | `components.schemas.StoreSubscriptionPackageRequest.properties.description` | new optional field [description] |
| `component_schema_field_added` | `components.schemas.StoreSubscriptionPackageRequest.properties.name_ar` | new optional field [name_ar] |
| `component_schema_required_field_added` | `components.schemas.SubscriptionPackageResource.properties.description` | new REQUIRED field [description] |
| `component_schema_required_field_added` | `components.schemas.SubscriptionPackageResource.properties.duration_days` | new REQUIRED field [duration_days] |
| `component_schema_required_field_added` | `components.schemas.SubscriptionPackageResource.properties.id` | new REQUIRED field [id] |
| `component_schema_required_field_added` | `components.schemas.SubscriptionPackageResource.properties.name_ar` | new REQUIRED field [name_ar] |
| `component_schema_required_field_added` | `components.schemas.SubscriptionPackageResource.properties.package_definition` | new REQUIRED field [package_definition] |
| `component_schema_required_field_added` | `components.schemas.SubscriptionPackageResource.properties.price` | new REQUIRED field [price] |
| `component_schema_required_field_added` | `components.schemas.SubscriptionPackageResource.properties.version` | new REQUIRED field [version] |
| `component_schema_required_field_added` | `components.schemas.SupplementalTaxDocumentResource.properties.file.properties.url` | new REQUIRED field [url] |
| `component_schema_required_field_added` | `components.schemas.SupplierInvoice.properties.amount_before_tax` | new REQUIRED field [amount_before_tax] |
| `component_schema_required_field_added` | `components.schemas.SupplierInvoice.properties.invoice_number` | new REQUIRED field [invoice_number] |
| `component_schema_required_field_added` | `components.schemas.SupplierInvoice.properties.returned_amount` | new REQUIRED field [returned_amount] |
| `component_schema_required_field_added` | `components.schemas.SupplierInvoice.properties.tax_treatment` | new REQUIRED field [tax_treatment] |
| `component_schema_required_field_added` | `components.schemas.SupplierInvoice.properties.vat_amount` | new REQUIRED field [vat_amount] |
| `component_schema_required_field_added` | `components.schemas.SupplierInvoice.properties.vat_review_status` | new REQUIRED field [vat_review_status] |
| `component_schema_required_field_added` | `components.schemas.SupplierResource.properties.commercial_register` | new REQUIRED field [commercial_register] |
| `component_schema_required_field_added` | `components.schemas.SupplierResource.properties.contact_person` | new REQUIRED field [contact_person] |
| `component_schema_required_field_added` | `components.schemas.SupplierResource.properties.search_hit` | new REQUIRED field [search_hit] |
| `component_schema_required_field_added` | `components.schemas.SupplierResource.properties.vat_number` | new REQUIRED field [vat_number] |
| `shared_component_added` | `components.schemas.SupportPageType` | component [schemas.SupportPageType] added |
| `component_schema_required_field_added` | `components.schemas.TaxPeriodInvoiceResource.properties.attachment.properties.name` | new REQUIRED field [name] |
| `component_schema_required_field_added` | `components.schemas.TaxPeriodInvoiceResource.properties.attachment.properties.url` | new REQUIRED field [url] |
| `component_schema_field_added` | `components.schemas.UpdateBranchRequest.properties.city_id` | new optional field [city_id] |
| `component_schema_field_added` | `components.schemas.UpdateCatalogProductRequest.properties.is_active` | new optional field [is_active] |
| `component_schema_field_added` | `components.schemas.UpdateCustomerRequest.properties.is_active` | new optional field [is_active] |
| `component_schema_field_added` | `components.schemas.UpdateCustomerRequest.properties.is_government_entity` | new optional field [is_government_entity] |
| `component_schema_field_added` | `components.schemas.UpdateOrganizationRequest.properties.city_id` | new optional field [city_id] |
| `component_schema_field_added` | `components.schemas.UpdateOrganizationRequest.properties.contact_name` | new optional field [contact_name] |
| `component_schema_field_added` | `components.schemas.UpdateOrganizationRequest.properties.contact_role` | new optional field [contact_role] |
| `component_schema_field_added` | `components.schemas.UpdateOrganizationRequest.properties.landline` | new optional field [landline] |
| `component_schema_field_added` | `components.schemas.UpdateOrganizationRequest.properties.logo` | new optional field [logo] |
| `component_schema_field_added` | `components.schemas.UpdateOrganizationRequest.properties.phone` | new optional field [phone] |
| `component_schema_field_added` | `components.schemas.UpdateOrganizationRequest.properties.phone_code` | new optional field [phone_code] |
| `component_schema_field_added` | `components.schemas.UpdateOrganizationRequest.properties.remove_logo` | new optional field [remove_logo] |
| `component_schema_field_added` | `components.schemas.UpdateOrganizationRequest.properties.status` | new optional field [status] |
| `shared_component_added` | `components.schemas.UpdatePackageEntitlementsRequest` | component [schemas.UpdatePackageEntitlementsRequest] added |
| `shared_component_added` | `components.schemas.UpdatePlatformSettingsRequest` | component [schemas.UpdatePlatformSettingsRequest] added |
| `component_schema_field_added` | `components.schemas.UpdateRegistrationApplicationStatusRequest.properties.amount` | new optional field [amount] |
| `component_schema_field_added` | `components.schemas.UpdateRegistrationApplicationStatusRequest.properties.currency` | new optional field [currency] |
| `component_schema_field_added` | `components.schemas.UpdateRegistrationApplicationStatusRequest.properties.reason` | new optional field [reason] |
| `component_schema_field_added` | `components.schemas.UpdateRolePermissionsRequest.properties.expected_version` | new optional field [expected_version] |
| `component_schema_field_added` | `components.schemas.UpdateRoleRequest.properties.name_ar` | new optional field [name_ar] |
| `component_schema_field_added` | `components.schemas.UpdateSubscriptionPackageRequest.properties.description` | new optional field [description] |
| `component_schema_field_added` | `components.schemas.UpdateSubscriptionPackageRequest.properties.name_ar` | new optional field [name_ar] |
| `shared_component_added` | `components.schemas.UpdateSupplierInvoiceRequest` | component [schemas.UpdateSupplierInvoiceRequest] added |
| `component_schema_field_added` | `components.schemas.UpdateSupplierRequest.properties.commercial_register` | new optional field [commercial_register] |
| `component_schema_field_added` | `components.schemas.UpdateSupplierRequest.properties.is_active` | new optional field [is_active] |
| `component_schema_field_added` | `components.schemas.UpdateSupplierRequest.properties.person` | new optional field [person] |
| `component_schema_field_added` | `components.schemas.UpdateSupplierRequest.properties.phone` | new optional field [phone] |
| `component_schema_field_added` | `components.schemas.UpdateSupplierRequest.properties.vat_number` | new optional field [vat_number] |
| `component_schema_field_added` | `components.schemas.UploadSupplementalTaxDocumentRequest.properties.amount` | new optional field [amount] |
| `component_schema_field_added` | `components.schemas.UploadSupplementalTaxDocumentRequest.properties.date` | new optional field [date] |
| `component_schema_field_added` | `components.schemas.UploadSupplementalTaxDocumentRequest.properties.number` | new optional field [number] |
| `component_schema_field_added` | `components.schemas.UploadSupplementalTaxDocumentRequest.properties.total` | new optional field [total] |
| `component_schema_field_added` | `components.schemas.UploadSupplementalTaxDocumentRequest.properties.vat` | new optional field [vat] |
| `component_schema_field_added` | `components.schemas.UploadSupplementalTaxDocumentRequest.properties.vendor` | new optional field [vendor] |
| `shared_component_added` | `components.schemas.VatReturnPreparationResource` | component [schemas.VatReturnPreparationResource] added |
| `shared_component_added` | `components.schemas.VerifyRegistrationCodeRequest` | component [schemas.VerifyRegistrationCodeRequest] added |
| `shared_component_added` | `components.schemas.VerifyRegistrationPaymentRequest` | component [schemas.VerifyRegistrationPaymentRequest] added |
| `shared_component_added` | `components.schemas.VerifySubscriptionPaymentRequest` | component [schemas.VerifySubscriptionPaymentRequest] added |
| `shared_component_added` | `components.schemas.ZakatCalculationRequest` | component [schemas.ZakatCalculationRequest] added |
| `component_schema_required_field_added` | `components.schemas.ZakatSessionResource.properties.reference_number` | new REQUIRED field [reference_number] |
| `component_schema_required_field_added` | `components.schemas.ZakatSessionResource.properties.worksheet` | new REQUIRED field [worksheet] |
| `operation_added` | `paths./api/accountant/accounting/financial-periods.get` | GET /api/accountant/accounting/financial-periods added to the contract |
| `operation_added` | `paths./api/accountant/accounting/financial-periods.post` | POST /api/accountant/accounting/financial-periods added to the contract |
| `response_schema_type_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.action_link` | new REQUIRED field [action_link] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.assigned_accountant_reference` | new REQUIRED field [assigned_accountant_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.due_date` | new REQUIRED field [due_date] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.linked_process_reference` | new REQUIRED field [linked_process_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.name` | new REQUIRED field [name] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.overdue` | new REQUIRED field [overdue] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.reason` | new REQUIRED field [reason] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.reference` | new REQUIRED field [reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.source_module` | new REQUIRED field [source_module] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.source_operation` | new REQUIRED field [source_operation] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.source_type` | new REQUIRED field [source_type] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.status` | new REQUIRED field [status] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.task_type` | new REQUIRED field [task_type] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.type` | new REQUIRED field [type] |
| `response_schema_enum_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.last_evaluation.properties.evaluated_by_kind` | enum constraint added |
| `response_schema_enum_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.last_evaluation.properties.status` | enum constraint added |
| `response_schema_enum_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.period.properties.status` | enum constraint added |
| `response_schema_enum_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | enum constraint added |
| `response_schema_type_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.action_link` | new REQUIRED field [action_link] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.assigned_accountant_reference` | new REQUIRED field [assigned_accountant_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.due_date` | new REQUIRED field [due_date] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.linked_process_reference` | new REQUIRED field [linked_process_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.name` | new REQUIRED field [name] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.overdue` | new REQUIRED field [overdue] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.reason` | new REQUIRED field [reason] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.reference` | new REQUIRED field [reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.source_module` | new REQUIRED field [source_module] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.source_operation` | new REQUIRED field [source_operation] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.source_type` | new REQUIRED field [source_type] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.status` | new REQUIRED field [status] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.task_type` | new REQUIRED field [task_type] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.type` | new REQUIRED field [type] |
| `response_schema_type_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.action_link` | new REQUIRED field [action_link] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.assigned_accountant_reference` | new REQUIRED field [assigned_accountant_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.due_date` | new REQUIRED field [due_date] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.linked_process_reference` | new REQUIRED field [linked_process_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.name` | new REQUIRED field [name] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.overdue` | new REQUIRED field [overdue] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.reason` | new REQUIRED field [reason] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.reference` | new REQUIRED field [reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.source_module` | new REQUIRED field [source_module] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.source_operation` | new REQUIRED field [source_operation] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.source_type` | new REQUIRED field [source_type] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.status` | new REQUIRED field [status] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.task_type` | new REQUIRED field [task_type] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.type` | new REQUIRED field [type] |
| `response_schema_enum_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.last_evaluation.properties.evaluated_by_kind` | enum constraint added |
| `response_schema_enum_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.last_evaluation.properties.status` | enum constraint added |
| `response_schema_enum_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.period.properties.status` | enum constraint added |
| `response_schema_enum_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | enum constraint added |
| `response_schema_type_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.action_link` | new REQUIRED field [action_link] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.assigned_accountant_reference` | new REQUIRED field [assigned_accountant_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.due_date` | new REQUIRED field [due_date] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.linked_process_reference` | new REQUIRED field [linked_process_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.name` | new REQUIRED field [name] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.overdue` | new REQUIRED field [overdue] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.reason` | new REQUIRED field [reason] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.reference` | new REQUIRED field [reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.source_module` | new REQUIRED field [source_module] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.source_operation` | new REQUIRED field [source_operation] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.source_type` | new REQUIRED field [source_type] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.status` | new REQUIRED field [status] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.task_type` | new REQUIRED field [task_type] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.warnings.items.properties.type` | new REQUIRED field [type] |
| `response_schema_type_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items` | type added (any -> ['object']) |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.action_link` | new REQUIRED field [action_link] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.assigned_accountant_reference` | new REQUIRED field [assigned_accountant_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.due_date` | new REQUIRED field [due_date] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.linked_process_reference` | new REQUIRED field [linked_process_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.name` | new REQUIRED field [name] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.overdue` | new REQUIRED field [overdue] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.reason` | new REQUIRED field [reason] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.reference` | new REQUIRED field [reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.source_module` | new REQUIRED field [source_module] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.source_operation` | new REQUIRED field [source_operation] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.source_type` | new REQUIRED field [source_type] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.status` | new REQUIRED field [status] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.task_type` | new REQUIRED field [task_type] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blockers.items.properties.type` | new REQUIRED field [type] |
| `response_schema_enum_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.period.properties.status` | enum constraint added |
| `response_schema_enum_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary.properties.readiness_status` | enum constraint added |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.close_sequence` | new REQUIRED field [close_sequence] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.closed_at` | new REQUIRED field [closed_at] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.closed_by_reference` | new REQUIRED field [closed_by_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.period_reference` | new REQUIRED field [period_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.period_status` | new REQUIRED field [period_status] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.reference` | new REQUIRED field [reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.replayed` | new REQUIRED field [replayed] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.summary` | new REQUIRED field [summary] |
| `response_status_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.post.responses.201` | response [201] added to the contract |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/history.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.summary.properties.completed_tasks` | new REQUIRED field [completed_tasks] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/history.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.summary.properties.completion_percent` | new REQUIRED field [completion_percent] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/history.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.summary.properties.overdue_tasks` | new REQUIRED field [overdue_tasks] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/history.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.summary.properties.pending_requirements` | new REQUIRED field [pending_requirements] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/history.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.summary.properties.readiness_status` | new REQUIRED field [readiness_status] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/history.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.summary.properties.remaining_tasks` | new REQUIRED field [remaining_tasks] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/history.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.summary.properties.total_tasks` | new REQUIRED field [total_tasks] |
| `operation_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/reopen.post` | POST /api/accountant/accounting/financial-periods/{periodId}/closing/reopen added to the contract |
| `response_schema_enum_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.display_status` | enum constraint added |
| `response_schema_enum_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.priority` | enum constraint added |
| `response_schema_enum_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.source` | enum constraint added |
| `response_schema_enum_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.status` | enum constraint added |
| `response_schema_enum_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.task_type` | enum constraint added |
| `response_schema_enum_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta.properties.fiscal_period.properties.status` | enum constraint added |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.assigned_accountant_reference` | new REQUIRED field [assigned_accountant_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.assigned_by_reference` | new REQUIRED field [assigned_by_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.attachments` | new REQUIRED field [attachments] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.blocks_close` | new REQUIRED field [blocks_close] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.company_id` | new REQUIRED field [company_id] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.completed_at` | new REQUIRED field [completed_at] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.completed_by_reference` | new REQUIRED field [completed_by_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.created_at` | new REQUIRED field [created_at] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.definition` | new REQUIRED field [definition] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.description` | new REQUIRED field [description] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.display_status` | new REQUIRED field [display_status] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.due_date` | new REQUIRED field [due_date] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.fiscal_period_reference` | new REQUIRED field [fiscal_period_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.is_overdue` | new REQUIRED field [is_overdue] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.name` | new REQUIRED field [name] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.notes` | new REQUIRED field [notes] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.priority` | new REQUIRED field [priority] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.related` | new REQUIRED field [related] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.source` | new REQUIRED field [source] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.started_at` | new REQUIRED field [started_at] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | new REQUIRED field [status] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.task_type` | new REQUIRED field [task_type] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.version` | new REQUIRED field [version] |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.waiting_reason` | new REQUIRED field [waiting_reason] |
| `response_status_added` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.201` | response [201] added to the contract |
| `response_schema_required_field_added` | `paths./api/accountant/accounting/journal-entries.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.meta` | new REQUIRED field [meta] |
| `request_schema_field_added` | `paths./api/accountant/accounting/journal-entries/{id}/amend.post.requestBody.content.application/json.schema.properties.amended_data.properties.lines.items.properties.account_reference` | new optional field [account_reference] |
| `operation_added` | `paths./api/accountant/accounting/journal-entry-requests.get` | GET /api/accountant/accounting/journal-entry-requests added to the contract |
| `operation_added` | `paths./api/accountant/accounting/posting-mappings.get` | GET /api/accountant/accounting/posting-mappings added to the contract |
| `operation_added` | `paths./api/accountant/accounting/posting-mappings/missing.get` | GET /api/accountant/accounting/posting-mappings/missing added to the contract |
| `operation_added` | `paths./api/accountant/accounting/posting-mappings/{reference}/unassign.post` | POST /api/accountant/accounting/posting-mappings/{reference}/unassign added to the contract |
| `operation_added` | `paths./api/accountant/accounting/posting-mappings/{role}.put` | PUT /api/accountant/accounting/posting-mappings/{role} added to the contract |
| `operation_added` | `paths./api/accountant/accounting/posting-requests.get` | GET /api/accountant/accounting/posting-requests added to the contract |
| `operation_added` | `paths./api/accountant/accounting/posting-requests/reprocess.post` | POST /api/accountant/accounting/posting-requests/reprocess added to the contract |
| `operation_added` | `paths./api/accountant/accounting/posting-requests/{reference}.get` | GET /api/accountant/accounting/posting-requests/{reference} added to the contract |
| `operation_added` | `paths./api/accountant/accounting/posting-requests/{reference}/closed-period-correction.post` | POST /api/accountant/accounting/posting-requests/{reference}/closed-period-correction added to the contract |
| `operation_added` | `paths./api/accountant/accounting/posting-requests/{reference}/reprocess.post` | POST /api/accountant/accounting/posting-requests/{reference}/reprocess added to the contract |
| `operation_added` | `paths./api/accountant/accounting/posting-roles.get` | GET /api/accountant/accounting/posting-roles added to the contract |
| `operation_added` | `paths./api/accountant/accounting/posting-templates.get` | GET /api/accountant/accounting/posting-templates added to the contract |
| `operation_added` | `paths./api/accountant/accounting/posting-templates/{template}/apply.post` | POST /api/accountant/accounting/posting-templates/{template}/apply added to the contract |
| `operation_added` | `paths./api/accountant/accounting/reconciliation/bank-accounts.get` | GET /api/accountant/accounting/reconciliation/bank-accounts added to the contract |
| `operation_added` | `paths./api/accountant/accounting/reconciliation/bank-accounts.post` | POST /api/accountant/accounting/reconciliation/bank-accounts added to the contract |
| `operation_added` | `paths./api/accountant/accounting/reconciliation/bank-accounts/{id}.get` | GET /api/accountant/accounting/reconciliation/bank-accounts/{id} added to the contract |
| `operation_added` | `paths./api/accountant/accounting/reconciliation/bank-accounts/{id}.patch` | PATCH /api/accountant/accounting/reconciliation/bank-accounts/{id} added to the contract |
| `operation_added` | `paths./api/accountant/accounting/reconciliation/bank-statements.get` | GET /api/accountant/accounting/reconciliation/bank-statements added to the contract |
| `operation_added` | `paths./api/accountant/accounting/reconciliation/bank-transactions.get` | GET /api/accountant/accounting/reconciliation/bank-transactions added to the contract |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.account_reference` | new REQUIRED field [account_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.accountant_reference` | new REQUIRED field [accountant_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.amount_before_tax` | new REQUIRED field [amount_before_tax] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.approved_at` | new REQUIRED field [approved_at] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.approved_version` | new REQUIRED field [approved_version] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.branch_id` | new REQUIRED field [branch_id] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.classification_review_reason` | new REQUIRED field [classification_review_reason] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.classification_status` | new REQUIRED field [classification_status] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.description` | new REQUIRED field [description] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.document_path` | new REQUIRED field [document_path] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.document_url` | new REQUIRED field [document_url] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.due_date` | new REQUIRED field [due_date] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.expense_category` | new REQUIRED field [expense_category] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.invoice_date` | new REQUIRED field [invoice_date] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.invoice_number` | new REQUIRED field [invoice_number] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.journal_entry_reference` | new REQUIRED field [journal_entry_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.journal_posted_at` | new REQUIRED field [journal_posted_at] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.notes` | new REQUIRED field [notes] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.operation_type` | new REQUIRED field [operation_type] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.payment_method` | new REQUIRED field [payment_method] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.payment_status` | new REQUIRED field [payment_status] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.posting_requested_at` | new REQUIRED field [posting_requested_at] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.public_reference` | new REQUIRED field [public_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.source` | new REQUIRED field [source] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | new REQUIRED field [status] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.suggested_expense_category` | new REQUIRED field [suggested_expense_category] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.suggested_operation_type` | new REQUIRED field [suggested_operation_type] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.supplier_reference` | new REQUIRED field [supplier_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.suspicion_reason` | new REQUIRED field [suspicion_reason] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.total_amount` | new REQUIRED field [total_amount] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.vat_amount` | new REQUIRED field [vat_amount] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.version` | new REQUIRED field [version] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.po_number` | new REQUIRED field [po_number] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.uploaded_by_reference` | new REQUIRED field [uploaded_by_reference] |
| `response_schema_required_field_added` | `paths./api/accountant/expenses/expenses/{reference}/payment-status.put.responses.200.content.application/json.schema.allOf[1].properties.data.anyOf[0].properties.vendor_name` | new REQUIRED field [vendor_name] |
| `operation_added` | `paths./api/accountant/expenses/expenses/{reference}/reject.post` | POST /api/accountant/expenses/expenses/{reference}/reject added to the contract |
| `operation_added` | `paths./api/accountant/general/closing-accountants.get` | GET /api/accountant/general/closing-accountants added to the contract |
| `response_schema_enum_added` | `paths./api/accountant/general/closing-tasks/{taskId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.display_status` | enum constraint added |
| `response_schema_enum_added` | `paths./api/accountant/general/closing-tasks/{taskId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.priority` | enum constraint added |
| `response_schema_enum_added` | `paths./api/accountant/general/closing-tasks/{taskId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.source` | enum constraint added |
| `response_schema_enum_added` | `paths./api/accountant/general/closing-tasks/{taskId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | enum constraint added |
| `response_schema_enum_added` | `paths./api/accountant/general/closing-tasks/{taskId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.task_type` | enum constraint added |
| `response_schema_enum_added` | `paths./api/accountant/general/closing-tasks/{taskId}.patch.responses.200.content.application/json.schema.allOf[1].properties.data.properties.display_status` | enum constraint added |
| `response_schema_enum_added` | `paths./api/accountant/general/closing-tasks/{taskId}.patch.responses.200.content.application/json.schema.allOf[1].properties.data.properties.priority` | enum constraint added |
| `response_schema_enum_added` | `paths./api/accountant/general/closing-tasks/{taskId}.patch.responses.200.content.application/json.schema.allOf[1].properties.data.properties.source` | enum constraint added |
| `response_schema_enum_added` | `paths./api/accountant/general/closing-tasks/{taskId}.patch.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | enum constraint added |
| `response_schema_enum_added` | `paths./api/accountant/general/closing-tasks/{taskId}.patch.responses.200.content.application/json.schema.allOf[1].properties.data.properties.task_type` | enum constraint added |
| `operation_added` | `paths./api/accountant/general/closing-tasks/{taskId}/attachments/{attachmentId}.get` | GET /api/accountant/general/closing-tasks/{taskId}/attachments/{attachmentId} added to the contract |
| `response_schema_enum_added` | `paths./api/accountant/general/closing-tasks/{taskId}/complete.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.display_status` | enum constraint added |
| `response_schema_enum_added` | `paths./api/accountant/general/closing-tasks/{taskId}/complete.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.priority` | enum constraint added |
| `response_schema_enum_added` | `paths./api/accountant/general/closing-tasks/{taskId}/complete.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.source` | enum constraint added |
| `response_schema_enum_added` | `paths./api/accountant/general/closing-tasks/{taskId}/complete.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.status` | enum constraint added |
| `response_schema_enum_added` | `paths./api/accountant/general/closing-tasks/{taskId}/complete.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.task_type` | enum constraint added |
| `operation_added` | `paths./api/accountant/general/companies.get` | GET /api/accountant/general/companies added to the contract |
| `optional_parameter_added` | `paths./api/accountant/general/return-notes.get.parameters.page` | optional parameter [page] (in query) added |
| `operation_added` | `paths./api/accountant/general/vat-returns/{vatReturn}/approve.post` | POST /api/accountant/general/vat-returns/{vatReturn}/approve added to the contract |
| `operation_added` | `paths./api/accountant/general/vat-returns/{vatReturn}/export.post` | POST /api/accountant/general/vat-returns/{vatReturn}/export added to the contract |
| `operation_added` | `paths./api/accountant/general/vat-returns/{vatReturn}/preparation.get` | GET /api/accountant/general/vat-returns/{vatReturn}/preparation added to the contract |
| `operation_added` | `paths./api/accountant/inventory/catalog-categories.get` | GET /api/accountant/inventory/catalog-categories added to the contract |
| `operation_added` | `paths./api/accountant/inventory/catalog-products.get` | GET /api/accountant/inventory/catalog-products added to the contract |
| `operation_added` | `paths./api/accountant/inventory/catalog-products/{catalogProduct}.get` | GET /api/accountant/inventory/catalog-products/{catalogProduct} added to the contract |
| `operation_added` | `paths./api/accountant/inventory/inventory/items.get` | GET /api/accountant/inventory/inventory/items added to the contract |
| `operation_added` | `paths./api/accountant/inventory/inventory/items/{item}.get` | GET /api/accountant/inventory/inventory/items/{item} added to the contract |
| `operation_added` | `paths./api/accountant/inventory/inventory/movements.get` | GET /api/accountant/inventory/inventory/movements added to the contract |
| `operation_added` | `paths./api/accountant/inventory/waste/records.get` | GET /api/accountant/inventory/waste/records added to the contract |
| `optional_request_body_added` | `paths./api/accountant/meetings/meetings/{meetingReference}/provider/retry.post.requestBody` | request body added (optional) |
| `operation_added` | `paths./api/accountant/notifications/notifications.get` | GET /api/accountant/notifications/notifications added to the contract |
| `operation_added` | `paths./api/accountant/notifications/notifications/read-all.post` | POST /api/accountant/notifications/notifications/read-all added to the contract |
| `operation_added` | `paths./api/accountant/notifications/notifications/unread-count.get` | GET /api/accountant/notifications/notifications/unread-count added to the contract |
| `operation_added` | `paths./api/accountant/notifications/notifications/{uuid}.get` | GET /api/accountant/notifications/notifications/{uuid} added to the contract |
| `operation_added` | `paths./api/accountant/notifications/notifications/{uuid}/read.post` | POST /api/accountant/notifications/notifications/{uuid}/read added to the contract |
| `operation_added` | `paths./api/accountant/notifications/notifications/{uuid}/unread.post` | POST /api/accountant/notifications/notifications/{uuid}/unread added to the contract |
| `operation_added` | `paths./api/accountant/payroll/payroll/runs/{runId}/return-to-draft.post` | POST /api/accountant/payroll/payroll/runs/{runId}/return-to-draft added to the contract |
| `response_schema_required_field_added` | `paths./api/accountant/pricing/pricing/finalize-price.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.materials.items.properties.id` | new REQUIRED field [id] |
| `response_schema_required_field_added` | `paths./api/accountant/pricing/pricing/finalize-price.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.submitted_by_name` | new REQUIRED field [submitted_by_name] |

_… and 1487 more (see the JSON report)._

## Documentation-only changes (389)

| Kind | Location | Detail |
|---|---|---|
| `component_schema_documentation` | `components.schemas.AccountantDetailsResource.properties.public_reference` | description changed |
| `component_schema_documentation` | `components.schemas.AccountantOperationalDashboardResource.properties.branch_id` | description changed |
| `component_schema_documentation` | `components.schemas.AccountantOperationalDashboardResource.properties.branch_performance` | description changed |
| `component_schema_documentation` | `components.schemas.AccountantOperationalDashboardResource.properties.company_id` | description changed |
| `component_schema_documentation` | `components.schemas.AccountantOperationalDashboardResource.properties.tenant_id` | description changed |
| `component_schema_documentation` | `components.schemas.CreateRoleRequest.properties.description` | description changed |
| `component_schema_documentation` | `components.schemas.CreateSupplierRequest` | description changed |
| `component_schema_reference_shape` | `components.schemas.CreateSupplierRequest.properties.supplier_type` | schema moved between $ref and inline definition (same effective shape) |
| `component_schema_documentation` | `components.schemas.CustomizeMonthlyReportRequest` | description changed |
| `component_schema_documentation` | `components.schemas.InitiatePaymentRequest.properties.payment_data` | description changed |
| `component_schema_documentation` | `components.schemas.PortfolioCompanyResource.properties.net_profit` | description changed |
| `component_schema_documentation` | `components.schemas.PortfolioCompanyResource.properties.public_reference` | description changed |
| `component_schema_documentation` | `components.schemas.PortfolioCompanyResource.properties.revenue` | description changed |
| `component_schema_documentation` | `components.schemas.RegisterApplicationRequest` | description changed |
| `component_schema_documentation` | `components.schemas.RegistrationApplication.properties.status` | description changed |
| `component_schema_documentation` | `components.schemas.RegistrationApplicationStatus` | description changed |
| `component_schema_documentation` | `components.schemas.RenewAdminSubscriptionRequest` | description changed |
| `component_schema_documentation` | `components.schemas.SendRegistrationCodeRequest` | description changed |
| `component_schema_documentation` | `components.schemas.StoreExpenseRequest` | description changed |
| `component_schema_documentation` | `components.schemas.StoreExpenseRequest.properties.payment_method` | title changed |
| `component_schema_documentation` | `components.schemas.Subscription.properties.status` | description changed |
| `component_schema_reference_shape` | `components.schemas.Subscription.properties.status` | schema moved between $ref and inline definition (same effective shape) |
| `component_schema_documentation` | `components.schemas.SubscriptionStatus` | description changed |
| `component_schema_documentation` | `components.schemas.UpdateBranchRequest.properties.name` | description changed |
| `component_schema_documentation` | `components.schemas.UpdateRoleRequest.properties.description` | description changed |
| `component_schema_documentation` | `components.schemas.UpdateSupplierRequest` | description changed |
| `component_schema_documentation` | `components.schemas.UpdateSupplierRequest.properties.name` | description changed |
| `component_schema_documentation` | `components.schemas.UploadRegistrationPaymentProofRequest.properties.transfer_proof` | description changed |
| `component_schema_documentation` | `components.schemas.UploadSupplementalTaxDocumentRequest` | description changed |
| `response_description_changed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing.get.responses.200.description` | response description changed |
| `response_description_changed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/check.post.responses.200.description` | response description changed |
| `response_description_changed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.get.responses.200.description` | response description changed |
| `response_description_changed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/close.post.responses.200.description` | response description changed |
| `response_description_changed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/history.get.responses.200.description` | response description changed |
| `response_schema_documentation` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.display_status` | description changed |
| `request_schema_documentation` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.requestBody.content.application/json.schema.properties.accountant_reference` | description changed |
| `response_schema_documentation` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_description_changed` | `paths./api/accountant/accounting/financial-periods/{periodId}/closing/tasks.post.responses.200.description` | response description changed |
| `operation_documentation` | `paths./api/accountant/accounting/journal-entries.get.description` | description changed |
| `response_status_added` | `paths./api/accountant/accounting/journal-entries.get.responses.422` | response [422] added to the contract |
| `operation_documentation` | `paths./api/accountant/expenses/expenses/{reference}/return.post.summary` | summary changed |
| `operation_extension_changed` | `paths./api/accountant/expenses/expenses/{reference}/return.post.x-access` | vendor extension [x-access] changed |
| `response_schema_documentation` | `paths./api/accountant/general/closing-tasks/{taskId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.display_status` | description changed |
| `response_schema_documentation` | `paths./api/accountant/general/closing-tasks/{taskId}.patch.responses.200.content.application/json.schema.allOf[1].properties.data.properties.display_status` | description changed |
| `response_schema_documentation` | `paths./api/accountant/general/closing-tasks/{taskId}/complete.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.display_status` | description changed |
| `operation_documentation` | `paths./api/accountant/meetings/meetings/{meetingReference}/join-link.get.summary` | summary changed |
| `operation_extension_changed` | `paths./api/accountant/meetings/meetings/{meetingReference}/join-link.get.x-access` | vendor extension [x-access] changed |
| `operation_documentation` | `paths./api/accountant/meetings/meetings/{meetingReference}/join.get.summary` | summary changed |
| `operation_extension_changed` | `paths./api/accountant/meetings/meetings/{meetingReference}/join.get.x-access` | vendor extension [x-access] changed |
| `operation_extension_changed` | `paths./api/accountant/meetings/meetings/{meetingReference}/provider/retry.post.x-access` | vendor extension [x-access] changed |
| `response_description_changed` | `paths./api/accountant/reports/monthly-reports.post.responses.200.description` | response description changed |
| `response_description_changed` | `paths./api/accountant/reports/monthly-reports/{reportId}/commentary.put.responses.200.description` | response description changed |
| `response_description_changed` | `paths./api/accountant/reports/monthly-reports/{reportId}/document.get.responses.200.description` | response description changed |
| `response_description_changed` | `paths./api/accountant/reports/monthly-reports/{reportId}/publish.post.responses.200.description` | response description changed |
| `response_description_changed` | `paths./api/accountant/reports/monthly-reports/{reportId}/ready.post.responses.200.description` | response description changed |
| `response_description_changed` | `paths./api/accountant/reports/monthly-reports/{reportId}/refresh-draft.post.responses.200.description` | response description changed |
| `response_description_changed` | `paths./api/accountant/reports/monthly-reports/{reportId}/versions.get.responses.200.description` | response description changed |
| `operation_documentation` | `paths./api/accountant/sales/customers/{id}/invoices.get.summary` | summary changed |
| `operation_documentation` | `paths./api/admin/admin-roles.get.summary` | summary changed |
| `operation_documentation` | `paths./api/admin/admin-roles/{roleReference}.get.summary` | summary changed |
| `parameter_documentation` | `paths./api/admin/clients/registration-requests/{id}.get.parameters.id.description` | parameter description changed |
| `operation_documentation` | `paths./api/admin/clients/registration-requests/{id}.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/admin/clients/registration-requests/{id}/approve.post.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/admin/clients/registration-requests/{id}/approve.post.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `operation_documentation` | `paths./api/admin/clients/registration-requests/{id}/approve.post.summary` | summary changed |
| `request_schema_documentation` | `paths./api/admin/clients/registration-requests/{id}/payment/verify.post.requestBody.content.application/json.schema` | title changed |
| `request_schema_documentation` | `paths./api/admin/clients/registration-requests/{id}/payment/verify.post.requestBody.content.application/json.schema` | description changed |
| `request_schema_reference_shape` | `paths./api/admin/clients/registration-requests/{id}/payment/verify.post.requestBody.content.application/json.schema` | schema moved between $ref and inline definition (same effective shape) |
| `operation_documentation` | `paths./api/admin/clients/registration-requests/{id}/payment/verify.post.summary` | summary changed |
| `response_schema_documentation` | `paths./api/admin/clients/registration-requests/{id}/reject.post.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/admin/clients/registration-requests/{id}/reject.post.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `operation_documentation` | `paths./api/admin/clients/registration-requests/{id}/reject.post.summary` | summary changed |
| `response_schema_documentation` | `paths./api/admin/clients/registration-requests/{id}/request-info.post.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/admin/clients/registration-requests/{id}/request-info.post.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/admin/reports/accountant-assignments.get.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/admin/reports/accountant-assignments.get.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/admin/reports/accountant-workload.get.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/admin/reports/accountant-workload.get.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/admin/reports/clients.get.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/admin/reports/clients.get.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/admin/reports/renewals.get.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/admin/reports/renewals.get.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/admin/reports/subscriptions.get.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/admin/reports/subscriptions.get.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/admin/reports/suppliers.get.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/admin/reports/suppliers.get.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/admin/reports/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/admin/reports/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/auth/account/profile.post.responses.200.content.application/json.schema.properties.data.properties.status` | description changed |
| `response_status_added` | `paths./api/auth/accountant/meetings.get.responses.422` | response [422] added to the contract |
| `operation_documentation` | `paths./api/auth/accountant/meetings.get.summary` | summary changed |
| `response_status_added` | `paths./api/auth/accounting/financial-statements.get.responses.422` | response [422] added to the contract |
| `operation_documentation` | `paths./api/auth/bootstrap.get.description` | description changed |
| `operation_documentation` | `paths./api/auth/bootstrap.get.summary` | summary changed |
| `request_schema_documentation` | `paths./api/auth/login.post.requestBody.content.application/json.schema` | title changed |
| `request_schema_documentation` | `paths./api/auth/login.post.requestBody.content.application/json.schema` | description changed |
| `request_schema_reference_shape` | `paths./api/auth/login.post.requestBody.content.application/json.schema` | schema moved between $ref and inline definition (same effective shape) |
| `operation_documentation` | `paths./api/auth/onboarding/applications/send-code.post.summary` | summary changed |
| `operation_documentation` | `paths./api/auth/subscriptions/registration-request.get.description` | description changed |
| `operation_documentation` | `paths./api/auth/subscriptions/registration-request.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/auth/subscriptions/registration-status.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.payment_status` | description changed |
| `operation_documentation` | `paths./api/auth/subscriptions/registration.put.description` | description changed |
| `operation_documentation` | `paths./api/auth/subscriptions/registration/resubmit.post.description` | description changed |
| `request_schema_documentation` | `paths./api/auth/subscriptions/registration/resubmit.post.requestBody.content.application/json.schema` | title changed |
| `request_schema_documentation` | `paths./api/auth/subscriptions/registration/resubmit.post.requestBody.content.application/json.schema` | description changed |
| `request_schema_reference_shape` | `paths./api/auth/subscriptions/registration/resubmit.post.requestBody.content.application/json.schema` | schema moved between $ref and inline definition (same effective shape) |
| `response_status_added` | `paths./api/auth/subscriptions/registration/resubmit.post.responses.404` | response [404] added to the contract |
| `operation_documentation` | `paths./api/auth/subscriptions/registration/resubmit.post.summary` | summary changed |
| `response_schema_documentation` | `paths./api/owner/accounting/general-ledger.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_documentation` | `paths./api/owner/accounting/journal-entries.get.description` | description changed |
| `response_status_added` | `paths./api/owner/accounting/journal-entries.get.responses.422` | response [422] added to the contract |
| `response_schema_documentation` | `paths./api/owner/dashboard/owner.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/owner/expenses/expenses.post.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/owner/expenses/expenses.post.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_description_changed` | `paths./api/owner/expenses/expenses.post.responses.200.description` | response description changed |
| `operation_documentation` | `paths./api/owner/general/admin/roles.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/owner/general/admin/roles/{roleReference}/permissions.put.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_documentation` | `paths./api/owner/inventory/catalog-products.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/owner/inventory/catalog-products/{catalogProduct}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/owner/inventory/catalog/products/{productReference}/recipe-components.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items` | title changed |
| `response_schema_reference_shape` | `paths./api/owner/inventory/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items` | schema moved between $ref and inline definition (same effective shape) |
| `response_status_added` | `paths./api/owner/inventory/inventory/items.get.responses.422` | response [422] added to the contract |
| `operation_documentation` | `paths./api/owner/inventory/inventory/items.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/owner/inventory/waste/analytics.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/owner/inventory/waste/analytics.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/owner/inventory/waste/analytics.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/owner/meetings/meetings/availability.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/owner/notifications/notifications.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/owner/notifications/notifications/{uuid}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/owner/payroll/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/owner/payroll/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `operation_documentation` | `paths./api/owner/payroll/payroll/employees.post.summary` | summary changed |
| `operation_documentation` | `paths./api/owner/payroll/payroll/employees/{publicReference}.patch.summary` | summary changed |
| `parameter_schema_documentation` | `paths./api/owner/purchases/purchase-orders.get.parameters.status.schema` | title changed |
| `parameter_schema_documentation` | `paths./api/owner/purchases/purchase-orders.get.parameters.status.schema` | description changed |
| `response_schema_documentation` | `paths./api/owner/purchases/suppliers.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/owner/purchases/suppliers/{id}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/owner/reports/monthly-reports/{reportId}.get.responses.200.description` | response description changed |
| `response_description_changed` | `paths./api/owner/reports/monthly-reports/{reportId}/document.get.responses.200.description` | response description changed |
| `response_description_changed` | `paths./api/owner/reports/monthly-reports/{reportId}/versions.get.responses.200.description` | response description changed |
| `parameter_documentation` | `paths./api/owner/reports/owner/reporting/financial.get.parameters.expense_category_id.description` | parameter description changed |
| `response_schema_documentation` | `paths./api/owner/reports/owner/reporting/financial.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/owner/reports/owner/reporting/financial.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/owner/reports/owner/reporting/financial.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `operation_documentation` | `paths./api/owner/sales/customers/{id}/invoices.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/owner/settings/audit-log.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.log.items.properties.user_id` | description changed |
| `response_schema_documentation` | `paths./api/owner/settings/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/owner/settings/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/owner/settings/branches/selectable.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/owner/settings/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `operation_documentation` | `paths./api/owner/settings/identity/users/{userReference}.delete.summary` | summary changed |
| `response_schema_documentation` | `paths./api/owner/settings/organizations/current.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_documentation` | `paths./api/owner/settings/users.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/owner/settings/users/form-options.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.roles.items.properties.description` | description changed |
| `operation_documentation` | `paths./api/public/general/countries.get.description` | description changed |
| `operation_documentation` | `paths./api/public/general/countries.get.summary` | summary changed |
| `parameter_documentation` | `paths./api/public/support/page.get.parameters.type.description` | parameter description changed |
| `parameter_schema_documentation` | `paths./api/public/support/page.get.parameters.type.schema` | title changed |
| `parameter_schema_documentation` | `paths./api/public/support/page.get.parameters.type.schema` | description changed |
| `parameter_schema_reference_shape` | `paths./api/public/support/page.get.parameters.type.schema` | schema moved between $ref and inline definition (same effective shape) |
| `response_status_removed` | `paths./api/public/support/page.get.responses.400` | response [400] removed from the contract |
| `response_status_added` | `paths./api/public/support/page.get.responses.422` | response [422] added to the contract |
| `operation_documentation` | `paths./api/public/support/page.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/v1/account/profile.post.responses.200.content.application/json.schema.properties.data.properties.status` | description changed |
| `response_status_added` | `paths./api/v1/accountant/meetings.get.responses.422` | response [422] added to the contract |
| `operation_documentation` | `paths./api/v1/accountant/meetings.get.summary` | summary changed |
| `operation_documentation` | `paths./api/v1/accountant/meetings/{meetingReference}/join-link.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/accountant/meetings/{meetingReference}/join-link.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/accountant/meetings/{meetingReference}/join-link.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/accountant/meetings/{meetingReference}/join.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/accountant/meetings/{meetingReference}/join.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/accountant/meetings/{meetingReference}/join.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/accountant/meetings/{meetingReference}/provider/retry.post.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/accountant/meetings/{meetingReference}/provider/retry.post.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/accountant/meetings/{meetingReference}/provider/retry.post.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/accounting/financial-statements.get.description` | description changed |
| `response_status_added` | `paths./api/v1/accounting/financial-statements.get.responses.422` | response [422] added to the contract |
| `operation_tags_changed` | `paths./api/v1/accounting/financial-statements.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/accounting/financial-statements.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/accounting/financial-statements/{statement}.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/accounting/financial-statements/{statement}.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/accounting/financial-statements/{statement}.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/accounting/journal-entries.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/accounting/journal-entries.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/accounting/journal-entries.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/accounting/journal-entries/{reference}.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/accounting/journal-entries/{reference}.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/accounting/journal-entries/{reference}.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/accounting/reports/trial-balance.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/accounting/reports/trial-balance.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/accounting/reports/trial-balance.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/accounts.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/accounts.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/accounts.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/admin/roles.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/v1/admin/roles/{roleReference}/permissions.put.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_documentation` | `paths./api/v1/audit-log.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.log.items.properties.user_id` | description changed |
| `request_schema_documentation` | `paths./api/v1/auth/login.post.requestBody.content.application/json.schema` | title changed |
| `request_schema_documentation` | `paths./api/v1/auth/login.post.requestBody.content.application/json.schema` | description changed |
| `request_schema_reference_shape` | `paths./api/v1/auth/login.post.requestBody.content.application/json.schema` | schema moved between $ref and inline definition (same effective shape) |
| `operation_documentation` | `paths./api/v1/bootstrap.get.description` | description changed |
| `operation_documentation` | `paths./api/v1/bootstrap.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/v1/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/v1/branches.post.responses.201.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/v1/branches/selectable.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/v1/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/v1/branches/{reference}.put.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `operation_documentation` | `paths./api/v1/catalog-categories.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/catalog-categories.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/catalog-categories.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/catalog-products.get.description` | description changed |
| `response_schema_documentation` | `paths./api/v1/catalog-products.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_tags_changed` | `paths./api/v1/catalog-products.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/catalog-products.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/catalog-products/{catalogProduct}.get.description` | description changed |
| `response_schema_documentation` | `paths./api/v1/catalog-products/{catalogProduct}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_tags_changed` | `paths./api/v1/catalog-products/{catalogProduct}.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/catalog-products/{catalogProduct}.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `response_schema_documentation` | `paths./api/v1/catalog/products/{productReference}/recipe-components.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_schema_documentation` | `paths./api/v1/closing-tasks/{taskId}.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.display_status` | description changed |
| `response_schema_documentation` | `paths./api/v1/closing-tasks/{taskId}.patch.responses.200.content.application/json.schema.allOf[1].properties.data.properties.display_status` | description changed |
| `response_schema_documentation` | `paths./api/v1/closing-tasks/{taskId}/complete.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.display_status` | description changed |
| `parameter_documentation` | `paths./api/v1/content/support/page.get.parameters.type.description` | parameter description changed |
| `parameter_schema_documentation` | `paths./api/v1/content/support/page.get.parameters.type.schema` | title changed |
| `parameter_schema_documentation` | `paths./api/v1/content/support/page.get.parameters.type.schema` | description changed |
| `parameter_schema_reference_shape` | `paths./api/v1/content/support/page.get.parameters.type.schema` | schema moved between $ref and inline definition (same effective shape) |
| `response_status_removed` | `paths./api/v1/content/support/page.get.responses.400` | response [400] removed from the contract |
| `response_status_added` | `paths./api/v1/content/support/page.get.responses.422` | response [422] added to the contract |
| `operation_documentation` | `paths./api/v1/content/support/page.get.summary` | summary changed |
| `operation_documentation` | `paths./api/v1/customer-balances.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/customer-balances.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/customer-balances.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/customers/{id}.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/customers/{id}.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/customers/{id}.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/customers/{id}/financial-summary.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/customers/{id}/financial-summary.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/customers/{id}/financial-summary.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/customers/{id}/invoices.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/v1/dashboards/owner.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_documentation` | `paths./api/v1/erp/notifications.get.description` | description changed |
| `response_schema_documentation` | `paths./api/v1/erp/notifications.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_tags_changed` | `paths./api/v1/erp/notifications.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/erp/notifications.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/erp/notifications/read-all.post.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/erp/notifications/read-all.post.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/erp/notifications/read-all.post.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/erp/notifications/unread-count.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/erp/notifications/unread-count.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/erp/notifications/unread-count.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/erp/notifications/{uuid}.get.description` | description changed |
| `response_schema_documentation` | `paths./api/v1/erp/notifications/{uuid}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_tags_changed` | `paths./api/v1/erp/notifications/{uuid}.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/erp/notifications/{uuid}.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/erp/notifications/{uuid}/read.post.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/erp/notifications/{uuid}/read.post.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/erp/notifications/{uuid}/read.post.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/erp/notifications/{uuid}/unread.post.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/erp/notifications/{uuid}/unread.post.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/erp/notifications/{uuid}/unread.post.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `response_schema_documentation` | `paths./api/v1/expenses.post.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/v1/expenses.post.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_description_changed` | `paths./api/v1/expenses.post.responses.200.description` | response description changed |
| `operation_documentation` | `paths./api/v1/expenses/{reference}/return.post.summary` | summary changed |
| `operation_extension_changed` | `paths./api/v1/expenses/{reference}/return.post.x-access` | vendor extension [x-access] changed |
| `response_description_changed` | `paths./api/v1/financial-periods/{periodId}/closing.get.responses.200.description` | response description changed |
| `response_description_changed` | `paths./api/v1/financial-periods/{periodId}/closing/check.post.responses.200.description` | response description changed |
| `response_description_changed` | `paths./api/v1/financial-periods/{periodId}/closing/close.get.responses.200.description` | response description changed |
| `response_description_changed` | `paths./api/v1/financial-periods/{periodId}/closing/close.post.responses.200.description` | response description changed |
| `response_description_changed` | `paths./api/v1/financial-periods/{periodId}/closing/history.get.responses.200.description` | response description changed |
| `response_schema_documentation` | `paths./api/v1/financial-periods/{periodId}/closing/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items.properties.display_status` | description changed |
| `request_schema_documentation` | `paths./api/v1/financial-periods/{periodId}/closing/tasks.post.requestBody.content.application/json.schema.properties.accountant_reference` | description changed |
| `response_schema_documentation` | `paths./api/v1/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/v1/financial-periods/{periodId}/closing/tasks.post.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_description_changed` | `paths./api/v1/financial-periods/{periodId}/closing/tasks.post.responses.200.description` | response description changed |
| `response_schema_documentation` | `paths./api/v1/general-ledger.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_documentation` | `paths./api/v1/general/countries.get.description` | description changed |
| `operation_documentation` | `paths./api/v1/general/countries.get.summary` | summary changed |
| `operation_documentation` | `paths./api/v1/identity/users/{userReference}.delete.summary` | summary changed |
| `operation_documentation` | `paths./api/v1/inventory/items.get.description` | description changed |
| `response_schema_documentation` | `paths./api/v1/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items` | title changed |
| `response_schema_reference_shape` | `paths./api/v1/inventory/items.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.items.items` | schema moved between $ref and inline definition (same effective shape) |
| `response_status_added` | `paths./api/v1/inventory/items.get.responses.422` | response [422] added to the contract |
| `operation_documentation` | `paths./api/v1/inventory/items.get.summary` | summary changed |
| `operation_tags_changed` | `paths./api/v1/inventory/items.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/inventory/items.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/inventory/movements.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/inventory/movements.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/inventory/movements.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/journal-entries.get.description` | description changed |
| `response_status_added` | `paths./api/v1/journal-entries.get.responses.422` | response [422] added to the contract |
| `response_schema_documentation` | `paths./api/v1/meetings/availability.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_documentation` | `paths./api/v1/meetings/{meetingReference}/join-link.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/meetings/{meetingReference}/join-link.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/meetings/{meetingReference}/join-link.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/meetings/{meetingReference}/join.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/meetings/{meetingReference}/join.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/meetings/{meetingReference}/join.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/meetings/{meetingReference}/provider/retry.post.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/meetings/{meetingReference}/provider/retry.post.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/meetings/{meetingReference}/provider/retry.post.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `response_description_changed` | `paths./api/v1/monthly-reports.post.responses.200.description` | response description changed |
| `operation_documentation` | `paths./api/v1/monthly-reports/{reportId}.get.description` | description changed |
| `response_description_changed` | `paths./api/v1/monthly-reports/{reportId}.get.responses.200.description` | response description changed |
| `operation_tags_changed` | `paths./api/v1/monthly-reports/{reportId}.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/monthly-reports/{reportId}.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `response_description_changed` | `paths./api/v1/monthly-reports/{reportId}/commentary.put.responses.200.description` | response description changed |
| `response_description_changed` | `paths./api/v1/monthly-reports/{reportId}/document.get.responses.200.description` | response description changed |
| `response_description_changed` | `paths./api/v1/monthly-reports/{reportId}/publish.post.responses.200.description` | response description changed |
| `response_description_changed` | `paths./api/v1/monthly-reports/{reportId}/ready.post.responses.200.description` | response description changed |
| `response_description_changed` | `paths./api/v1/monthly-reports/{reportId}/refresh-draft.post.responses.200.description` | response description changed |
| `response_description_changed` | `paths./api/v1/monthly-reports/{reportId}/versions.get.responses.200.description` | response description changed |
| `operation_documentation` | `paths./api/v1/onboarding/applications/send-code.post.summary` | summary changed |
| `response_schema_documentation` | `paths./api/v1/organizations/current.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `parameter_documentation` | `paths./api/v1/owner/reporting/financial.get.parameters.expense_category_id.description` | parameter description changed |
| `response_schema_documentation` | `paths./api/v1/owner/reporting/financial.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/v1/owner/reporting/financial.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/v1/owner/reporting/financial.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `response_schema_documentation` | `paths./api/v1/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/v1/payroll-runs/{runId}/export-payment-file.post.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `operation_documentation` | `paths./api/v1/payroll/employees.post.summary` | summary changed |
| `operation_documentation` | `paths./api/v1/payroll/employees/{publicReference}.patch.summary` | summary changed |
| `operation_documentation` | `paths./api/v1/platform/admin-roles.get.summary` | summary changed |
| `operation_documentation` | `paths./api/v1/platform/admin-roles/{roleReference}.get.summary` | summary changed |
| `parameter_documentation` | `paths./api/v1/platform/clients/registration-requests/{id}.get.parameters.id.description` | parameter description changed |
| `operation_documentation` | `paths./api/v1/platform/clients/registration-requests/{id}.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/v1/platform/clients/registration-requests/{id}/approve.post.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/v1/platform/clients/registration-requests/{id}/approve.post.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `operation_documentation` | `paths./api/v1/platform/clients/registration-requests/{id}/approve.post.summary` | summary changed |
| `request_schema_documentation` | `paths./api/v1/platform/clients/registration-requests/{id}/payment/verify.post.requestBody.content.application/json.schema` | title changed |
| `request_schema_documentation` | `paths./api/v1/platform/clients/registration-requests/{id}/payment/verify.post.requestBody.content.application/json.schema` | description changed |
| `request_schema_reference_shape` | `paths./api/v1/platform/clients/registration-requests/{id}/payment/verify.post.requestBody.content.application/json.schema` | schema moved between $ref and inline definition (same effective shape) |
| `operation_documentation` | `paths./api/v1/platform/clients/registration-requests/{id}/payment/verify.post.summary` | summary changed |
| `response_schema_documentation` | `paths./api/v1/platform/clients/registration-requests/{id}/reject.post.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/v1/platform/clients/registration-requests/{id}/reject.post.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `operation_documentation` | `paths./api/v1/platform/clients/registration-requests/{id}/reject.post.summary` | summary changed |
| `response_schema_documentation` | `paths./api/v1/platform/clients/registration-requests/{id}/request-info.post.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/v1/platform/clients/registration-requests/{id}/request-info.post.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/v1/platform/reports/accountant-assignments.get.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/v1/platform/reports/accountant-assignments.get.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/v1/platform/reports/accountant-workload.get.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/v1/platform/reports/accountant-workload.get.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/v1/platform/reports/clients.get.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/v1/platform/reports/clients.get.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/v1/platform/reports/renewals.get.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/v1/platform/reports/renewals.get.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/v1/platform/reports/subscriptions.get.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/v1/platform/reports/subscriptions.get.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/v1/platform/reports/suppliers.get.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/v1/platform/reports/suppliers.get.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `response_schema_documentation` | `paths./api/v1/platform/reports/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data` | title changed |
| `response_schema_reference_shape` | `paths./api/v1/platform/reports/tasks.get.responses.200.content.application/json.schema.allOf[1].properties.data` | schema moved between $ref and inline definition (same effective shape) |
| `operation_documentation` | `paths./api/v1/purchase-orders.get.description` | description changed |
| `parameter_schema_documentation` | `paths./api/v1/purchase-orders.get.parameters.status.schema` | title changed |
| `parameter_schema_documentation` | `paths./api/v1/purchase-orders.get.parameters.status.schema` | description changed |
| `operation_tags_changed` | `paths./api/v1/purchase-orders.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/purchase-orders.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/purchase-orders/{reference}.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/purchase-orders/{reference}.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/purchase-orders/{reference}.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/subscriptions/registration-request.get.description` | description changed |
| `operation_documentation` | `paths./api/v1/subscriptions/registration-request.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/v1/subscriptions/registration-status.post.responses.200.content.application/json.schema.allOf[1].properties.data.properties.payment_status` | description changed |
| `operation_documentation` | `paths./api/v1/subscriptions/registration.put.description` | description changed |
| `operation_documentation` | `paths./api/v1/subscriptions/registration/resubmit.post.description` | description changed |
| `request_schema_documentation` | `paths./api/v1/subscriptions/registration/resubmit.post.requestBody.content.application/json.schema` | title changed |
| `request_schema_documentation` | `paths./api/v1/subscriptions/registration/resubmit.post.requestBody.content.application/json.schema` | description changed |
| `request_schema_reference_shape` | `paths./api/v1/subscriptions/registration/resubmit.post.requestBody.content.application/json.schema` | schema moved between $ref and inline definition (same effective shape) |
| `response_status_added` | `paths./api/v1/subscriptions/registration/resubmit.post.responses.404` | response [404] added to the contract |
| `operation_documentation` | `paths./api/v1/subscriptions/registration/resubmit.post.summary` | summary changed |
| `operation_documentation` | `paths./api/v1/suppliers.get.description` | description changed |
| `response_schema_documentation` | `paths./api/v1/suppliers.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_tags_changed` | `paths./api/v1/suppliers.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/suppliers.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/suppliers/{id}.get.description` | description changed |
| `response_schema_documentation` | `paths./api/v1/suppliers/{id}.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `operation_tags_changed` | `paths./api/v1/suppliers/{id}.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/suppliers/{id}.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |
| `operation_documentation` | `paths./api/v1/users.get.summary` | summary changed |
| `response_schema_documentation` | `paths./api/v1/users/form-options.get.responses.200.content.application/json.schema.allOf[1].properties.data.properties.roles.items.properties.description` | description changed |
| `response_schema_documentation` | `paths./api/v1/waste/analytics.get.responses.200.content.application/json.schema.allOf[1].properties.data` | examples changed |
| `response_description_changed` | `paths./api/v1/waste/analytics.get.responses.200.description` | response description changed |
| `operation_extension_changed` | `paths./api/v1/waste/analytics.get.x-owner-read-model` | vendor extension [x-owner-read-model] changed |
| `operation_documentation` | `paths./api/v1/waste/records.get.description` | description changed |
| `operation_tags_changed` | `paths./api/v1/waste/records.get.tags` | tags changed |
| `operation_extension_changed` | `paths./api/v1/waste/records.get.x-canonical-replacement` | vendor extension [x-canonical-replacement] changed |

> **Fail closed:** unclassified changes require an explicit
> compatibility decision before this contract may be approved.

