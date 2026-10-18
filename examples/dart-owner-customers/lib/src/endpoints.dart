/// Paths come from the pinned contract (.capitalix-contract/contract.lock).
/// `python3 ../../tools/capitalix_contract.py check lib/` proves each exists.
/// Canonical routes only: `/api/v1/*` are deprecated aliases.
abstract final class Endpoints {
  /// POST — operationId `auth.login`.
  static const login = '/api/auth/login';

  /// GET (paginated: page, per_page) — operationId `owner.sales.customer-balances`.
  /// The contract has no plain GET customers list; this is the closest list.
  static const customerBalances = '/api/owner/sales/customer-balances';

  /// POST — operationId `owner.sales.customers.store`.
  static const customers = '/api/owner/sales/customers';

  /// GET / PUT / DELETE — operationIds `owner.sales.customers.{show,update,destroy}`.
  static String customer(String id) => '/api/owner/sales/customers/$id';
}
