# Reference consumer — Owner app Customers (Dart)

The Owner app's Customers feature (`api/BACKEND_API.md` §24) implemented
against the **pinned** Capitalix contract: the paginated customer list, create,
update and delete, with 401/403/409/422 handling. Plain Dart (`package:http`),
so the same code drops into the Flutter app's data layer.

| File | |
|---|---|
| `.capitalix-contract/contract.lock`, `manifest.json` | the pinned version (`openapi.json` is restored by `sync`) |
| `lib/src/endpoints.dart` | canonical paths from the contract |
| `lib/src/customers.dart` | models and API built from the contract schemas |
| `lib/src/api_client.dart` | envelope and error handling (`SuccessEnvelope`, `ErrorEnvelope`) |
| `test/fixtures/` | responses generated from the contract (`tool/fixtures.sh`) |
| `test/customers_contract_test.dart` | unit tests on contract fixtures; records `build/traffic-mock.json` |
| `test/backend_integration_test.dart` | the same feature against a real backend; records `build/traffic-backend.json` |

```sh
T=../../tools/capitalix_contract.py
python3 $T sync && python3 $T verify --remote   # restore + verify the pin
sh tool/fixtures.sh                               # regenerate fixtures from the pin
dart pub get && dart analyze --fatal-infos
dart test --exclude-tags backend                  # unit tests
python3 $T validate build/traffic-mock.json       # requests/responses conform
python3 $T check lib/                             # every path is in the contract

# against a real (non-production) backend:
CAPITALIX_BASE_URL=http://127.0.0.1:8765 CAPITALIX_LOGIN=… CAPITALIX_PASSWORD=… dart test --tags backend
python3 $T validate build/traffic-backend.json
```

Contract facts this example had to respect (see `api/requirements/owner-app-map.json`):
the list is `customer-balances` (`data.items` + `data.meta`); `type` is
`INDIVIDUAL|ORGANIZATION`; update is `PUT`; amounts are decimal strings;
an `ORGANIZATION` needs `tax_number` (backend rule the contract does not state).
