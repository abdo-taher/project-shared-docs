import 'api_client.dart';
import 'endpoints.dart';

/// Contract enum `CustomerType`.
enum CustomerType {
  individual('INDIVIDUAL'),
  organization('ORGANIZATION');

  const CustomerType(this.wire);
  final String wire;

  /// Null for a value the request enum does not define.
  static CustomerType? tryParse(String value) =>
      values.where((t) => t.wire == value).firstOrNull;
}

/// Contract enum of `customer-balances[].payment_status` (null: no invoices yet).
enum PaymentStatus {
  unpaid('UNPAID'),
  partiallyPaid('PARTIALLY_PAID'),
  paid('PAID');

  const PaymentStatus(this.wire);
  final String wire;

  static PaymentStatus? parse(Object? value) => value == null
      ? null
      : values.firstWhere((s) => s.wire == value,
          orElse: () => throw FormatException('unknown PaymentStatus $value'));
}

/// Contract schema `CustomerResource` (every field is required; some nullable).
/// The contract types `type` and `status` as plain strings in responses (only
/// requests use the `CustomerType` enum), so the raw values are kept.
class Customer {
  Customer.fromJson(Map<String, Object?> json)
      : id = json['id']! as String,
        name = json['name']! as String,
        type = json['type']! as String,
        status = json['status']! as String,
        mobile = json['mobile'] as String?,
        email = json['email'] as String?,
        taxNumber = json['tax_number'] as String?,
        commercialRegistrationNo = json['commercial_registration_no'] as String?,
        nationalAddress = json['national_address'] as String?,
        createdAt = json['created_at']! as String,
        updatedAt = json['updated_at']! as String;

  final String id;
  final String name;
  final String type;
  final String status;

  /// [type] as the request enum, when it is one of its values.
  CustomerType? get knownType => CustomerType.tryParse(type);
  final String? mobile;
  final String? email;
  final String? taxNumber;
  final String? commercialRegistrationNo;
  final String? nationalAddress;
  final String createdAt;
  final String updatedAt;
}

/// Contract schema `PaginationMeta`.
class PageMeta {
  PageMeta.fromJson(Map<String, Object?> json)
      : currentPage = json['current_page']! as int,
        lastPage = json['last_page']! as int,
        total = json['total']! as int;

  final int currentPage;
  final int lastPage;
  final int total;

  bool get hasMore => currentPage < lastPage;
}

/// A paginated list payload: `data: {items: [...], meta: {...}}`.
class Page<T> {
  Page(this.items, this.meta);

  final List<T> items;
  final PageMeta meta;
}

/// One row of `GET /api/owner/sales/customer-balances`.
/// Amounts are decimal strings in the contract: keep them exact.
class CustomerBalance {
  CustomerBalance.fromJson(Map<String, Object?> json)
      : customerReference = json['customer_reference']! as String,
        name = json['name']! as String,
        mobile = json['mobile'] as String?,
        invoiceCount = json['invoice_count']! as int,
        paidAmount = json['paid_amount']! as String,
        remainingAmount = json['remaining_amount']! as String,
        paymentStatus = PaymentStatus.parse(json['payment_status']),
        hasDebt = json['has_debt']! as bool,
        hasOverdue = json['has_overdue']! as bool;

  final String customerReference;
  final String name;
  final String? mobile;
  final int invoiceCount;
  final String paidAmount;
  final String remainingAmount;
  final PaymentStatus? paymentStatus;
  final bool hasDebt;
  final bool hasOverdue;
}

/// Contract schemas `CreateCustomerRequest` / `UpdateCustomerRequest`.
class CustomerInput {
  const CustomerInput({
    required this.name,
    required this.type,
    this.mobile,
    this.email,
    this.taxNumber,
    this.commercialRegistrationNo,
    this.nationalAddress,
    this.confirmDistinct,
  });

  final String name;
  final CustomerType type;
  final String? mobile;
  final String? email;
  final String? taxNumber;
  final String? commercialRegistrationNo;
  final String? nationalAddress;

  /// Send `true` to confirm after the server answered 409 (likely duplicate).
  final bool? confirmDistinct;

  Map<String, Object?> toJson() => {
        'name': name,
        'type': type.wire,
        if (mobile != null) 'mobile': mobile,
        if (email != null) 'email': email,
        if (taxNumber != null) 'tax_number': taxNumber,
        if (commercialRegistrationNo != null) 'commercial_registration_no': commercialRegistrationNo,
        if (nationalAddress != null) 'national_address': nationalAddress,
        if (confirmDistinct != null) 'confirm_distinct': confirmDistinct,
      };
}

/// The Owner app Customers feature, bound to the pinned contract.
class CustomersApi {
  CustomersApi(this._client);

  final CapitalixApiClient _client;

  /// `GET customer-balances` — filters and pagination exactly as the contract
  /// defines them; `meta` tells the caller whether more pages exist.
  Future<Page<CustomerBalance>> listBalances({
    String? name,
    String? mobile,
    PaymentStatus? paymentStatus,
    bool? hasDebt,
    int? page,
    int? perPage,
  }) async {
    if (perPage != null && (perPage < 1 || perPage > 100)) {
      throw ArgumentError.value(perPage, 'perPage', 'contract allows 1..100');
    }
    final data = await _client.send('GET', Endpoints.customerBalances, query: {
      'name': name,
      'mobile': mobile,
      'payment_status': paymentStatus?.wire,
      'has_debt': hasDebt == null ? null : (hasDebt ? 'true' : 'false'),
      'page': page,
      'per_page': perPage,
    });
    final payload = _object(data);
    return Page(
      [
        for (final row in (payload['items'] as List? ?? const []))
          CustomerBalance.fromJson((row as Map).cast<String, Object?>()),
      ],
      PageMeta.fromJson(_object(payload['meta'])),
    );
  }

  /// `POST customers` → 201 with the created `CustomerResource`.
  Future<Customer> create(CustomerInput input) async =>
      Customer.fromJson(_object(await _client.send('POST', Endpoints.customers, body: input.toJson())));

  /// `PUT customers/{id}` (full update; the owner-app spec suggested POST).
  Future<Customer> update(String id, CustomerInput input) async =>
      Customer.fromJson(_object(await _client.send('PUT', Endpoints.customer(id), body: input.toJson())));

  /// `DELETE customers/{id}` — 409/422 when the customer has transactions.
  Future<void> delete(String id) => _client.send('DELETE', Endpoints.customer(id));

  static Map<String, Object?> _object(Object? data) =>
      (data as Map? ?? (throw const FormatException('expected an object in data'))).cast<String, Object?>();
}
