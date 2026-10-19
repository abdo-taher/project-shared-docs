"""JSON-over-HTTPS client for the GitHub and GitLab REST APIs (stdlib only).

- TLS is verified by urllib's default context; it is never disabled.
- 429, rate-limit 403, 5xx and network timeouts are retried with exponential
  backoff (honouring Retry-After, capped); other statuses fail at once.
- Errors carry the method, a credential-free URL path and the status; never a
  header, a token or a full response body.
"""

from __future__ import annotations

import json
import re
import socket
import time
import urllib.error
import urllib.parse
import urllib.request

USER_AGENT = "capitalix-api-gap-coordinator/1.0"


class ApiError(Exception):
    """A request failed. `transient` is True when retrying later may succeed."""

    def __init__(self, message: str, status: int | None = None, transient: bool = False):
        super().__init__(message)
        self.status = status
        self.transient = transient


_SECRETISH = re.compile(r"(?i)(token|private_token|access_token|key|secret|password)=[^&]+")


def redact(text: str) -> str:
    return _SECRETISH.sub(r"\1=<redacted>", text)


class Http:
    def __init__(self, base: str, headers: dict, *, timeout: float = 30, attempts: int = 5,
                 max_wait: float = 60, sleep=time.sleep, opener=None):
        self.base = base.rstrip("/")
        self.headers = {"User-Agent": USER_AGENT, "Accept": "application/json", **headers}
        self.timeout = timeout
        self.attempts = attempts
        self.max_wait = max_wait
        self.sleep = sleep
        self.opener = opener or urllib.request.build_opener()
        self.calls = 0

    def _url(self, path: str, params: dict | None) -> str:
        url = path if path.startswith("https://") or path.startswith("http://") else f"{self.base}/{path.lstrip('/')}"
        if params:
            url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params, doseq=True)
        return url

    def _wait(self, attempt: int, headers) -> float:
        value = headers.get("Retry-After") if headers else None
        try:
            wait = float(value) if value is not None else 2.0 ** attempt
        except ValueError:
            wait = 2.0 ** attempt
        return min(max(wait, 0.0), self.max_wait)

    @staticmethod
    def _rate_limited(status: int, headers) -> bool:
        if status == 429:
            return True
        return status == 403 and bool(headers) and (headers.get("X-RateLimit-Remaining") == "0"
                                                    or headers.get("RateLimit-Remaining") == "0")

    def request(self, method: str, path: str, *, params: dict | None = None, body=None,
                raw: bool = False, headers: dict | None = None):
        """Returns (decoded JSON or bytes, response headers)."""
        url = self._url(path, params)
        label = f"{method} {redact(urllib.parse.urlsplit(url).path)}"
        data = None if body is None else json.dumps(body).encode()
        headers = {**self.headers, **(headers or {})}
        if data is not None:
            headers["Content-Type"] = "application/json"
        for attempt in range(self.attempts):
            last = attempt == self.attempts - 1
            self.calls += 1
            try:
                request = urllib.request.Request(url, data=data, method=method, headers=headers)
                with self.opener.open(request, timeout=self.timeout) as response:
                    payload = response.read()
                    if raw:
                        return payload, response.headers
                    return (json.loads(payload) if payload.strip() else None), response.headers
            except urllib.error.HTTPError as exc:
                retryable = self._rate_limited(exc.code, exc.headers) or exc.code >= 500
                if retryable and not last:
                    self.sleep(self._wait(attempt, exc.headers))
                    continue
                kind = ("rate limited" if self._rate_limited(exc.code, exc.headers)
                        else {401: "unauthorized (credential missing, expired or revoked)",
                              403: "forbidden (credential lacks permission)",
                              404: "not found (or not visible to this credential)"}.get(exc.code, "failed"))
                raise ApiError(f"{label}: HTTP {exc.code} {kind}", exc.code, transient=retryable) from None
            except (socket.timeout, TimeoutError):
                if not last:
                    self.sleep(self._wait(attempt, None))
                    continue
                raise ApiError(f"{label}: timed out after {self.attempts} attempts", transient=True) from None
            except urllib.error.URLError as exc:
                if not last:
                    self.sleep(self._wait(attempt, None))
                    continue
                raise ApiError(f"{label}: unreachable ({type(exc.reason).__name__})", transient=True) from None
            except json.JSONDecodeError:
                raise ApiError(f"{label}: response is not JSON") from None
        raise ApiError(f"{label}: unreachable", transient=True)

    def get(self, path: str, **params):
        return self.request("GET", path, params=params or None)[0]

    def paginate(self, path: str, params: dict | None = None, limit: int = 2000) -> list:
        """Follow GitHub `Link: rel="next"` and GitLab `X-Next-Page` pagination."""
        params = {"per_page": 100, **(params or {})}
        items: list = []
        url, query = path, params
        while url and len(items) < limit:
            page, headers = self.request("GET", url, params=query)
            if not isinstance(page, list):
                raise ApiError(f"GET {redact(urllib.parse.urlsplit(self._url(path, None)).path)}: expected a list")
            items += page
            link = headers.get("Link") or ""
            nxt = re.search(r'<([^>]+)>;\s*rel="next"', link)
            if nxt:
                # Credentials are sent to the next URL: it must stay on the API host.
                if urllib.parse.urlsplit(nxt.group(1)).netloc != urllib.parse.urlsplit(self.base).netloc:
                    raise ApiError("pagination link points to another host; refusing to follow")
                url, query = nxt.group(1), None
            elif headers.get("X-Next-Page"):
                url, query = path, {**params, "page": headers["X-Next-Page"]}
            else:
                url = None
        return items[:limit]
