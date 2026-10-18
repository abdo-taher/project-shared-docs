import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;

/// Records every exchange so `capitalix_contract.py validate` can check the
/// exact requests sent and responses received against the pinned contract.
class RecordingClient extends http.BaseClient {
  RecordingClient(this._inner);

  final http.Client _inner;
  final List<Map<String, Object?>> exchanges = [];

  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) async {
    final body = request is http.Request && request.body.isNotEmpty ? jsonDecode(request.body) : null;
    final streamed = await _inner.send(request);
    final bytes = await streamed.stream.toBytes();
    Object? decoded;
    try {
      decoded = bytes.isEmpty ? null : jsonDecode(utf8.decode(bytes));
    } on FormatException {
      decoded = null;
    }
    exchanges.add({
      'method': request.method,
      'path': request.url.path,
      'query': request.url.queryParameters,
      'body': body,
      'status': streamed.statusCode,
      if (decoded != null) 'response': decoded,
    });
    return http.StreamedResponse(Stream.value(bytes), streamed.statusCode,
        headers: streamed.headers, request: request, reasonPhrase: streamed.reasonPhrase);
  }

  void writeTo(String path) {
    File(path)
      ..parent.createSync(recursive: true)
      ..writeAsStringSync(const JsonEncoder.withIndent(' ').convert(exchanges));
  }
}
