# Capitalix — Backend API Requirements (Business Owner mobile app)

> Prepared by **Muath Sharawy** (Flutter) for the backend team — October 2026.
> The mobile app UI is finished and every screen already calls its service. Each endpoint below is an **empty path** in the app today (`lib/core/resources/api_constants.dart`) and answers with sample data. When you ship an endpoint, send me its path and I'll plug it in.
>
> Every key, enum value and response shape in this file is **exactly what the app parses today**. If you need a different name or shape, tell me before building so we agree once.

## Table of contents

0. [General contract (read first)](#0-general-contract-read-first)
1. [Auth & registration](#1-auth--registration)
2. [Subscription (plans & payment)](#2-subscription-plans--payment)
3. [Packages & modules](#3-packages--modules)
4. [Dashboard (home tab)](#4-dashboard-home-tab)
5. [Notifications & push](#5-notifications--push)
6. [Inventory](#6-inventory)
7. [Sales invoices, quotations & collections](#7-sales-invoices-quotations--collections)
8. [Purchases (POs & direct purchases)](#8-purchases-pos--direct-purchases)
9. [Suppliers & debts](#9-suppliers--debts)
10. [Expenses](#10-expenses)
11. [VAT](#11-vat)
12. [Zakat](#12-zakat)
13. [Financial statements & reports](#13-financial-statements--reports)
14. [Waste](#14-waste)
15. [Pricing (from the accountant)](#15-pricing-from-the-accountant)
16. [Meetings with the accountant](#16-meetings-with-the-accountant)
17. [Accountant reports & notes](#17-accountant-reports--notes)
18. [My account & subscription](#18-my-account--subscription)
19. [More tab summary](#19-more-tab-summary)
20. [Business settings](#20-business-settings)
21. [Branches](#21-branches)
22. [Users, roles & audit log](#22-users-roles--audit-log)
23. [App settings & account deletion](#23-app-settings--account-deletion)
24. [Customers](#24-customers)
25. [Items (products) & categories](#25-items-products--categories)
26. [Assets & depreciation](#26-assets--depreciation)
27. [Payroll & employees](#27-payroll--employees)
28. [Static pages](#28-static-pages)
29. [General lookups](#29-general-lookups)
30. [Endpoint checklist](#30-endpoint-checklist)

---

## 0. General contract (read first)

### 0.1 Base URL
The app reads the base URL once from Firebase Realtime Database:
`https://capitalix-5d68e-default-rtdb.firebaseio.com/base_url.json` → a plain string, e.g. `"https://api.capitalix.sa/api/v1"`.
All paths in this file are relative to it. **The paths in this file are suggestions** — keep them or send me yours.

### 0.2 Headers the app sends on every request
| Header | Value |
|---|---|
| `Authorization` | `Bearer <token>` (when signed in) |
| `Accept` | `application/json` |
| `Accept-Language` | `ar` or `en` — **every label / title / status text in a response must come in this language** |
| `DeviceId` | the FCM token of the device |

Null or empty query params / body fields are **not sent** — treat a missing field as "not provided".

### 0.3 Response envelope
Every success response is JSON with status `2xx`:
```json
{
  "message": "Saved successfully",
  "data": { }
}
```
- The app always reads `data`. For lists, `data` is an **object** that contains the list + its summary + `meta` (shapes per endpoint below).
- `message` is shown as a toast after actions — please send a short, translated message.

### 0.4 Errors
| Status | What the app does |
|---|---|
| `422` (or any 4xx) | Shows the first message from `errors` (e.g. `{"errors": {"phone": ["Phone is taken"]}}`), else `message`. |
| `401` | Clears the user and goes back to the start (token invalid / expired). |
| `403` | **Account disabled / banned**: signs out and shows `message` on the login screen. On the login request itself the `message` shows in the form. Use 403 only for this. |
| `5xx` / HTML | Generic "something went wrong". |

### 0.5 Pagination
Paginated lists take `page` (1-based) and return:
```json
"meta": { "current_page": 1, "last_page": 4, "total": 31 }
```
`total` = number of records matching the current filters.

### 0.6 Conventions
- IDs: strings or ints are both fine (the app reads everything as string).
- Money and quantities: numbers (`1290.5`), not formatted strings. Currency is SAR.
- Dates: `YYYY-MM-DD`; date-time: ISO 8601. Fields named `*_label` or `date` that are shown as-is (e.g. `"اليوم · 09:12"`) may be pre-formatted by you — they're marked "display text".
- Booleans: `true/false` (`1/0` also accepted).
- Files: uploads are `multipart/form-data`. File URLs in responses must be absolute.
- **Exports** (PDF / Excel) return `data: { "file_url": "https://…" }` — the app opens the URL.
- `period` query params for reports (shared `ReportPeriod`):

| Param | Values |
|---|---|
| `period_type` | `month` · `quarter` · `ytd` · `year` |
| `year` | e.g. `2026` |
| `period` | month `1–12` or quarter `1–4` (only for `month` / `quarter`) |

- `branch_id` empty / missing = all branches.
- **Field formats the app validates** (please validate the same on the server):

| Field | Rule |
|---|---|
| Saudi mobile (`phone`) | 9 digits, starts with `5`, no leading `0`, no country code (`phone_code` is separate, default `966`) |
| Commercial register | 10 digits |
| VAT number | 15 digits, starts and ends with `3` |
| IBAN | `SA` + 22 digits |
| Password | ≥ 8 chars, upper + lower case letter, a digit |
- **Permission flags (`can_*`)**: wherever a response has `can_edit`, `can_delete`, `can_approve`… the app shows the action only when it's `true`. **The backend is the judge** — still validate on the server.

---

## 1. Auth & registration

Flow (BRD): Register (3 steps) → OTP → plans → payment → request status (under review / needs completion / approved / rejected). Login goes straight in, then the app decides where the owner lands from the **user object**.

### 1.1 The user object (returned by login, verify, profile)
```json
{
  "id": "12",
  "name": "عبدالله الشمري",
  "email": "owner@mail.com",
  "phone": "512345678",
  "phone_code": "966",
  "image": "https://…/avatar.jpg",
  "locale": "ar",
  "token": "eyJ…",
  "business_name": "مطعم بيت الشاورما",
  "request_status": "under_review",
  "is_active": true,
  "is_notify": true,
  "is_verified": true,
  "is_blocked": false,
  "has_subscription": true,
  "is_subscription_expired": false,
  "unread_notification_count": 3,
  "modules": ["dashboard", "invoices", "expenses", "inventory"]
}
```
| Field | Used for |
|---|---|
| `is_blocked` | Checked first → signs out and shows the reason. |
| `is_verified` | `false` → OTP screen (`verifyAccount` flow, the app asks for the first code). |
| `has_subscription` | `false` → plans screen. |
| `request_status` | `under_review` · `needs_completion` · `approved` · `rejected` → request status screen until approved. |
| `is_active` | Account approved and active. |
| `is_subscription_expired` | `true` → renewal (plans). |
| `modules` | The package's modules — see [section 3](#3-packages--modules). |

### 1.2 Endpoints
| # | Name in app | Method | Suggested path | Body | Response `data` |
|---|---|---|---|---|---|
| 1 | `authLogin` | POST | `auth/login` | `phone, phone_code, password, device_token, type (android/ios)` | user object (with `token`) |
| 2 | `authRegister` | POST | `auth/register` | see 1.3 | user object (with `token`), `is_verified: false`, OTP sent to the phone |
| 3 | `authSendCode` | POST | `auth/send-code` | `phone, phone_code` | – (resend / first code for unverified login) |
| 4 | `authVerifyCode` | POST | `auth/verify` | `phone, phone_code, code, device_token, type` | user object, `is_verified: true` |
| 5 | `passwordForget` | POST | `auth/password/forget` | `phone, phone_code` | – (sends OTP; also used for resend) |
| 6 | `passwordVerifyCode` | POST | `auth/password/verify` | `phone, phone_code, code` | – |
| 7 | `passwordReset` | POST | `auth/password/reset` | `phone, phone_code, code, password, password_confirmation` | – |
| 8 | `authProfile` | GET | `auth/profile` | – | user object (token optional). Called on every app start to pick up ban / approval / expiry. |
| 9 | `authLogout` | POST | `auth/logout` | – | – (remove the device token) |
| 10 | `registrationRequest` | GET | `auth/registration-request` | – | see 1.4 |
| 11 | `registrationRequestUpdate` | POST | `auth/registration-request/update` | same as register **without password** | – (resubmit after "needs completion") |

Login with wrong credentials → 422 with message. Login of a banned account → 403 with the reason.

### 1.3 Register body
```json
{
  "name": "Owner name",
  "phone": "512345678",
  "phone_code": "966",
  "email": "owner@mail.com",
  "password": "********",
  "password_confirmation": "********",
  "business_name": "مطعم بيت الشاورما",
  "activity_type": "مطاعم ومقاهي",
  "commercial_register": "1010445872",
  "tax_number": "310445872900003",
  "city_id": "1",
  "address": "حي العليا، الرياض",
  "business_phone": "512458800",
  "business_email": "info@business.sa",
  "accept_terms": true,
  "device_token": "fcm…",
  "type": "android"
}
```
Password rules checked in the app: min 8 chars, upper + lower case, a number. Please validate the same on the server.

### 1.4 Registration request (status screen)
```json
{
  "id": "1",
  "number": "REQ-10245",
  "created_at": "2026-09-23",
  "status": "under_review",
  "payment_status": "under_review",
  "plan_name": "النمو",
  "amount": 861.35,
  "admin_notes": "Please upload a clear CR copy",
  "rejection_reason": "",
  "name": "…", "phone": "…", "phone_code": "966", "email": "…",
  "business_name": "…", "activity_type": "…",
  "commercial_register": "…", "tax_number": "…",
  "address": "…", "business_phone": "…", "business_email": "…",
  "city": { "id": "1", "name": "الرياض" }
}
```
- `status`: `under_review` · `needs_completion` · `approved` · `rejected`
- `payment_status`: `paid` · `under_review` · `unpaid`
- `admin_notes` shows on "needs completion"; the form is prefilled from this object and resubmitted with `registrationRequestUpdate`.

---

## 2. Subscription (plans & payment)

Agreed with backend: each plan has its own `price` and `duration` (set by the admin). The owner only picks a plan — **no duration picker**. The subscription starts on the account approval date and runs for the plan's duration.

| # | Name | Method | Suggested path | Params / body | Response `data` |
|---|---|---|---|---|---|
| 1 | `subscriptionPlans` | GET | `subscription/plans` | – | `{ plans: [plan] }` |
| 2 | `subscriptionPaymentInfo` | GET | `subscription/payment-info` | – | `{ vat_rate, bank_name, account_holder, account_number, iban }` |
| 3 | `subscriptionPay` | POST multipart | `subscription/pay` | see below | – (see note) |

Plan:
```json
{
  "id": "growth",
  "name": "النمو",
  "tag": "الأكثر اختياراً",
  "description": "مخزون وأتمتة مشتريات وتسعير وضريبة",
  "price": 749,
  "duration": { "id": "1", "name": "شهر", "months": 1 },
  "modules": ["كل الأساسية", "المخزون", "أتمتة المشتريات"],
  "features": ["…"],
  "limits": ["حتى 3 فروع", "حتى 10 مستخدمين"],
  "integrations": ["ZATCA", "Foodics", "رواء"]
}
```
(`modules` / `features` / `limits` / `integrations` here are **display texts**, not module keys. `tag` optional.)

Pay (multipart):
| Field | Notes |
|---|---|
| `plan_id` | required |
| `payment_method` | `online` · `bank_transfer` |
| `is_renewal` | `0/1` — renewal from my account / expired subscription |
| `is_plan_change` | `0/1` — renewal on another plan (upgrade / downgrade) |
| `sender_name` | transfer only |
| `transfer_proof` | file (image / PDF), transfer only |

**Online payment — needs agreement:** the gateway isn't chosen yet, so the app currently treats a successful `pay` as done. Tell me the gateway (URL to open in a webview with a success / fail redirect, or an SDK) and I'll wire it.

The price shown = plan price + VAT (`vat_rate`). A transfer puts the request / payment "under review" until the admin confirms.

---

## 3. Packages & modules

The owner's package decides which modules are open. Send the module keys in the user object: `modules: [key, …]`. **Empty / missing = everything open** (so please always send it once packages are live).

| Key | Module (BRD) |
|---|---|
| `dashboard` | لوحة المعلومات |
| `customers` | عملاء المنشأة |
| `suppliers` | الموردين والمديونيات |
| `products` | الأصناف |
| `inventory` | إدارة المخزون |
| `purchases` | أتمتة المشتريات |
| `pricing` | التسعير |
| `invoices` | الفواتير وعروض الأسعار |
| `expenses` | المصروفات |
| `vat` | ضريبة القيمة المضافة |
| `waste` | الهدر |
| `reports` | التقارير المالية / تقارير المحاسب / التقرير الشهري |
| `journal` | الدفاتر المحاسبية (الحسابات، القيود، الأستاذ، ميزان المراجعة) |
| `assets` | الأصول والإهلاك |
| `payroll` | مسير الرواتب |
| `zakat` | الوعاء الزكوي |
| `notifications` | مركز الإشعارات |
| `meetings` | الاجتماعات مع المحاسب |
| `business_settings` | إعدادات المنشأة |
| `integrations` | التكاملات (Foodics، رواء…) |
| `subscription` | إدارة الاشتراك |

Tabs, home components, quick actions, KPIs, More rows and notification targets are hidden / locked by these keys. **The server must also refuse requests to modules outside the package** (403 is reserved for banned accounts — please use another code, e.g. 422 with a message, for "not in your plan").

---

## 4. Dashboard (home tab)

| Name | Method | Suggested path | Params |
|---|---|---|---|
| `dashboard` | GET | `dashboard` | `period` = `month` · `quarter` · `year`, `branch_id` (empty = all) |

Response `data`:
```json
{
  "business_name": "مطعم بيت الشاورما",
  "period_label": "أغسطس 2026",
  "revenue": 486300,
  "expenses": 361400,
  "net_profit": 124900,
  "profit_change": 12.4,
  "chart": [ { "label": "أ1", "value": 38 } ],

  "inventory_value": 84620,
  "items_count": 24,
  "low_stock_count": 3,
  "supplier_debts": 38450,
  "due_supplier_invoices": 3,
  "net_vat": 21460,
  "output_vat": 57780,
  "input_vat": 36320,
  "purchases_total": 0,
  "waste_cost": 0,
  "orders_in_delivery": 0,

  "monthly_close": {
    "period_label": "يوليو 2026",
    "status": "has_notes",
    "note": "فرق مطابقة بنكية 420 ر.س",
    "target_id": "mr-2026-07"
  },

  "tasks": [
    { "id": "t1", "type": "low_stock", "title": "…", "subtitle": "…", "count": 3, "target_id": "" }
  ],

  "accountant_updated_at": "اليوم 09:12",
  "accountant_items": [
    { "id": "a1", "type": "pricing", "title": "…", "subtitle": "…", "target_id": "p1" }
  ],

  "recent_moves": [
    {
      "id": "m1", "type": "sale", "title": "فاتورة مبيعات · شركة الريادة",
      "party": "شركة الريادة", "reference": "INV-2026-0418", "date": "2026-08-23",
      "branch": "العليا", "payment_method": "تحويل بنكي", "status": "مسددة",
      "amount": 4830, "vat": 630
    }
  ],

  "subscription": { "plan_name": "باقة النمو", "end_date": "2026-09-30", "days_left": 35 },

  "branches": [ { "id": "b1", "name": "الفرع الرئيسي — العليا", "short_name": "العليا", "code": "BR-001", "city": "الرياض", "is_active": true, "operations_count": 1284 } ],

  "sections": ["branch", "profit", "kpis", "quick_actions", "pending_actions", "accountant", "recent_moves", "subscription"],
  "kpis": ["inventory_value", "low_stock", "supplier_debts", "net_vat"],
  "quick_actions": ["create_invoice", "direct_invoice", "review_purchase_order", "upload_expense", "pay_supplier", "stock_count", "waste_log", "approve_pricing", "accountant_meeting", "renew_subscription"]
}
```

Rules / enums:
- `profit_change` = net profit change vs previous period, in %.
- `chart` = performance bars for the period (any number of points, `label` is display text).
- `monthly_close.status`: `in_progress` · `closed` · `has_notes`. `target_id` = the monthly report id it opens. Omit `monthly_close` when the accountant hasn't sent it.
- `tasks[].type` (pending actions "إجراءات بانتظارك"): `low_stock` · `purchase_review` · `purchase_receive` · `pricing_approval` · `payroll` · `supplier_due` · `vat_due` · `report` · `meeting` · `subscription` · `other`. `target_id` = the exact record to open (PO / pricing / supplier / report / meeting id; for `payroll` = the period `2026-08`). Empty = opens the module list.
- `accountant_items[].type`: `pricing` · `report` · `note` (`target_id` = pricing id or report id).
- `recent_moves[].type`: `sale` · `expense` · `supplier_payment` · `purchase_receipt`. `status`, `payment_method`, `branch` are display texts.
- `subscription` omitted → card hidden. `days_left ≤ 7` shows the renewal warning.
- **Package-driven home**: `sections`, `kpis`, `quick_actions` are ordered key lists for the owner's package. Missing / empty = the app's defaults. Unknown keys are skipped.
  - `sections`: `branch` · `profit` · `kpis` · `quick_actions` · `pending_actions` · `accountant` · `recent_moves` · `subscription`
  - `kpis`: `inventory_value` · `low_stock` · `supplier_debts` · `net_vat` · `purchases` · `waste_cost`
  - `quick_actions`: `create_invoice` · `direct_invoice` · `review_purchase_order` · `upload_expense` · `pay_supplier` · `stock_count` · `waste_log` · `approve_pricing` · `accountant_meeting` · `renew_subscription`
- A period with no revenue, no expenses, no chart values and no moves shows a "no data" banner — just send zeros / empty lists.

---

## 5. Notifications & push

| # | Name | Method | Suggested path | Params / body | Response `data` |
|---|---|---|---|---|---|
| 1 | `notifications` | GET | `notifications` | `status` (`all`·`unread`·`read`), `period` (`all`·`today`·`7_days`·`30_days`), `kind` (optional), `page` | see below |
| 2 | `notificationDetails` | GET | `notifications/{id}` | – | notification object (the app then calls `read`) |
| 3 | `notificationsUnreadCount` | GET | `notifications/unread-count` | – | `{ unread_count }` |
| 4 | `notificationRead` | POST | `notifications/{id}/read` | – | – |
| 5 | `notificationUnread` | POST | `notifications/{id}/unread` | – | – |
| 6 | `notificationsReadAll` | POST | `notifications/read-all` | – | – |
| 7 | `notificationDelete` | DELETE | `notifications/{id}` | – | – |

List response:
```json
{
  "notifications": [ notification ],
  "meta": { "current_page": 1, "last_page": 2, "total": 15 },
  "total_count": 15,
  "unread_count": 9,
  "kind_counts": [ { "kind": "inventory", "count": 3 } ]
}
```
`total_count`, `unread_count`, `kind_counts` are for the **whole log**; the list and `meta.total` follow the filters.

Notification:
```json
{
  "id": "n4",
  "kind": "purchases",
  "title": "أمر شراء تلقائي PO-2026-041 يحتاج مراجعة",
  "body": "…",
  "source": "النظام",
  "branch_name": "الفرع الرئيسي",
  "business_name": "مطعم بيت الشاورما",
  "date": "اليوم · 07:55",
  "is_read": false,
  "action_label": "مراجعة أمر الشراء",
  "target": "purchase_order",
  "target_id": "po-41",
  "meeting_link": ""
}
```
- `kind`: `inventory` · `purchases` · `suppliers` · `finance` · `tax` · `reports` · `pricing` · `payroll` · `meetings` · `assets` · `system` · `general`
- `target` (where the action button goes) + `target_id` (record id; empty = the list):

| `target` | Opens | `target_id` |
|---|---|---|
| `subscription` | renewal (plans) | – |
| `invoices` | invoices tab | – |
| `invoice` / `quote` | invoice / quote details | invoice / quote id |
| `purchase_order` | PO details (or purchases tab) | PO id |
| `inventory` | item details (or inventory tab) — low / out of stock | item id |
| `supplier` | supplier details | supplier id |
| `vat_period` | VAT screen | – |
| `expense` | expense details (review result: approved / returned) | expense id |
| `zakat` | zakat calculation | zakat calc id |
| `journal` | journal entry details (accountant changed it after the owner's request) | entry id |
| `monthly_report` | monthly report | monthly report id |
| `pricing` | pricing details | pricing id |
| `meeting` | meeting details | meeting id |
| `report` | accountant report details | report id |
| `waste` | waste screen | – |
| `payroll` | payroll run | period `2026-08` |
| `business_settings` | business settings | – |
| `customer` | customer details | customer id |
| `asset` | asset details | asset id |

The action button shows only when `action_label` is not empty and `target` is in this table.
- `meeting_link`: a Google Meet link (`https://meet.google.com/…`) for meeting notifications → "Join meeting" button.

### 5.1 Push (FCM)
- The device token is sent as `device_token` + `type` on login / register / verify, and in the `DeviceId` header on every request.
- Android channel id: `capitalix_default` (please set `android.notification.channel_id` to it).
- Push payload `data`:
  - `notification_id` → the app opens that notification's details (loads `notifications/{id}` then marks it read). **Please always send it** for notifications stored in the center.
  - without it → the app opens the notifications center.
- Respect the owner's push settings ([section 23](#23-app-settings--account-deletion)) before sending.

---

## 6. Inventory

BRD "إدارة المخزون". Stock status rule: `qty ≤ 0` → `out`, `qty ≤ min_qty` → `low`, else `available`. You can send `status` or let the app compute it.

| # | Name | Method | Suggested path | Params / body | Response `data` |
|---|---|---|---|---|---|
| 1 | `inventoryItems` | GET | `inventory/items` | `search` (name / code), `status` (comma list of `available,low,out`), `category` (name), `page` | see 6.1 |
| 2 | `inventoryItemDetails` | GET | `inventory/items/{id}` | – | item + `usage` + `moves` (6.2) |
| 3 | `inventoryItemLimits` | POST | `inventory/items/{id}/limits` | `min_qty, target_qty` (target ≥ min) | – |
| 4 | `inventoryItemStock` | PUT | `inventory/items/{id}/stock` | `unit, qty, supplier_id, branch_id?, note?` | – (a different `qty` is recorded as an **adjustment move** with the note) |
| 5 | `inventoryFormOptions` | GET | `inventory/form-options` | – | 6.3 |
| 6 | `inventoryItemCreate` | POST | `inventory/items` | 6.4 | the created item. Duplicate → 422 with message |
| 7 | `inventorySync` | POST | `inventory/sync/{key}` | – (`key` = `foodics`, `rewaa`…) | `{ last_sync }` |
| 8 | `inventoryRecipes` | GET | `inventory/recipes` | `search` | `[ { id, name, category, sub_category, components_count } ]` |
| 9 | `inventoryRecipeDetails` | GET | `inventory/recipes/{id}` | – | 6.5 |
| 10 | `inventoryRecipeSave` | POST | `inventory/recipes/{id}` | `{ components: [ { item_id, quantity } ] }` — replaces all; empty list = unlink | – |

### 6.1 Items list
```json
{
  "summary": {
    "total_value": 84620, "available_value": 61200,
    "items_count": 24, "available_count": 19, "low_count": 3, "out_count": 2,
    "branch_label": "كل الفروع",
    "integrations": [ { "key": "foodics", "name": "Foodics", "last_sync": "2026-08-23 · 08:15 ص" } ]
  },
  "categories": ["المواد الغذائية", "المشروبات"],
  "items": [ item ],
  "meta": { "current_page": 1, "last_page": 2, "total": 10 }
}
```
`summary` is for the whole inventory; `items` / `meta` follow the filters. **One sync card per connected integration** (any integration the client adds) — no fixed list.

Item:
```json
{
  "id": "i1", "name": "لحم شاورما", "code": "RM-1001",
  "category": "المواد الغذائية", "sub_category": "اللحوم",
  "kind": "raw",
  "unit": "كجم", "qty": 18, "min_qty": 25, "target_qty": 80,
  "unit_cost": 42, "selling_price": null, "vat_rate": null,
  "supplier_id": "s1", "supplier_name": "مؤسسة اللحوم الطازجة",
  "branch_id": "b1", "branch_name": "الرئيسي — العليا",
  "last_sync": "2026-08-23 · 08:15 ص · Foodics",
  "status": "low"
}
```
- `kind`: `raw` (raw material — deducted through linked products) · `ready` (ready product — deducted from its own stock on sale).
- `unit_cost`, `selling_price`, `vat_rate` are **optional** — send `null` / omit when not set (stock value shows only when a cost exists; value = qty × unit_cost).

### 6.2 Item details
Item object + :
```json
"usage": [ { "product_name": "صحن شاورما", "quantity": 0.25 } ],
"moves": [ { "type": "وارد — استلام أمر شراء", "date": "2026-08-21", "quantity": 20, "reference": "PO-2026-041", "note": "استلام كامل" } ]
```
`moves.quantity` positive = in, negative = out. `type` is display text (sale, PO receipt, approved waste, adjustment…).

### 6.3 Form options
```json
{
  "items": [ { "id": "r3", "name": "عصير برتقال 250 مل", "category": "المشروبات", "sub_category": "المياه والعصائر", "selling_price": 5, "vat_rate": 15 } ],
  "categories": [ { "id": "c1", "name": "المواد الغذائية", "sub_categories": [ { "id": "c1-1", "name": "اللحوم" } ] } ],
  "units": ["كجم", "جرام", "لتر", "حبة", "عبوة"],
  "vat_rates": [15, 0],
  "suppliers": [ { "id": "s1", "name": "مؤسسة اللحوم الطازجة", "subtitle": "خالد العتيبي · 0551234417" } ],
  "branches": [ { "id": "b1", "name": "الرئيسي — العليا" } ]
}
```
- `items` = items **already registered in Items (الأصناف) without stock data** — business decision "no duplicates".
- `categories` come from the Items module (main › sub).
- The branch is asked only when there is more than one branch.

### 6.4 Create item body
Existing item (from `options.items`) — only stock data:
```json
{ "kind": "ready", "item_id": "r3", "unit": "عبوة", "opening_qty": 50, "min_qty": 20, "target_qty": 100, "unit_cost": 2.5, "supplier_id": "s2", "branch_id": "b1" }
```
New item — also registered in Items:
```json
{ "kind": "raw", "name": "زيت زيتون", "code": "RM-1100", "category_id": "c1", "sub_category_id": "c1-5", "selling_price": 0, "vat_rate": 15, "unit": "لتر", "opening_qty": 10, "min_qty": 5, "target_qty": 30, "unit_cost": 28, "supplier_id": "s1", "branch_id": "b1" }
```
Optional: `code` (generate one if missing), `selling_price`, `vat_rate`, `unit_cost`, `supplier_id`, `branch_id` (default = main branch). Rule: `target_qty ≥ min_qty`.

### 6.5 Recipe details (product ↔ raw materials)
```json
{
  "id": "p1", "name": "صحن شاورما", "category": "الوجبات", "sub_category": "الشاورما", "components_count": 4,
  "components": [ { "item_id": "i1", "item_name": "لحم شاورما", "unit": "كجم", "quantity": 0.25 } ],
  "items": [ { "id": "i1", "name": "لحم شاورما", "unit": "كجم", "code": "RM-1001" } ]
}
```
`quantity` = amount used in **one unit** of the product (> 0). `items` = items that can be added (raw materials only — not ready products). Integration sales deduct the components × sold quantity.

---

## 7. Sales invoices, quotations & collections

BRD "الفواتير". Invoice types: `tax` (B2B — customer VAT number required) · `simplified` (B2C / cash customer). Payment status: `unpaid` · `partial` · `paid` (paid only when nothing remains; the app can compute it from `total` / `paid` if `status` is missing).
A **quotation** creates no accounting entry, no customer debt, and is not sent to ZATCA until converted.

| # | Name | Method | Suggested path | Params / body | Response `data` |
|---|---|---|---|---|---|
| 1 | `invoices` | GET | `invoices` | `status` (`paid`·`partial`·`unpaid`, or comma list), `source=pos` (POS integration invoices only), `customer_id`, `all=1` (no paging), `page` | 7.1 |
| 2 | `invoiceDetails` | GET | `invoices/{id}` | – | invoice + `lines` + `payments` (7.2) |
| 3 | `invoiceFormOptions` | GET | `invoices/form-options` | – | 7.3 |
| 4 | `invoiceCreate` | POST | `invoices` | 7.4 | `{ id, number }` |
| 5 | `invoiceCollectionMethods` | GET | `invoices/collection-methods` | – | `[ { id, name } ]` |
| 6 | `invoiceCollectionScan` | POST multipart | `invoices/collection-scan` | `file` | 7.5 (OCR) |
| 7 | `invoiceCollect` | POST multipart | `invoices/collect` | 7.6 | – |
| 8 | `quotes` | GET | `quotes` | `page` | 7.7 |
| 9 | `quoteDetails` | GET | `quotes/{id}` | – | quote + `lines` |
| 10 | `quoteCreate` | POST | `quotes` | same as invoice body (no `type`) | `{ id, number, valid_until }` |
| 11 | `quoteConvert` | POST | `quotes/{id}/convert` | `{ type: "tax" \| "simplified" }` | `{ id, number }` of the new invoice |

The collection screen ("record collection" from the More / dashboard) calls `invoices?customer_id=…&status=unpaid,partial&all=1` → `data: { items: [invoice] }` (no paging).

### 7.1 Invoices list
```json
{
  "summary": { "sales_total": 21072.6, "output_vat": 2748.6, "count": 5 },
  "items": [ invoice ],
  "meta": { "current_page": 1, "last_page": 1, "total": 5 }
}
```
`summary` = all invoices; `items` / `meta` follow the filter.

### 7.2 Invoice
```json
{
  "id": "inv1051",
  "number": "INV-1051",
  "type": "tax",
  "status": "paid",
  "customer_id": "c5",
  "customer_name": "شركة الوفاق للتموين",
  "customer_vat_number": "310556677800003",
  "issuer_name": "مطعم بيت الشاورما",
  "issuer_vat_number": "300123456700003",
  "date": "2026-08-22",
  "due_date": "2026-09-06",
  "source": "عرض سعر QT-2026-013",
  "quote_number": "QT-2026-013",
  "is_pos": false,
  "branch_name": "الفرع الرئيسي — العليا",
  "subtotal": 4200, "vat": 630, "total": 4830, "paid": 4830,
  "notes": "…",
  "pdf_url": "https://…/INV-1051.pdf",
  "lines": [ { "name": "عصير طازج", "unit": "كوب", "quantity": 60, "price": 10, "total": 600 } ],
  "payments": [ { "amount": 4830, "date": "2026-08-23", "method": "تحويل بنكي", "reference": "TRX-458721", "proof_url": "https://…" } ]
}
```
- `source` = display text (يدوي / بيع مباشر / Foodics / رِواء / عرض سعر …). `is_pos` = came from a POS integration.
- `pdf_url` = the ZATCA-compliant invoice PDF (with QR).
- Remaining = `total − paid`; "Record collection" shows only while remaining > 0.

### 7.3 Form options
```json
{
  "vat_rate": 15,
  "issuer": { "name": "مطعم بيت الشاورما", "vat_number": "300123456700003", "is_complete": true, "missing": "" },
  "customers": [ { "id": "c1", "name": "شركة الريادة", "type": "business", "vat_number": "310122334400003", "phone": "0551234567", "national_address": "الرياض · حي العليا · 8228", "is_active": true } ],
  "products": [ { "id": "pr1", "name": "صحن شاورما", "unit": "صحن", "price": 24 } ],
  "branches": [ { "id": "b1", "name": "الفرع الرئيسي — العليا", "short_name": "العليا", "is_active": true } ],
  "payment_methods": [ { "id": "cash", "name": "نقداً" } ]
}
```
- `issuer.is_complete = false` blocks issuing; `missing` = text telling the owner what to complete in business settings (BRD: the business data must be complete before issuing).
- Send **all** customers incl. inactive (`is_active: false`) — the app only lets active ones be picked.
- `products` = active items only (inactive items can't be picked in new invoices) with the current selling price **before VAT**.
- Customer `type`: `business` · `individual`.

### 7.4 Create invoice body
```json
{
  "type": "tax",
  "is_direct": false,
  "customer_id": "c1",
  "branch_id": "b1",
  "date": "2026-10-12",
  "due_date": "2026-10-27",
  "payment_method_id": "cash",
  "notes": "…",
  "lines": [ { "product_id": "pr1", "quantity": 3, "price": 24 } ]
}
```
- `price` = unit price before VAT (editable in the form). Backend computes subtotal, VAT (`vat_rate`), total, number, PDF and ZATCA submission.
- **Direct invoice** (`is_direct: true`): simplified invoice paid on the spot — customer optional (cash customer), `payment_method_id` required, no `due_date`; save it as **paid** with one payment record.
- `tax` invoice requires a customer with a VAT number.

### 7.5 OCR scan (collection proof) — response
```json
{ "is_valid": true, "message": "", "amount": 4830, "date": "2026-08-23", "reference": "TRX-458721" }
```
`is_valid: false` + `message` → the app refuses the file. The app pre-fills amount / date / reference from the scan. **Same response is used for the supplier payment scan.**

### 7.6 Collect (multipart)
| Field | Notes |
|---|---|
| `invoice_id` | required |
| `amount` | > 0 and ≤ remaining |
| `date` | `YYYY-MM-DD` |
| `method_id` | from collection methods |
| `reference` | optional |
| `proof` | file — **required** (image / PDF) |

Backend updates paid / remaining / status and the customer debt, and records the entry.

### 7.7 Quotes list & quote
```json
{
  "summary": { "open_count": 1, "open_value": 6382.5, "count": 3 },
  "items": [ quote ],
  "meta": { "current_page": 1, "last_page": 1, "total": 3 }
}
```
Quote:
```json
{
  "id": "qt13", "number": "QT-2026-013",
  "customer_name": "شركة الوفاق للتموين", "customer_has_vat": true,
  "date": "2026-08-12", "valid_until": "2026-08-26",
  "status": "converted",
  "invoice_id": "inv1051", "invoice_number": "INV-1051",
  "subtotal": 4200, "vat": 630, "total": 4830,
  "notes": "", "pdf_url": "https://…",
  "lines": [ { "name": "…", "unit": "…", "quantity": 80, "price": 45, "total": 3600 } ]
}
```
`status`: `open` · `converted` · `expired` (set `expired` after `valid_until`). Only `open` can be converted.

---

## 8. Purchases (POs & direct purchases)

BRD "أتمتة المشتريات".

**Types** (`type`): `auto` (created by the system when an item reaches its minimum) · `manual` (any time) · `direct` (quick / direct purchase — no send / supplier-invoice cycle).

**Statuses** (`status`): `ready_for_review` · `sent` · `invoice_uploaded` · `in_delivery` · `received` · `completed` · `cancelled`
- PO cycle: `ready_for_review → sent → invoice_uploaded → in_delivery → received → completed`
- Direct purchase: created as **`in_delivery`** → `received` → `completed`
- `completed` = received **and** the supplier invoice is linked.

**Business rules (approved, Sept 2026 — please enforce on the server):**
1. A PO (auto / manual) uses **registered suppliers and inventory items only**. One-off suppliers and free (non-stock) lines are for direct purchases only.
2. PO unit price is **optional** ("when available"); a **direct purchase needs the unit price on every line**.
3. PO total = Σ (quantity × unit price) — **no 15% VAT line**; the actual VAT comes from the supplier invoice.
4. A line not linked to an inventory item is **non-stock** automatically. Only stock lines update the stock, and **only on receipt confirmation**.
5. Supplier invoice upload: the **invoice number is required** (used for the duplicate check — reject duplicates).
6. Auto POs: the backend creates them when an item hits its minimum — **one open auto PO per need**, suggested supplier = the item's supplier, quantity = target − balance.
7. Cancel only before the receipt, with a reason.
8. Edit / send only while `ready_for_review`. Sending needs the supplier's WhatsApp.

| # | Name | Method | Suggested path | Params / body | Response `data` |
|---|---|---|---|---|---|
| 1 | `purchaseOrders` | GET | `purchases` | `status`, `type`, `page` | 8.1 |
| 2 | `purchaseOrderDetails` | GET | `purchases/{id}` | – | 8.2 |
| 3 | `purchaseFormOptions` | GET | `purchases/form-options` | – | 8.3 |
| 4 | `purchaseOrderCreate` | POST (JSON, or multipart when a direct purchase has its invoice) | `purchases` | 8.4 | `{ id, number }` |
| 5 | `purchaseOrderUpdate` | PUT | `purchases/{id}` | same as create | `{ id, number }` |
| 6 | `purchaseOrderGenerate` | POST | `purchases/generate` | – | `{ items: [ { id, number } ] }` — runs the auto-PO automation now (returns the open ones if they already exist) |
| 7 | `purchaseOrderSend` | POST | `purchases/{id}/send` | – | – (backend sends the WhatsApp message with the PO number + a link for the supplier) → `sent`, set `sent_at` |
| 8 | `purchaseOrderInvoice` | POST multipart | `purchases/{id}/invoice` | `file`, `number` (required), `date` | – (owner uploads the supplier invoice on the supplier's behalf; record `source: owner` + the user) |
| 9 | `purchaseOrderDelivery` | POST | `purchases/{id}/delivery` | – | – → `in_delivery` |
| 10 | `purchaseOrderReceive` | POST | `purchases/{id}/receive` | `{ lines: [ { id, received_qty } ] }` | – → `received` (or `completed`); updates stock (stock lines only) and the supplier debt from the approved invoice |
| 11 | `purchaseOrderCancel` | POST | `purchases/{id}/cancel` | `{ reason }` | – → `cancelled` |

### 8.1 List
```json
{
  "summary": { "open_count": 6, "review_count": 2, "delivery_count": 1, "completed_count": 9 },
  "low_stock": [
    { "id": "i4", "name": "بطاطس مجمدة", "unit": "كجم", "supplier_name": "مؤسسة اللحوم الطازجة", "qty": 0, "min_qty": 20, "target_qty": 100, "open_order_number": "PO-2026-041" }
  ],
  "items": [ order ],
  "meta": { "current_page": 1, "last_page": 1, "total": 7 }
}
```
`summary` and `low_stock` are for everything; `items` / `meta` follow the filters. In the list an order may send `lines_count` + `total` instead of `lines`. `low_stock[].open_order_number` = the open auto PO already created for that item (empty = none).

### 8.2 Order (details)
```json
{
  "id": "po-41", "number": "PO-2026-041",
  "type": "auto", "status": "ready_for_review",
  "date": "2026-08-23", "expected_date": "2026-08-26", "received_date": "", "sent_at": "",
  "branch_id": "b1", "branch_name": "الرئيسي — العليا",
  "notes": "", "cancel_reason": "",
  "total": 3360,
  "supplier": {
    "id": "s1", "name": "مؤسسة اللحوم الطازجة", "phone": "0551234417", "whatsapp": "0551234417",
    "vat_number": "310445872900003", "contact": "خالد العتيبي",
    "is_registered": true, "has_account": true
  },
  "lines": [
    { "id": "l1", "item_id": "i1", "name": "لحم شاورما", "unit": "كجم", "is_stock": true, "quantity": 62, "unit_price": 42, "received_qty": null }
  ],
  "invoice": {
    "id": "SI-790", "number": "F-22018", "date": "2026-08-24",
    "file_url": "https://…", "file_name": "invoice.pdf",
    "source": "supplier", "uploaded_by": "…", "uploaded_at": "2026-08-24 · 10:12"
  }
}
```
- `unit_price: null` = no price yet. `received_qty: null` = not received yet.
- `supplier.is_registered: false` = one-off supplier of a direct purchase. `has_account` = the supplier has a portal account (can upload its own invoice).
- `invoice: null` when none. `invoice.source`: `supplier` · `owner`.
- `sent_at`, `uploaded_at` = display date-time.

### 8.3 Form options
```json
{
  "suppliers": [ { "id": "s1", "name": "…", "person": "خالد العتيبي", "whatsapp": "0551234417", "items": ["i1", "i4"] } ],
  "items": [ { "id": "i1", "name": "لحم شاورما", "code": "RM-1001", "unit": "كجم", "supplier_id": "s1", "qty": 18, "min_qty": 25, "target_qty": 80, "unit_cost": 42 } ],
  "branches": [ { "id": "b1", "name": "الرئيسي — العليا", "is_active": true } ]
}
```
Active registered suppliers only, with the item ids they supply. `unit_cost` = last cost (pre-fills the price).

### 8.4 Create / update body
```json
{
  "type": "direct",
  "supplier_id": "s1",
  "one_off_supplier": { "name": "محل الخضار", "phone": "0550000000", "vat_number": "", "contact": "" },
  "branch_id": "b1",
  "expected_date": "2026-10-15",
  "notes": "…",
  "lines": [
    { "id": "l1", "item_id": "i1", "name": "لحم شاورما", "is_stock": true, "quantity": 10, "unit_price": 42 },
    { "name": "أجرة نقل", "is_stock": false, "quantity": 1, "unit_price": 50 }
  ]
}
```
- Either `supplier_id` **or** `one_off_supplier` (direct only; kept with the operation, not added to the suppliers list).
- Line `id` only when editing an existing line. Free line = no `item_id`.
- Manual PO created as `ready_for_review`; direct purchase as `in_delivery`.
- Multipart variant (direct purchase with its invoice): same fields flattened (`lines[0][quantity]`…) + `invoice` (file), `invoice_number`, `invoice_date`.

---

## 9. Suppliers & debts

| # | Name | Method | Suggested path | Params / body | Response `data` |
|---|---|---|---|---|---|
| 1 | `suppliers` | GET | `suppliers` | `search` (name, contact person, linked item, mobile, CR / VAT, invoice number) | 9.1 |
| 2 | `supplierDetails` | GET | `suppliers/{id}` | – | supplier + `invoices` (9.2) |
| 3 | `supplierCreate` | POST | `suppliers` | 9.3 | `{ id, … }` |
| 4 | `supplierUpdate` | POST | `suppliers/{id}` | 9.3 | `{ id, … }` |
| 5 | `supplierToggleStatus` | POST | `suppliers/{id}/status` | `{ is_active: 0/1 }` | – (**refuse deactivating a supplier with debt**) |
| 6 | `supplierPaymentScan` | POST multipart | `suppliers/payment-scan` | `file` | same as 7.5 (OCR of the transfer proof) |
| 7 | `supplierPayInvoice` | POST multipart | `suppliers/pay` | `invoice_id, amount, date, reference, proof (file)` | – |
| – | linkable items | GET | `inventory/items?fields=id,name&all=1` | – | `{ items: [ { id, name } ] }` (re-uses the inventory list, no paging) |

Payment rule (BRD): payment is **per invoice** (no open payment on the supplier account), amount ≤ remaining, transfer proof required and checked by OCR first. Update the supplier debt, invoice paid / remaining, and post the entry.

### 9.1 List
```json
{
  "total_debt": 38450, "suppliers_count": 4, "due_invoices_count": 3,
  "suppliers": [ supplier ]
}
```
Totals are for all suppliers; the list follows `search`.

Supplier:
```json
{
  "id": "s1", "name": "مؤسسة اللحوم الطازجة", "person": "خالد العتيبي",
  "phone": "551234417", "whatsapp": "551234417",
  "commercial_register": "1010445872", "vat_number": "310445872900003",
  "is_active": true, "has_account": true,
  "items": [ { "id": "i1", "name": "لحم شاورما" } ],
  "purchase_orders_count": 3, "invoices_count": 1,
  "total_invoiced": 2604, "total_paid": 1200, "debt": 1404,
  "search_hit": "صنف مطابق: لحم شاورما"
}
```
`search_hit` (optional, display text) = why the search matched when it isn't the name.

### 9.2 Supplier invoices (details)
```json
"invoices": [
  {
    "id": "SI-771", "po_number": "PO-2026-041",
    "date": "2026-08-21", "due_date": "2026-09-05",
    "total": 2604, "paid": 1200, "uploaded_by": "المورد",
    "payments": [ { "amount": 1200, "date": "2026-08-22", "reference": "PAY-4201", "by": "صاحب المنشأة" } ]
  }
]
```
Status (unpaid / partial / paid) is computed by the app from `total` / `paid`.

### 9.3 Create / update body
```json
{ "name": "…", "phone": "551234417", "whatsapp": "551234417", "person": "…", "commercial_register": "…", "vat_number": "…", "item_ids": ["i1", "i4"], "is_active": 1 }
```
WhatsApp is required to send POs to the supplier.

---

## 10. Expenses

BRD "المصروفات". The list shows **every expense invoice** — the ones the owner uploads **and** the supplier invoices from the purchases cycle (never re-entered).

- `review_status`: `under_review` · `approved` · `returned` (accountant review cycle; a returned one is corrected and sent again).
- `operation_type` (the system classifies, the owner can correct): `tax_invoice` · `non_tax_invoice` · `transfer`. Only `tax_invoice` carries VAT.
- `payment_status` (input): `paid` · `deferred`.

| # | Name | Method | Suggested path | Params / body | Response `data` |
|---|---|---|---|---|---|
| 1 | `expenses` | GET | `expenses` | `review_status` (optional), `page` | 10.1 |
| 2 | `expenseDetails` | GET | `expenses/{id}` | – | expense |
| 3 | `expenseAnalysis` | GET | `expenses/analysis` | report period params (§0.6) **or** `period_type=all` (everything approved) | `{ total, categories: [ { id, name, amount } ] }` — approved expenses by category |
| 4 | `expenseFormOptions` | GET | `expenses/form-options` | – | `{ vat_rate, categories: [{id,name}], payment_methods: [{id,name}], branches: [branch] }` |
| 5 | `expenseScan` | POST multipart | `expenses/scan` | `file` | 10.2 (OCR) |
| 6 | `expenseCreate` | POST multipart | `expenses` | 10.3 | – (saved `under_review` for the accountant) |
| 7 | `expenseUpdate` | POST multipart | `expenses/{id}/resubmit` | 10.3 (file optional — the old one stays) | – (a returned expense corrected → back to `under_review`) |

Paying a supplier invoice from the expense details uses `supplierPayInvoice` (§9) with `invoice_id` = the expense `number`.

### 10.1 List
```json
{
  "summary": { "approved_total": 48620, "input_vat": 5980.4, "due_total": 7350, "under_review_count": 2 },
  "items": [ expense ],
  "meta": { "current_page": 1, "last_page": 1, "total": 6 }
}
```
Expense:
```json
{
  "id": "SI-771", "number": "SI-771",
  "date": "2026-08-21", "due_date": "2026-09-05",
  "vendor": "مؤسسة اللحوم الطازجة", "description": "…",
  "category_id": "purchases", "category": "مشتريات",
  "operation_type": "tax_invoice",
  "amount": 2264.35, "vat": 339.65, "total": 2604, "paid": 1000,
  "payment_method_id": "transfer", "payment_method": "حوالة بنكية",
  "branch_id": "b1", "branch": "الفرع الرئيسي — العليا",
  "po_number": "PO-2026-041",
  "uploaded_by": "المورد",
  "file_name": "si_SI-771.pdf", "file_url": "https://…",
  "review_status": "approved", "review_note": "",
  "from_purchase": true,
  "supplier_id": "s1", "supplier_name": "مؤسسة اللحوم الطازجة"
}
```
- `from_purchase: true` = supplier invoice from the purchases cycle (corrected from its PO, not here).
- `review_note` = the accountant's note (shown when returned).
- `supplier_id` set + remaining > 0 → "Pay supplier" button.

### 10.2 OCR scan response (any field may be empty)
```json
{ "number": "INV-10025", "date": "2026-08-09", "due_date": "2026-09-09", "vendor": "شركة النور للتوريدات", "description": "فاتورة كهرباء شهر يوليو", "po_number": "", "category_id": "utilities", "operation_type": "tax_invoice", "payment_method_id": "transfer", "amount": 1000, "vat": 150 }
```

### 10.3 Submit body (multipart)
| Field | Notes |
|---|---|
| `file` | invoice image / PDF (required on create) |
| `number`, `date`, `vendor`, `description` | required |
| `due_date` | optional |
| `category_id` | from form options |
| `operation_type` | `tax_invoice` · `non_tax_invoice` · `transfer` |
| `amount`, `vat`, `total` | `total = amount + vat` |
| `payment_status` | `paid` · `deferred` |
| `payment_method_id` | when paid |
| `branch_id`, `po_number` | optional |

---

## 11. VAT

BRD "ضريبة القيمة المضافة". Net VAT = output VAT (sales) − recoverable input VAT (purchases + expenses). Positive = due to ZATCA, negative = refundable.

| # | Name | Method | Suggested path | Params / body | Response `data` |
|---|---|---|---|---|---|
| 1 | `vatSummary` | GET | `vat/summary` | `type` (`monthly`·`quarterly`), `year`, `period` (1–12 or 1–4) | 11.1 |
| 2 | `vatExport` | GET | `vat/export` | `type, year, period`, `kind` (`return`·`invoices`), `format` (`pdf`·`excel`) | `{ file_url }` |
| 3 | `vatInvoiceUpload` | POST multipart | `vat/invoices` | same body as expense create (10.3) | – — "رفع فاتورة ضريبية": a tax invoice added to **its VAT period, taken from the invoice date** |

- `kind=return` → the return data of the period (PDF or Excel) matching the summary shown (not a ZATCA submission).
- `kind=invoices` → all taxable invoices of the period **with their attachments in one PDF** (`format=pdf`).

### 11.1 Summary
```json
{
  "output_vat": 945, "input_vat": 1270.43,
  "sources": [ { "type": "sales", "count": 2, "vat": 945 }, { "type": "purchase", "count": 2, "vat": 547.82 }, { "type": "expense", "count": 1, "vat": 722.61 } ],
  "documents": [
    { "id": "INV-1051", "type": "sales", "date": "2026-08-22", "party": "شركة الوفاق للتموين", "status": "مدفوعة", "source": "موديول الفواتير · يدوي", "file": "sales_INV-1051.pdf", "file_url": "https://…", "total": 4830, "vat": 630, "amount": 4200 }
  ],
  "years": ["2026", "2025"]
}
```
- `type`: `sales` (output) · `purchase` · `expense` (input). Each document appears once.
- `years` = years that have data (year picker).
- `status`, `source` are display texts. `amount` optional (= total − vat).

---

## 12. Zakat

BRD "الوعاء الزكوي". Vessel = base + additions − deductions; zakat = vessel × rate (0 when vessel ≤ 0). **The rate is fixed per year / period (2.5% Hijri or 2.578% Gregorian) and comes from the backend — never picked in the app.**
Status: `draft` → `ready_for_review` → `approved` (locked; one record per period).

| # | Name | Method | Suggested path | Params / body | Response `data` |
|---|---|---|---|---|---|
| 1 | `zakat` | GET | `zakat` | `period` (optional; empty = current) | 12.1 |
| 2 | `zakatSubmit` | POST | `zakat/submit` | 12.2 | – → `ready_for_review` |
| 3 | `zakatApprove` | POST | `zakat/approve` | 12.2 | – → `approved` (save approved_at / by) |
| 4 | `zakatHistory` | GET | `zakat/history` | – | `[ { period, period_label, vessel, zakat, status, created_at, approved_at, approved_by } ]` (data is a list) |

### 12.1 Calculation
```json
{
  "periods": [ { "id": "2026", "label": "السنة المالية 2026" }, { "id": "2025", "label": "السنة المالية 2025" } ],
  "calculation": {
    "period": "2026", "period_label": "السنة المالية 2026",
    "status": "draft", "rate": 2.578, "note": "",
    "created_at": "2026-08-23", "approved_at": "", "approved_by": "",
    "base": [ { "id": "equity", "label": "حقوق الملكية", "amount": 980000, "source": "القوائم المالية — الميزانية", "manual_amount": null, "editable": true } ],
    "additions": [ { "id": "add_other", "label": "إضافات أخرى", "amount": 0, "source": "", "manual_amount": null, "editable": true } ],
    "deductions": [ { "id": "fa", "label": "صافي الأصول الثابتة", "amount": 348100, "source": "الأصول والإهلاك", "manual_amount": null, "editable": true } ]
  }
}
```
- `amount` = value pulled from the system, `source` = where from (empty = manual-only item).
- `manual_amount` = the owner's override (`null` = none) — the app uses it instead of `amount` and marks it "manual".
- `editable` = the owner may enter / correct this value before approval.

### 12.2 Submit / approve body
```json
{ "period": "2026", "note": "…", "manual": [ { "id": "add_other", "amount": 15000 } ] }
```
Save the manual values and the note, then move the status.

---

## 13. Financial statements & reports

BRD "القوائم المالية والتقارير" (More › القوائم والتقارير المالية). **All figures come from approved entries only.**
Every report endpoint takes the report period params (§0.6: `period_type`, `year`, `period`) + `branch_id` (absent = all branches the user may see), and every response adds `branches: [branch]` (for the branch picker).
The accounting books (accounts, journal, ledger, trial balance) belong to module `journal`.

| # | Name | Method | Suggested path | Extra params / body | Response `data` |
|---|---|---|---|---|---|
| 1 | `statementsSummary` | GET | `statements/summary` | – | `{ revenue, expenses, accounts_count, journals_count, monthly_report_label, branches }` (hub; net = revenue − expenses) |
| 2 | `accounts` | GET | `statements/accounts` | – | `{ accounts: [account], branches }` |
| 3 | `journalEntries` | GET | `statements/journal` | `status` (optional) | `{ entries: [entry], branches }` |
| 4 | `journalEntryDetails` | GET | `statements/journal/{id}` | – | entry (with `lines` + `log`) |
| 5 | `journalEntryRequest` | POST | `statements/journal/{id}/request` | `{ kind: "edit" \| "cancel", reason }` | – (owner asks the accountant; log it on the entry and notify the accountant) |
| 6 | `ledger` | GET | `statements/ledger` | `account` (account code; empty = first account) | 13.3 |
| 7 | `trialBalance` | GET | `statements/trial-balance` | – | `{ rows: [ { code, name, debit, credit } ], branches }` |
| 8 | `financialStatement` | GET | `statements/statement` | `kind` = `income` · `balance` · `cash_flow` | **StatementModel** (13.4) + `branches` |
| 9 | `profitReport` | GET | `statements/profit` | `revenue_category_id`, `revenue_type_id`, `expense_category_id`, `expense_type_id` (all optional) | 13.5 |
| 10 | `monthlyReport` | GET | `statements/monthly-report` | `id` (e.g. `2026-07`; empty = latest issued) | 13.6 |
| 11 | `monthlyReportCustomize` | POST | `statements/monthly-report/{id}/customize` | `{ hidden: [table key], extras: [extra key] }` | – (view / export only; data unchanged) |
| 12 | `statementsExport` | GET | `statements/export` | `report`, `format` (`pdf`·`excel`), period + `branch_id`, the report's own params (`kind`, `account`, `id`, profit filters…), `split_months` (profit report: one column per month) | `{ file_url }` |
| 13 | `statementsExportBundle` | POST | `statements/export-bundle` | `{ period_type, year, period, branch_id, format, reports: [key] }` | `{ file_url }` — one file with the picked statements, with business name, VAT number, period and branch on it |

`report` keys (export): `income` · `balance` · `cash_flow` · `trial` · `ledger` · `journal` · `profit` · `monthly`
`reports` keys (bundle): `income` · `balance` · `cash_flow` · `trial` · `ledger` · `journal` · `profit` · `vat` · `waste` · `recon`

**Owner rules (agreed):** the owner **views only** — no approval of entries. From an entry they can "ask the accountant to edit / cancel" (logged on the entry). Report periods: month, quarter, YTD, full fiscal year. Exports: PDF or Excel from each screen + the bundle.

### 13.1 Account
```json
{ "id": "1110", "code": "1110", "name": "الصندوق", "type": "assets", "parent_name": "الأصول المتداولة", "is_active": true }
```
`type`: `assets` · `liabilities` · `equity` · `revenue` · `expenses`.

### 13.2 Journal entry
```json
{
  "id": "JE-2026-0412", "date": "2026-08-22",
  "operation_type": "فاتورة مبيعات", "reference": "INV-1051",
  "ref_type": "invoice", "ref_id": "inv1051",
  "description": "فاتورة مبيعات — شركة الوفاق للتموين",
  "source": "موديول الفواتير",
  "status": "approved",
  "created_at": "2026-08-22 11:05", "updated_at": "",
  "lines": [ { "account_code": "1130", "account_name": "العملاء", "debit": 4830, "credit": 0 } ],
  "log": [ "طلب تعديل أُرسل إلى المحاسب — … · بانتظار تنفيذ المحاسب" ]
}
```
- `status`: `under_review` · `approved` · `modified` · `cancelled`.
- `ref_type` + `ref_id` open the original operation: `invoice` · `expense` · `supplier` / `supplier_payment` (id = supplier id) · `purchase_order` · `journal` · `payroll` (id = period `2026-08`) · `asset` · `assets` (the list). Other values (e.g. `integration`) only show `source`.
- `log` = change log lines (display text).

### 13.3 Ledger
```json
{
  "accounts": [ account ],
  "account": account,
  "balance": 18450,
  "rows": [ { "journal_id": "JE-2026-0412", "date": "2026-08-22", "reference": "INV-1051", "description": "…", "debit": 4830, "credit": 0, "balance": 18450 } ],
  "branches": [ ]
}
```
Running balance per row; positive = debit, negative = credit.

### 13.4 StatementModel (income / balance / cash flow / monthly report)
The backend builds the statement; the app only renders it — so grouping and figures stay on your side.
```json
{
  "id": "income-2026-08",
  "hero": {
    "label": "صافي الربح", "amount": 124900, "value": "", "note": "+9.4% عن الشهر السابق",
    "chips": [ { "label": "الإيرادات", "amount": 468300 }, { "label": "المصروفات", "amount": 343400 } ]
  },
  "sections": [
    {
      "key": "revenue", "title": "الإيرادات", "subtitle": "", "total": 468300, "note": "",
      "items": [ { "label": "إجمالي الإيرادات", "amount": 468300, "tone": "success" }, { "label": "أوامر شراء مكتملة", "value": "11 من 14" } ],
      "rows":  [ { "title": "INV-1051 · …", "subtitle": "…", "amount": 4830, "tone": "", "tag": "", "tag_tone": "", "target": { "type": "invoice", "id": "inv1051" } } ],
      "bars":  [ { "label": "حليب طازج", "amount": 215.5, "percent": 4.1 } ]
    }
  ]
}
```
- A figure has `amount` (number, shown as money) **or** `value` (display text).
- `tone`: `success` · `danger` · `warning` · `info` · empty (neutral).
- Any of `items` / `rows` / `bars` / `note` may be empty. `target` (optional) uses the same types as `ref_type` above.

### 13.5 Profit & expenses report
```json
{
  "totals": { "revenue": 468300, "expenses": 343400 },
  "months": [
    {
      "label": "أغسطس 2026",
      "revenue": [ { "label": "مبيعات الوجبات", "amount": 320000 } ],
      "expense_groups": [ { "name": "مشتريات", "subs": [ { "label": "لحوم", "amount": 52000 } ] } ]
    }
  ],
  "matrix": {
    "months": ["يونيو", "يوليو", "أغسطس"],
    "rows": [ { "label": "مشتريات", "is_group": true, "cells": [50000, 52000, 54000] }, { "label": "لحوم", "is_group": false, "cells": [20000, 21000, 22000] } ]
  },
  "compare": [ { "label": "الإيرادات", "previous": 428000, "current": 468300, "lower_is_better": false } ],
  "filters": {
    "revenue_categories": [ { "id": "1", "name": "…" } ], "revenue_types": [ ],
    "expense_categories": [ ], "expense_types": [ ]
  },
  "branches": [ ]
}
```
One revenue table + one expense table per month (category → sub-types; a category total = sum of its sub-types), the monthly expenses matrix, and the comparison with the previous period. Filter options come with the response.

### 13.6 Monthly report (prepared, reviewed and sent by the accountant)
StatementModel (`hero` + `sections`, each section has its table `key`) + :
```json
{
  "id": "2026-07", "period_label": "يوليو 2026",
  "accountant": "أ. سامي الحربي", "issued_at": "2026-08-05",
  "file_url": "https://…/2026-07.pdf",
  "months": [ { "id": "2026-07", "name": "يوليو 2026" }, { "id": "2026-06", "name": "يونيو 2026" } ],
  "tables": [ { "key": "revenue", "label": "الإيرادات والمصروفات", "subtitle": "…", "on": true } ],
  "extras": [ { "key": "cash", "label": "ملخص التدفق النقدي", "subtitle": "…", "on": false } ]
}
```
- `months` = issued reports (month picker).
- `tables` = the report tables (`on` = shown); `extras` = optional reports (`on` = added). Saved per owner with `monthlyReportCustomize`; `sections` must respect them (hidden tables removed, added extras included).
- Table keys used in the design: `revenue`, `purchases`, `waste`, `recon`, `tax`, `notes`; extras: `cash`, `branches`, `aging`.

---

## 14. Waste

Read-only for the owner (recorded by the accountant).

| Name | Method | Suggested path | Params | Response `data` |
|---|---|---|---|---|
| `waste` | GET | `waste` | `period` = `month` · `quarter` · `year` (same as the dashboard), `branch_id` (empty = all) | 14.1 |

### 14.1 Response
```json
{
  "period_label": "أغسطس 2026",
  "total_cost": 128.6, "previous_cost": 144,
  "total_qty": 35.5, "previous_qty": 38.3, "percent": 10.4,
  "records": [
    {
      "id": "w1", "item": "لحم بقري مفروم", "unit": "كجم",
      "system_qty": 10, "actual_qty": 8.5, "waste_qty": 1.5,
      "unit_cost": 30, "total_cost": 45, "percent": 15,
      "reason": "فرق جرد", "notes": "", "date": "2026-08-24", "branch": "العليا"
    }
  ],
  "branches": [ branch ]
}
```
Formulas (computed by you): waste qty = system qty − actual qty; cost = waste qty × unit cost; % = waste qty ÷ system qty × 100. `total_qty` / `percent` (overall Σ waste ÷ Σ system qty) are optional — the app computes them from `records` if missing. The app groups cost by `reason` itself.

---

## 15. Pricing (from the accountant)

BRD "التسعير وحساب التكلفة". The accountant sends a product pricing; the owner approves the suggested price or sets a different final price (applies to **new operations only**).
`status`: `pending` · `approved` (final = suggested) · `modified` (owner set another price).

| # | Name | Method | Suggested path | Params / body | Response `data` |
|---|---|---|---|---|---|
| 1 | `pricing` | GET | `pricing` | `status` = `pending` · `done` (approved + modified) · missing = all | `[ pricing ]` (data is a list; summary fields enough) |
| 2 | `pricingDetails` | GET | `pricing/{id}` | – | pricing with the breakdown |
| 3 | `pricingApprove` | POST | `pricing/{id}/approve` | `{ final_price }` | – (status `approved` if equal to suggested, else `modified`; set `approved_at`; update the item's selling price) |

Pricing:
```json
{
  "id": "p1", "product": "صحن شاورما", "accountant": "أ. سامي الحربي",
  "date": "2026-08-24", "approved_at": "", "status": "pending",
  "materials_cost": 14.6, "operating_cost": 1.52, "total_cost": 16.12,
  "current_price": 24, "suggested_price": 26, "final_price": 0,
  "waste_percent": 4.2, "waste_note": "هدر اللحم 1.5 كجم هذا الشهر (للاطلاع — لا يدخل في التكلفة)",
  "materials": [ { "name": "لحم شاورما", "quantity": 0.25, "unit": "كجم", "supplier": "مؤسسة اللحوم الطازجة", "unit_price": 42, "cost": 10.5 } ],
  "operating_items": [ { "name": "الإيجار", "per_unit": 0.38 } ]
}
```
The app computes profit = price − total cost and margin = profit ÷ price × 100 for the current / suggested / final price.

---

## 16. Meetings with the accountant

Agreed (design over BRD): the owner **books**, and can also **edit** (move to another offered slot) or **cancel** an upcoming meeting. The backend notifies the accountant on book / edit / cancel. Meeting links are Google Meet.
`status`: `upcoming` · `completed` · `cancelled`.

| # | Name | Method | Suggested path | Params / body | Response `data` |
|---|---|---|---|---|---|
| 1 | `meetings` | GET | `meetings` | `type` = `upcoming` · `past` | `[ meeting ]` (data is a list) |
| 2 | `meetingDetails` | GET | `meetings/{id}` | – | meeting |
| 3 | `meetingSlots` | GET | `meetings/slots` | – | `{ accountant, days: [ { date, label, times: ["10:00", "11:30"] } ] }` — free slots of the business's accountant |
| 4 | `meetingBook` | POST | `meetings` | `{ date, time, subject?, notes? }` | `{ id }` (create the Google Meet link) |
| 5 | `meetingUpdate` | PUT | `meetings/{id}` | `{ date, time, subject, notes }` | `{ id }` |
| 6 | `meetingCancel` | POST | `meetings/{id}/cancel` | – | – |

Meeting:
```json
{
  "id": "mt1", "subject": "مراجعة إقفال شهر أغسطس", "notes": "…",
  "date": "2026-09-28", "time": "11:00",
  "accountant": "أ. سامي الحربي", "status": "upcoming",
  "meet_link": "https://meet.google.com/abc-defg-hij",
  "created_at": "2026-09-20", "updated_at": "2026-09-22",
  "can_edit": true, "can_cancel": true
}
```
`can_edit` / `can_cancel` missing = allowed while `upcoming`. "Join" shows for an upcoming meeting with a valid link.

---

## 17. Accountant reports & notes

BRD: the latest financial reports and notes sent by the accountant (dashboard "من المحاسب" card → "عرض الكل", and a row in the statements hub).
`type`: `report` · `note`.

| # | Name | Method | Suggested path | Params | Response `data` |
|---|---|---|---|---|---|
| 1 | `reports` | GET | `accountant-reports` | `type` (optional) | `[ report ]` (data is a list) |
| 2 | `reportDetails` | GET | `accountant-reports/{id}` | – | report with `figures` + `notes` |

```json
{
  "id": "r1", "type": "report",
  "title": "التقرير المالي لشهر يوليو", "period": "يوليو 2026",
  "issued_at": "2026-08-05", "accountant": "أ. سامي الحربي",
  "summary": "صافي ربح 124,900 ر.س",
  "file_url": "https://…/2026-07.pdf",
  "figures": [ { "label": "صافي الربح", "amount": 124900 }, { "label": "هامش صافي الربح", "value": "26.5%" } ],
  "notes": [ "ارتفاع تكلفة اللحوم 6% …" ]
}
```

---

## 18. My account & subscription

More › "حسابي والاشتراك". Rules (BRD, agreed):
- Name / email save directly. A **changed mobile is saved only after the OTP sent to the new number** is confirmed.
- Password change: current password + new + confirmation → OTP to the **registered** mobile → change. New password must differ from the current one.
- Renew and change plan both go through the payment endpoint (§2) with `is_renewal` / `is_plan_change`.
- The full payments log is kept — nothing is deleted.

| # | Name | Method | Suggested path | Body | Response `data` |
|---|---|---|---|---|---|
| 1 | `account` | GET | `account` | – | `{ profile, subscription }` (18.1) |
| 2 | `subscriptionDetails` | GET | `account/subscription` | – | `{ subscription, payments: [payment] }` |
| 3 | `accountUpdate` | POST | `account/update` | `{ name, email, phone, phone_code }` | updated user (optional). **If the phone changed**: keep the old number and send an OTP to the new one |
| 4 | `accountPhoneSendCode` | POST | `account/phone/send-code` | `{ phone, phone_code }` | – (resend to the new number) |
| 5 | `accountPhoneVerify` | POST | `account/phone/verify` | `{ phone, phone_code, code }` | – (now save the new number) |
| 6 | `accountPasswordSendCode` | POST | `account/password/send-code` | `{ current_password, password, password_confirmation }` (+ `phone, phone_code` on resend) | – (check the current password, send OTP to the registered mobile) |
| 7 | `accountPasswordChange` | POST | `account/password/change` | `{ phone, phone_code, code, current_password, password, password_confirmation }` | – (apply) |

### 18.1 Account
```json
{
  "profile": { "name": "عبدالله الشمري", "email": "…", "phone": "551234417", "phone_code": "966", "password_changed_at": "منذ 3 أشهر" },
  "subscription": {
    "plan_id": "growth", "plan_name": "النمو", "duration": "شهر",
    "start_date": "2026-09-04", "end_date": "2026-10-04", "days_left": 5, "is_expired": false,
    "price": 749, "vat": 112.35, "total": 861.35,
    "payment_method": "الدفع الإلكتروني", "payment_status": "success",
    "transaction_date": "2026-09-04 · 10:12", "reference": "TRX-90412",
    "usage": [ { "label": "الفروع", "used": 3, "limit": 5 }, { "label": "المستخدمون", "used": 4, "limit": 10 } ]
  }
}
```
- `password_changed_at` = display text. `usage.limit` 0 = unlimited.
- `payment_status` / payment `status`: `success` · `pending` (transfer under review) · `failed` · `rejected`.

Payment record:
```json
{ "id": "pm1", "title": "تجديد — باقة النمو", "duration": "شهر", "date": "2026-09-04 · 10:12", "method": "الدفع الإلكتروني", "amount": 861.35, "status": "success", "reference": "TRX-90412" }
```

---

## 19. More tab summary

One call gives the live subtitle (and an optional red badge) of each More row. Answer in the app language. If it fails, the app shows fixed subtitles.

| Name | Method | Suggested path | Response `data` |
|---|---|---|---|
| `moreSummary` | GET | `more/summary` | `{ <row key>: { subtitle, badge? } }` |

```json
{
  "suppliers": { "subtitle": "4 موردين · 3 فواتير مستحقة" },
  "pricing": { "subtitle": "2 بانتظار الاعتماد", "badge": 2 },
  "account": { "subtitle": "باقة النمو · حتى 2026-12-31" }
}
```
Row keys: `suppliers` · `expenses` · `vat` · `zakat` · `reports` · `pricing` · `waste` · `purchases` · `products` · `customers` · `payroll` · `assets` · `meetings` · `business_settings` · `app_settings` · `branches` · `users` · `account`. Send only rows in the package.

---

## 20. Business settings

More › "إعدادات المنشأة". Form rules (BRD): name + activity required; CR / VAT checked when entered; email + mobile required; landline, contact person, city, address, logo optional. **CR, VAT number and business status are editable only with `permissions.can_edit_sensitive`** — the app doesn't send them otherwise. Kept from the design (agreed): integrations card (read-only), edits log, and the owner can switch the business status (`active` / `suspended` = temporarily suspended).

| # | Name | Method | Suggested path | Body | Response `data` |
|---|---|---|---|---|---|
| 1 | `businessSettings` | GET | `business` | – | 20.1 |
| 2 | `businessSettingsUpdate` | POST multipart | `business/update` | 20.2 | same as GET (the updated settings); add a log entry |

### 20.1 Response
```json
{
  "business": {
    "id": "1", "name": "مطعم بيت الشاورما", "activity_type": "مطاعم ومقاهي",
    "commercial_register": "1010774521", "tax_number": "310774521900003",
    "email": "info@…", "phone": "551234417", "phone_code": "966", "landline": "0112458800",
    "contact_name": "عبدالله الشمري", "contact_role": "صاحب المنشأة",
    "city": { "id": "1", "name": "الرياض" }, "address": "…",
    "logo": "https://…/logo.png", "status": "active"
  },
  "summary": { "branches_count": 4, "active_branches_count": 3, "plan_name": "باقة النمو", "plan_duration": "شهري", "is_subscription_active": true, "subscription_days_left": 34 },
  "integrations": [ { "id": "foodics", "name": "Foodics", "description": "المنتجات والمبيعات · آخر مزامنة 08:15", "status": "connected" } ],
  "log": [ { "title": "تحديث رقم جوال التواصل", "by": "صاحب المنشأة", "at": "2026-08-11 · 09:24" } ],
  "permissions": { "can_edit": true, "can_edit_sensitive": true }
}
```
Integration `status`: `connected` · `pending` · anything else = disconnected. Integrations are managed by the platform (read-only here).

### 20.2 Update (multipart)
`name, activity_type, email, phone, phone_code, landline, contact_name, city_id, address` + (only with `can_edit_sensitive`) `commercial_register, tax_number, status` + `logo` (file, optional) or `remove_logo=1`.

---

## 21. Branches

More › "إدارة الفروع". Rules (agreed):
1. Only the **name** is required; name and code are **unique in the business**; city, address, contact number, email, manager optional (format checked when entered). Generate a code when missing.
2. The owner can set another **active** branch as main. The main branch can't be deactivated or deleted.
3. Delete only with **no linked operations** (`operations_count == 0`); otherwise deactivate. Inactive branches stay for history but can't be picked for new data.
4. Actions show only with `permissions.can_manage`.

| # | Name | Method | Suggested path | Params / body | Response `data` |
|---|---|---|---|---|---|
| 1 | `branches` | GET | `branches` | `search` (name, code, city, address), `status` (`active`·`inactive`, empty = all) | `{ summary: { total, active, inactive }, branches: [branch], permissions: { can_manage } }` |
| 2 | `branchCreate` | POST | `branches` | 21.1 | branch |
| 3 | `branchUpdate` | POST | `branches/{id}` | 21.1 | branch |
| 4 | `branchToggleStatus` | POST | `branches/{id}/status` | `{ is_active: 0/1 }` | – |
| 5 | `branchSetMain` | POST | `branches/{id}/main` | – | – |
| 6 | `branchDelete` | DELETE | `branches/{id}` | – | – |

Branch (shared object — also used by dashboard, invoices, purchases, expenses, reports):
```json
{
  "id": "b1", "name": "الفرع الرئيسي — العليا", "short_name": "العليا", "code": "BR-001",
  "city_id": "1", "city": "الرياض", "address": "…", "phone": "0112458800", "email": "…", "manager": "عبدالله الشمري",
  "is_active": true, "is_main": true, "staff_count": 12, "operations_count": 1240, "created_at": "2024-01-15"
}
```
In pickers only `id`, `name`, `short_name`, `is_active` are needed.

### 21.1 Body
```json
{ "name": "فرع النخيل", "code": "BR-002", "city_id": "1", "address": "…", "phone": "…", "email": "…", "manager": "…", "is_active": 1 }
```

---

## 22. Users, roles & audit log

More › "المستخدمون والصلاحيات". Rules (agreed):
- A new user is **`pending`** (pending activation) until they accept the invitation — the backend sends the invite on create. No status on create; once activated, edit can switch active / inactive.
- **Roles are read-only in the app** (managed on the web). The owner's system role isn't assignable.
- The owner can't be deactivated or deleted. Delete only with no operations (`operations_count == 0`), otherwise deactivate (can't sign in, operations kept).
- Actions show only with `permissions.can_manage`. A disabled user gets **403** on any request (§0.4).

| # | Name | Method | Suggested path | Params / body | Response `data` |
|---|---|---|---|---|---|
| 1 | `businessUsers` | GET | `users` | `search` (name, mobile, email, role), `status` (`active`·`pending`·`inactive`, empty = all) | `{ summary: { total, active, pending, inactive }, users: [user], permissions: { can_manage } }` |
| 2 | `businessUserFormOptions` | GET | `users/form-options` | – | `{ roles: [role] (assignable only), branches: [ { id, name, is_active } ] }` |
| 3 | `businessUserCreate` | POST | `users` | 22.1 | user |
| 4 | `businessUserUpdate` | POST | `users/{id}` | 22.1 (+ `is_active` for an activated user) | user |
| 5 | `businessUserToggleStatus` | POST | `users/{id}/status` | `{ is_active: 0/1 }` | – |
| 6 | `businessUserResendInvite` | POST | `users/{id}/resend-invite` | – | – |
| 7 | `businessUserDelete` | DELETE | `users/{id}` | – | – |
| 8 | `businessRoles` | GET | `roles` | – | `{ roles: [role] }` |
| 9 | `auditLog` | GET | `audit-log` | `user_id` (optional), `page` | `{ log: [entry], meta }` |

User:
```json
{
  "id": "u2", "name": "ماهر السبيعي", "phone": "553318820", "phone_code": "966", "email": "…", "job_title": "مدير المشتريات",
  "role": { "id": "r2", "name": "مسؤول المخزون والمشتريات" },
  "all_branches": false, "branches": [ { "id": "b1", "name": "العليا" } ],
  "status": "active", "is_owner": false,
  "created_at": "2024-03-02", "last_login_at": "اليوم · 07:58", "operations_count": 186
}
```
Role:
```json
{ "id": "r2", "name": "مسؤول المخزون والمشتريات", "description": "…", "allowed": "عرض · إضافة · تعديل · اعتماد (المشتريات)", "denied": "الرواتب · القيود المحاسبية", "is_system": false, "users_count": 2 }
```
(`allowed` / `denied` = your display summaries of the role permissions.)

Audit log entry (the whole business's operations log):
```json
{ "id": "l3", "user_id": "u1", "user_name": "عبدالله الشمري", "action": "تعديل بيانات المنشأة", "module": "إعدادات المنشأة", "reference": "رقم جوال التواصل", "at": "2026-08-11 · 09:24", "kind": "edit", "kind_label": "تعديل", "before": "0551234400", "after": "0551234417" }
```
`kind`: `add` · `edit` · `approve` · `disable` · `cancel` · `delete`. `before` / `after` optional (edits).

### 22.1 Body
```json
{ "name": "…", "phone": "…", "phone_code": "966", "email": "…", "job_title": "…", "role_id": "r2", "all_branches": 0, "branch_ids": ["b1", "b2"] }
```

---

## 23. App settings & account deletion

| # | Name | Method | Suggested path | Body | Response `data` |
|---|---|---|---|---|---|
| 1 | `appSettings` | GET | `settings` | – | 23.1 |
| 2 | `appSettingsUpdate` | POST | `settings` | any of: `notifications_enabled` (0/1), `disabled_categories` ([key]), `lang` (`ar`·`en`) | – |
| 3 | `accountDelete` | POST | `account/delete` | `{ reason }` | – (the app signs out) |

### 23.1 Settings
```json
{
  "notifications_enabled": true,
  "lang": "ar",
  "categories": [
    { "key": "stock", "name": "المخزون", "description": "نفاد الأصناف والحد الأدنى", "is_locked": false, "is_enabled": true },
    { "key": "security", "name": "الأمان والحساب", "description": "تسجيل الدخول وتغيير كلمة المرور", "is_locked": true, "is_enabled": true }
  ]
}
```
- Category keys in the design: `stock` · `purchases` · `finance` · `payroll` · `tax` · `reports` · `meetings` · `security` (locked on).
- **Respect these settings when sending pushes**; `lang` = the language for pushes / messages.
- Account deletion: a request — the account is deleted after a grace period; **signing in during the grace period cancels it**.

---

## 24. Customers

BRD "عملاء المنشأة" (More › تشغيل). `type`: `business` (VAT number + CR **required** — gets a full tax invoice) · `individual` (simplified invoice; VAT / CR optional, checked when entered).
Rules: delete only when the customer has **no invoices / transactions** (`can_delete`), otherwise set inactive. Inactive customers can't be picked in new invoices. Edited data applies to **new operations only**.

| # | Name | Method | Suggested path | Params / body | Response `data` |
|---|---|---|---|---|---|
| 1 | `customers` | GET | `customers` | `search` (name, mobile, VAT number), `status` (`active`·`inactive`), `type` (`business`·`individual`) | `{ summary: { total, active, inactive, business, individual, total_due }, customers: [customer] }` |
| 2 | `customerDetails` | GET | `customers/{id}` | – | customer + `invoices: [ { id, number, date, status, total, remaining } ]` |
| 3 | `customerCreate` | POST | `customers` | 24.1 | `{ id, … }` |
| 4 | `customerUpdate` | POST | `customers/{id}` | 24.1 | `{ id, … }` |
| 5 | `customerDelete` | DELETE | `customers/{id}` | – | – (refuse when it has invoices) |

Customer:
```json
{
  "id": "c1", "name": "شركة الأفق للتجارة", "type": "business", "is_active": true,
  "phone": "551234567", "email": "info@…", "vat_number": "310122334400003", "commercial_register": "1010223344",
  "national_address": "الرياض · حي العليا · 7421 · 12244", "created_at": "2026-03-14",
  "invoices_count": 2, "total_invoiced": 7130, "due": 4830, "can_delete": false
}
```
Invoice `status`: `unpaid` · `partial` · `paid`. "Create invoice" from the customer opens the invoice form with this customer.

### 24.1 Body
```json
{ "name": "…", "type": "business", "is_active": 1, "phone": "…", "email": "…", "vat_number": "…", "commercial_register": "…", "national_address": "…" }
```

---

## 25. Items (products) & categories

BRD "الأصناف". Main › sub category (a sub-category belongs to one main category). Items have **Active / Inactive** status (design, agreed) — inactive items stay in records but can't be picked in new invoices. A new price / VAT applies to **new invoices only**. Price ≥ 0, VAT 0–100.
These are the same items used by invoices, inventory ("existing item") and recipes.

| # | Name | Method | Suggested path | Params / body | Response `data` |
|---|---|---|---|---|---|
| 1 | `products` | GET | `products` | `search` (name), `category_id` (main) | 25.1 |
| 2 | `productDetails` | GET | `products/{id}` | – | product + `recipe: [ { id, name, unit, quantity } ]` (raw materials per unit, from the inventory recipe) |
| 3 | `productCreate` | POST | `products` | 25.2 | `{ id, … }` |
| 4 | `productUpdate` | POST | `products/{id}` | 25.2 | `{ id, … }` |
| 5 | `productCategories` | GET | `products/categories` | – | `{ categories: [ { id, name, products_count, sub_categories: [ { id, name } ] } ] }` |
| 6 | `productCategoryCreate` | POST | `products/categories` | `{ name, parent_id? }` (no `parent_id` = main category) | – |

### 25.1 List
```json
{
  "summary": { "products_count": 9, "categories_count": 4, "sub_categories_count": 7, "average_price": 17.67 },
  "categories": [ { "id": "g1", "name": "القهوة", "products_count": 3, "sub_categories": [ { "id": "g1-1", "name": "القهوة الساخنة" } ] } ],
  "products": [
    { "id": "p1", "name": "لاتيه", "category_id": "g1", "category": "القهوة", "sub_category_id": "g1-1", "sub_category": "القهوة الساخنة", "price": 18, "vat_rate": 15, "is_active": true, "updated_at": "2026-08-02" }
  ]
}
```
`price` = selling price before VAT (the app shows price with VAT = price × (1 + vat_rate/100)).

### 25.2 Body
```json
{ "category_id": "g1", "sub_category_id": "g1-1", "name": "لاتيه", "price": 18, "vat_rate": 15, "is_active": 1 }
```

---

## 26. Assets & depreciation

BRD "الأصول والإهلاك" — **read-only for the owner** (registered and approved by the accountant). Straight-line, computed by you: depreciable = cost − salvage; annual = depreciable ÷ life years; monthly = annual ÷ 12; book value = cost − accumulated (never below salvage). The depreciation log is kept (never replaced).
`status`: `active` · `fully_depreciated` · `disposed`.

| # | Name | Method | Suggested path | Params | Response `data` |
|---|---|---|---|---|---|
| 1 | `assets` | GET | `assets` | `search` (name), `status`, `type` | `{ summary: { count, cost_total, accumulated_total, book_total, monthly_total, types: [string] }, assets: [asset] }` |
| 2 | `assetDetails` | GET | `assets/{id}` | – | asset + `log` |

Asset:
```json
{
  "id": "a1", "name": "فرن غاز صناعي", "type": "معدات",
  "cost": 48000, "salvage_value": 3000, "purchase_date": "2024-03-12", "depreciation_start": "2024-04-01", "life_years": 5,
  "branch": "الفرع الرئيسي — العليا", "status": "active", "notes": "…",
  "depreciable": 45000, "annual_depreciation": 9000, "monthly_depreciation": 750,
  "accumulated": 21000, "book_value": 27000, "as_of": "2026-08-31",
  "log": [ { "period": "2026-08", "value_before": 27750, "depreciation": 750, "accumulated": 21000, "book_after": 27000, "recorded_at": "2026-08-28" } ]
}
```
`summary.monthly_total` = monthly depreciation of active, not fully depreciated assets. `types` = asset types for the filter.

---

## 27. Payroll & employees

BRD "مسير الرواتب". Each business's employees / salaries are separate.

**Run status:** `draft` → `ready_for_review` → `approved` → `ready_for_payment` → `paid`
Flow: owner picks a month → creates its run (active employees with their base salaries) → edits lines while not approved → send for review → **approve** (final; record the salaries liability; refuse incomplete / wrong salary data) → **export the bank transfer file** (→ `ready_for_payment`; blocked while an employee has no IBAN; exporting does **not** mark paid) → **record the transfer** (→ `paid`; settle the liability; create the payment entry once).
**Payslip status** (per employee line): `preparing` · `approved` · `ready_for_payment` · `paid`.
**Work days** come from the backend; the **overtime hour rate** is set on the run while it isn't approved.

**Formulas** (compute on the server; the app repeats them only for the live preview):
daily = base ÷ work days · absence = days × daily · overtime = hours × hour rate · gross = base + overtime + allowances · deductions = absence + other deductions · net = gross − deductions.

| # | Name | Method | Suggested path | Params / body | Response `data` |
|---|---|---|---|---|---|
| 1 | `payrollRun` | GET | `payroll/run` | `period` (`2026-08`; empty = the open run or the current month) | `{ period, period_label, can_create, run: run \| null }` |
| 2 | `payrollRunCreate` | POST | `payroll/runs` | `{ period }` | same as #1 |
| 3 | `payrollRunRate` | POST | `payroll/runs/{id}/overtime-rate` | `{ overtime_rate }` | – |
| 4 | `payrollLineUpdate` | POST | `payroll/runs/{id}/line` | `{ employee_id, absence_days, overtime_hours, extra_allowances, extra_deductions, notes }` | – |
| 5 | `payrollRunSubmit` | POST | `payroll/runs/{id}/submit` | – | – → `ready_for_review` |
| 6 | `payrollRunApprove` | POST | `payroll/runs/{id}/approve` | – | – → `approved` |
| 7 | `payrollRunExport` | POST | `payroll/runs/{id}/export` | – | `{ file_url }` → `ready_for_payment` |
| 8 | `payrollRunPay` | POST | `payroll/runs/{id}/pay` | – | – → `paid` |
| 9 | `payrollRuns` | GET | `payroll/runs` | – | `{ runs: [ { id, period, period_label, status, approved_at, paid_at, totals } ] }` newest first |
| 10 | `employees` | GET | `employees` | `search` (name, employee number), `status` (`active`·`inactive`) | `{ summary: { total, active, active_base_total }, current_run, employees: [employee] }` |
| 11 | `employeeDetails` | GET | `employees/{id}` | – | employee + `current_run`, `current_line` (null when not in the run), `branches`, `logs` |
| 12 | `employeeFormOptions` | GET | `employees/form-options` | – | `{ branches: [branch] }` |
| 13 | `employeeCreate` | POST | `employees` | 27.3 | `{ id }` — refuse a used employee number |
| 14 | `employeeUpdate` | POST | `employees/{id}` | 27.3 | `{ id }` |
| 15 | `employeeAction` | POST | `employees/{id}/action` | `{ action, …fields }` (27.4) | – |

### 27.1 Run
```json
{
  "id": "run-2026-08", "period": "2026-08", "period_label": "أغسطس 2026",
  "status": "draft", "work_days": 30, "overtime_rate": 45,
  "approved_at": "", "paid_at": "", "journal_entry_id": "", "file_exported": false,
  "can_edit": true, "can_submit": true, "can_approve": true, "can_export": false, "can_mark_paid": false,
  "totals": { "employees_count": 14, "base": 78000, "gross": 84500, "extra_allowances": 6500, "deductions": 1200, "net": 83300 },
  "lines": [
    {
      "employee_id": "e1", "name": "…", "number": "EMP-001", "title": "مدير فرع", "branch": "الفرع الرئيسي", "notes": "",
      "base_salary": 9000, "absence_days": 1, "overtime_hours": 4, "extra_allowances": 500, "extra_deductions": 0,
      "daily_rate": 300, "absence_value": 300, "overtime_value": 180,
      "gross": 9680, "total_deductions": 300, "net": 9380,
      "has_bank_account": true, "status": "preparing"
    }
  ]
}
```
- The buttons follow `can_*` exactly (backend is the judge).
- `journal_entry_id` (after paid) → "view entry" opens the journal entry.
- `can_create` (in #1) = the month's run can be created (not a future month, no run yet).

### 27.2 Employee
```json
{
  "id": "e1", "name": "…", "number": "EMP-001", "title": "مدير فرع",
  "branch_id": "b1", "branch": "الفرع الرئيسي", "join_date": "2024-01-15",
  "iban": "SA0380000000608010167519", "bank_holder": "…",
  "base_salary": 9000, "next_salary": 9500, "next_salary_from": "2026-10-01",
  "is_active": true, "current_net": 9380
}
```
`current_run` (in list + details):
```json
{ "period": "2026-08", "period_label": "أغسطس 2026", "exists": true, "is_locked": false, "work_days": 30, "overtime_rate": 45 }
```
`logs`: `[ { id, title, text, date, tone } ]` — `tone`: `success` · `danger` · `info` · `gold`.
`next_salary` / `next_salary_from` = a salary change waiting for its effective date.

### 27.3 Employee body
```json
{ "name": "…", "number": "EMP-015", "title": "…", "branch_id": "b1", "join_date": "2026-10-01", "base_salary": 6000, "iban": "SA…", "is_active": 1 }
```
`branch_id` only when the business has more than one branch (default = main branch).

### 27.4 Employee actions (`employeeAction`)
| `action` | Fields | Notes |
|---|---|---|
| `deduction` | `type` (`absence`·`penalty`·`advance`·`other`), `days` (absence) **or** `amount`, `reason` | goes on the open run; amount ≤ current net; days ≤ remaining work days |
| `bonus` | `type` (`performance`·`allowance`·`commission`·`other`), `amount`, `reason` | goes on the open run |
| `overtime` | `hours`, `note` | goes on the open run; needs the run's hour rate |
| `salary` | `reason` (`annual`·`promotion`·`contract`·`correction`), `base_salary`, `effective_from`, `note` | |
| `bank` | `iban` (`SA` + 22 digits), `holder` | |
| `branch` | `branch_id`, `date` | |
| `deactivate` | `reason` (`resignation`·`termination`·`unpaid_leave`·`other`), `date` (last day), `note` | |
| `activate` | `date`, `note` | |

`deduction` / `bonus` / `overtime` must be refused when the run is approved (locked) or the employee is inactive. Log every action in the employee `logs`.


---

## 28. Static pages

Pages the admin publishes (terms, privacy, FAQ, contact us, about…). **Both endpoints must work without a token** (the register screen opens terms / privacy). Answer in the `Accept-Language` language.

| # | Name | Method | Suggested path | Response `data` |
|---|---|---|---|---|
| 1 | `staticPages` | GET | `pages` | `[ { key, title, subtitle } ]` in the admin's order (data is a list) |
| 2 | `staticPageDetails` | GET | `pages/{key}` | page with sections |

```json
{
  "key": "terms", "title": "الشروط والأحكام", "subtitle": "آخر تحديث 12 يوليو 2026",
  "sections": [
    { "title": "نطاق الخدمة", "body": "…", "links": [ { "type": "email", "value": "support@capitalix.sa", "label": "الدعم" } ] }
  ]
}
```
Link `type`: `email` · `phone` · `whatsapp` · `url` (tappable). Keys the app opens directly: `terms`, `privacy`.

---

## 29. General lookups

| # | Name | Method | Path | Params | Response `data` |
|---|---|---|---|---|---|
| 1 | `generalCountries` | GET | `general/countries` (**already set in the app**) | `keyword` | `[ { id, name, phone_code, flag, phone_limit } ]` |
| 2 | `generalCities` | GET | `general/cities` | `keyword` | `[ { id, name } ]` |

---

## 30. Endpoint checklist

Tick each one when it's live and send me the final path. **Total: 160 endpoints** (1 already live).

| Section | Endpoints |
|---|---|
| 1 Auth | `authLogin` · `authRegister` · `authSendCode` · `authVerifyCode` · `passwordForget` · `passwordVerifyCode` · `passwordReset` · `authProfile` · `authLogout` · `registrationRequest` · `registrationRequestUpdate` |
| 2 Subscription | `subscriptionPlans` · `subscriptionPaymentInfo` · `subscriptionPay` |
| 4 Dashboard | `dashboard` |
| 5 Notifications | `notifications` · `notificationDetails` · `notificationsUnreadCount` · `notificationRead` · `notificationUnread` · `notificationsReadAll` · `notificationDelete` |
| 6 Inventory | `inventoryItems` · `inventoryItemDetails` · `inventoryItemLimits` · `inventoryItemCreate` · `inventoryFormOptions` · `inventoryItemStock` · `inventorySync` · `inventoryRecipes` · `inventoryRecipeDetails` · `inventoryRecipeSave` |
| 7 Invoices | `invoices` · `invoiceDetails` · `invoiceFormOptions` · `invoiceCreate` · `invoiceCollectionMethods` · `invoiceCollectionScan` · `invoiceCollect` · `quotes` · `quoteDetails` · `quoteCreate` · `quoteConvert` |
| 8 Purchases | `purchaseOrders` · `purchaseOrderDetails` · `purchaseFormOptions` · `purchaseOrderCreate` · `purchaseOrderUpdate` · `purchaseOrderGenerate` · `purchaseOrderSend` · `purchaseOrderInvoice` · `purchaseOrderDelivery` · `purchaseOrderReceive` · `purchaseOrderCancel` |
| 9 Suppliers | `suppliers` · `supplierDetails` · `supplierCreate` · `supplierUpdate` · `supplierToggleStatus` · `supplierPayInvoice` · `supplierPaymentScan` |
| 10 Expenses | `expenseScan` · `expenseFormOptions` · `expenseCreate` · `expenses` · `expenseDetails` · `expenseAnalysis` · `expenseUpdate` |
| 11 VAT | `vatSummary` · `vatInvoiceUpload` · `vatExport` |
| 12 Zakat | `zakat` · `zakatSubmit` · `zakatApprove` · `zakatHistory` |
| 13 Statements | `statementsSummary` · `accounts` · `journalEntries` · `journalEntryDetails` · `journalEntryRequest` · `ledger` · `trialBalance` · `financialStatement` · `profitReport` · `monthlyReport` · `monthlyReportCustomize` · `statementsExport` · `statementsExportBundle` |
| 14 Waste | `waste` |
| 15 Pricing | `pricing` · `pricingDetails` · `pricingApprove` |
| 16 Meetings | `meetings` · `meetingDetails` · `meetingSlots` · `meetingBook` · `meetingUpdate` · `meetingCancel` |
| 17 Accountant reports | `reports` · `reportDetails` |
| 18 My account | `account` · `accountUpdate` · `accountPhoneSendCode` · `accountPhoneVerify` · `accountPasswordSendCode` · `accountPasswordChange` · `subscriptionDetails` |
| 19 More | `moreSummary` |
| 20 Business settings | `businessSettings` · `businessSettingsUpdate` |
| 21 Branches | `branches` · `branchCreate` · `branchUpdate` · `branchToggleStatus` · `branchSetMain` · `branchDelete` |
| 22 Users | `businessUsers` · `businessUserCreate` · `businessUserUpdate` · `businessUserToggleStatus` · `businessUserResendInvite` · `businessUserDelete` · `businessUserFormOptions` · `businessRoles` · `auditLog` |
| 23 App settings | `appSettings` · `appSettingsUpdate` · `accountDelete` |
| 24 Customers | `customers` · `customerDetails` · `customerCreate` · `customerUpdate` · `customerDelete` |
| 25 Items | `products` · `productDetails` · `productCreate` · `productUpdate` · `productCategories` · `productCategoryCreate` |
| 26 Assets | `assets` · `assetDetails` |
| 27 Payroll | `payrollRun` · `payrollRunCreate` · `payrollRunRate` · `payrollLineUpdate` · `payrollRunSubmit` · `payrollRunApprove` · `payrollRunExport` · `payrollRunPay` · `payrollRuns` · `employees` · `employeeDetails` · `employeeFormOptions` · `employeeCreate` · `employeeUpdate` · `employeeAction` |
| 28 Static pages | `staticPages` · `staticPageDetails` |
| 29 Lookups | `generalCountries` ✅ · `generalCities` |

### Suggested delivery order
1. **Auth + subscription + profile** (§1, §2, §3, §29) — nothing works without sign-in and the `modules` list.
2. **Dashboard + notifications + push** (§4, §5).
3. **Items, customers, branches** (§25, §24, §21) — other modules pick from them.
4. **Invoices, inventory, suppliers, purchases, expenses** (§7, §6, §9, §8, §10).
5. **VAT, statements, zakat, waste, pricing, reports, meetings** (§11–§17).
6. **Account, business settings, users, app settings, More summary, static pages** (§18–§23, §28).
7. **Payroll, assets** (§27, §26).

### Open points to agree on
1. **Online payment gateway** (§2) — which gateway and how the app opens it (webview URL + redirect, or SDK).
2. **"Not in your plan" error** (§3) — status code / message for requests to a module outside the package (403 is reserved for banned accounts).
3. **Exact keys** — if any key / enum here doesn't fit your models, tell me before building and we'll agree once.
4. **Display texts** (`*_label`, `status` texts, `date` like "اليوم · 09:12") — confirm you'll pre-format them in the request language, or send raw values and I'll format them.

