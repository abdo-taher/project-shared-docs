import 'dart:convert';

import 'package:http/http.dart' as http;

/// Error envelope of every `api/*` error response (contract: `ErrorEnvelope`):
/// `{message, errors: {field: [messages]}, code, correlation_id, details}`.
class ApiException implements Exception {
  ApiException(this.status, this.message, this.code, this.errors, this.correlationId);

  final int status;
  final String message;
  final String? code;
  final Map<String, List<String>> errors;
  final String? correlationId;

  /// 422: field validation failed — show [firstError].
  bool get isValidation => status == 422;

  /// 401: token invalid/expired — the app clears the session.
  bool get isUnauthenticated => status == 401;

  /// 403: forbidden (account disabled, or the permission is missing).
  bool get isForbidden => status == 403;

  /// 409: conflicts with current state (e.g. a likely duplicate customer).
  bool get isConflict => status == 409;

  bool get isNotFound => status == 404;

  /// What the app shows: the first field error, else [message].
  String get firstError =>
      errors.values.expand((messages) => messages).firstOrNull ?? message;

  @override
  String toString() => 'ApiException($status ${code ?? ''}: $firstError)';
}

/// Thin JSON client: auth header, language, success-envelope unwrapping.
class CapitalixApiClient {
  CapitalixApiClient({
    required this.baseUrl,
    http.Client? httpClient,
    this.language = 'ar',
    this.token,
  }) : _http = httpClient ?? http.Client();

  final Uri baseUrl;
  final String language;
  final http.Client _http;
  String? token;

  Map<String, String> get _headers => {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Accept-Language': language,
        if (token != null) 'Authorization': 'Bearer $token',
      };

  Uri _uri(String path, [Map<String, Object?>? query]) {
    final params = <String, String>{
      for (final entry in (query ?? const {}).entries)
        // Null or empty params are not sent (owner-app convention).
        if (entry.value != null && entry.value.toString().isNotEmpty)
          entry.key: entry.value.toString(),
    };
    return baseUrl.replace(
      path: '${baseUrl.path.replaceAll(RegExp(r'/$'), '')}$path',
      queryParameters: params.isEmpty ? null : params,
    );
  }

  /// Returns the envelope `data` of a 2xx response; throws [ApiException].
  Future<Object?> send(
    String method,
    String path, {
    Map<String, Object?>? query,
    Map<String, Object?>? body,
  }) async {
    final request = http.Request(method, _uri(path, query))..headers.addAll(_headers);
    if (body != null) request.body = jsonEncode(body);
    final response = await http.Response.fromStream(await _http.send(request));
    final decoded = _decode(response);
    if (response.statusCode >= 200 && response.statusCode < 300) {
      return decoded is Map<String, Object?> ? decoded['data'] : null;
    }
    final envelope = decoded is Map<String, Object?> ? decoded : const <String, Object?>{};
    final rawErrors = envelope['errors'];
    throw ApiException(
      response.statusCode,
      envelope['message'] as String? ?? 'Request failed (${response.statusCode})',
      envelope['code'] as String?,
      {
        if (rawErrors is Map)
          for (final entry in rawErrors.entries)
            entry.key.toString(): [for (final m in (entry.value as List? ?? const [])) m.toString()],
      },
      envelope['correlation_id'] as String?,
    );
  }

  static Object? _decode(http.Response response) {
    if (response.body.isEmpty) return null;
    try {
      return jsonDecode(utf8.decode(response.bodyBytes));
    } on FormatException {
      return null; // HTML / non-JSON (5xx): handled as a generic failure.
    }
  }

  void close() => _http.close();
}
