import 'api_client.dart';
import 'endpoints.dart';

/// `POST /api/auth/login` (contract: `IssueTokenRequest`). The 201 `data` is
/// either a token object or the owner user object; both carry `token`.
class AuthApi {
  AuthApi(this._client);

  final CapitalixApiClient _client;

  Future<String> login({
    required String login,
    required String password,
    required String deviceName,
  }) async {
    final data = await _client.send('POST', Endpoints.login, body: {
      'login': login,
      'password': password,
      'device_name': deviceName,
    });
    final token = (data as Map?)?['token'];
    if (token is! String || token.isEmpty) {
      throw const FormatException('login response has no token');
    }
    _client.token = token;
    return token;
  }
}
