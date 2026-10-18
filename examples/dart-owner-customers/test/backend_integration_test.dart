@Tags(['backend'])
library;

import 'dart:io';

import 'package:capitalix_owner_customers_example/capitalix_owner_customers.dart';
import 'package:http/http.dart' as http;
import 'package:test/test.dart';

import 'support/recording_client.dart';

/// Runs against a REAL Capitalix backend (never production data):
///   CAPITALIX_BASE_URL=http://127.0.0.1:8765 CAPITALIX_LOGIN=... CAPITALIX_PASSWORD=...
///   dart test --tags backend
/// Real traffic is recorded to build/traffic-backend.json; then
///   python3 ../../tools/capitalix_contract.py validate build/traffic-backend.json
/// proves the backend's actual responses conform to the pinned contract.
void main() {
  final env = Platform.environment;
  final base = env['CAPITALIX_BASE_URL'];
  final skip = base == null ? 'set CAPITALIX_BASE_URL to run against a real backend' : null;

  late RecordingClient recorder;
  late CapitalixApiClient client;
  late CustomersApi customers;
  final stamp = DateTime.now().millisecondsSinceEpoch;

  setUpAll(() async {
    if (base == null) return;
    recorder = RecordingClient(http.Client());
    client = CapitalixApiClient(baseUrl: Uri.parse(base), httpClient: recorder, language: 'en');
    await AuthApi(client).login(
        login: env['CAPITALIX_LOGIN']!, password: env['CAPITALIX_PASSWORD']!, deviceName: 'contract-e2e');
    customers = CustomersApi(client);
  });

  tearDownAll(() {
    if (base != null) recorder.writeTo('build/traffic-backend.json');
  });

  test('create → update → list → delete a customer', () async {
    // The backend requires tax_number for ORGANIZATION although the contract
    // marks it optional (conditional rule; recorded in the gap mapping).
    final taxNumber = '3${(stamp % 10000000000000).toString().padLeft(13, '0')}3';
    final register = (stamp % 10000000000).toString().padLeft(10, '1');
    final created = await customers.create(CustomerInput(
        name: 'E2E Customer $stamp', type: CustomerType.organization,
        email: 'e2e-$stamp@example.test', taxNumber: taxNumber, commercialRegistrationNo: register));
    expect(created.name, 'E2E Customer $stamp');
    expect(created.knownType, CustomerType.organization);

    final updated = await customers.update(created.id, CustomerInput(
        name: 'E2E Customer $stamp (edited)', type: CustomerType.organization,
        email: 'e2e-$stamp@example.test', taxNumber: taxNumber, commercialRegistrationNo: register));
    expect(updated.id, created.id);
    expect(updated.name, endsWith('(edited)'));

    final page = await customers.listBalances(name: 'E2E Customer $stamp', page: 1, perPage: 50);
    expect(page.items.map((row) => row.customerReference), contains(created.id));
    expect(page.meta.currentPage, 1);
    expect(page.meta.total, greaterThanOrEqualTo(1));

    await customers.delete(created.id);
  }, skip: skip);

  test('invalid input is a 422 with field errors', () async {
    final error = await customers
        .create(const CustomerInput(name: '', type: CustomerType.individual, email: 'not-an-email'))
        .then<ApiException?>((_) => null, onError: (Object e) => e as ApiException);
    expect(error, isNotNull);
    expect(error!.isValidation, isTrue);
    expect(error.errors, isNotEmpty);
  }, skip: skip);

  test('a bad token is a 401', () async {
    final anonymous = CapitalixApiClient(baseUrl: Uri.parse(base ?? 'http://invalid'),
        httpClient: recorder, token: 'invalid-token');
    expect(CustomersApi(anonymous).listBalances(),
        throwsA(isA<ApiException>().having((e) => e.isUnauthenticated, 'isUnauthenticated', isTrue)));
  }, skip: skip);
}
