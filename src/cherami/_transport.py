"""Shared wire policy. Sync and async clients differ only at HTTPX I/O boundaries."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import json
import math
import re
from typing import Any, Generic, TypeVar
from urllib.parse import quote, urlsplit

import httpx

T = TypeVar("T")


class _DefaultTimeout(Enum):
    DEFAULT = "client default"


DEFAULT_TIMEOUT = _DefaultTimeout.DEFAULT
Timeout = float | None | _DefaultTimeout


@dataclass(frozen=True)
class ApiResponse(Generic[T]):
    data: T
    status: int
    headers: httpx.Headers
    request_id: str | None


class CheramiApiError(Exception):
    """HTTP failure, including redirects. Structured error details remain in body."""

    def __init__(self, status: int, headers: httpx.Headers, body: Any):
        error = body.get("error") if isinstance(body, dict) else None
        error = error if isinstance(error, dict) else {}
        super().__init__(error.get("message") or f"Cherami returned HTTP {status}.")
        self.status = status
        self.headers = headers
        self.body = body
        self.code = error.get("code")
        self.request_id = headers.get("x-request-id")
        self.retry_after = headers.get("retry-after")


class CheramiTransportError(Exception):
    """No usable complete response. A write may have happened; never blindly resend."""

    def __init__(self, message: str, *, status: int | None = None, request_id: str | None = None):
        super().__init__(message)
        self.status = status
        self.request_id = request_id


@dataclass(frozen=True)
class Route:
    path: str
    method: str
    path_params: list[str]
    query_params: list[str]
    body: bool
    binary: bool
    success_statuses: list[int]


def check_timeout(timeout: float | None) -> float | None:
    if timeout is not None and (
        isinstance(timeout, bool) or not isinstance(timeout, (int, float))
        or not math.isfinite(timeout) or timeout <= 0
    ):
        raise ValueError("timeout must be a positive number of seconds, or None to disable it.")
    return timeout


class WirePolicy:
    def __init__(self, api_key: str, base_url: str, timeout: float | None):
        if not isinstance(api_key, str) or not api_key or any(c.isspace() for c in api_key) or not api_key.isascii() or any(ord(c) < 33 or ord(c) == 127 for c in api_key):
            raise ValueError("Supply a nonempty ASCII API key without whitespace or control characters.")
        origin = urlsplit(base_url)
        local = origin.hostname in {"localhost", "127.0.0.1", "::1"}
        if (not origin.hostname or origin.username is not None or origin.password is not None
            or origin.path not in {"", "/"} or origin.query or origin.fragment
            or "?" in base_url or "#" in base_url or "\\" in base_url
            or any(c.isspace() or ord(c) < 32 for c in base_url)
            or not (origin.scheme == "https" or (local and origin.scheme == "http"))):
            raise ValueError("base_url must be a trusted HTTPS origin (HTTP is allowed only on loopback).")
        # Accessing port validates malformed ports before any possible credential use.
        origin.port
        self._origin = base_url.rstrip("/")
        self.__api_key = api_key
        self._timeout = check_timeout(timeout)

    def request_parts(self, route: Route, params: Any, timeout: Timeout) -> dict[str, Any]:
        if not isinstance(params, dict):
            raise TypeError("Supply a parameter dictionary.")
        allowed = set(route.path_params + route.query_params) | ({"body"} if route.body else set())
        if set(params) - allowed:
            raise TypeError(f"Unknown parameters: {', '.join(sorted(set(params) - allowed))}")
        path = route.path
        for name in route.path_params:
            value = params.get(name)
            if not isinstance(value, str) or not value or value in {".", ".."} or re.search(r"[\x00-\x20\x7f/\\?#%]", value):
                raise ValueError(f"Invalid {name}: use the returned resource ID.")
            path = path.replace("{" + name + "}", quote(value, safe=""))
        query: list[tuple[str, str]] = []
        for name in route.query_params:
            if name not in params:
                continue
            value = params[name]
            for item in value if isinstance(value, list) else [value]:
                if not isinstance(item, (str, int, float, bool)) or isinstance(item, float) and not math.isfinite(item):
                    raise TypeError(f"Invalid query parameter {name}; omit unused fields rather than passing None.")
                query.append((name, str(item).lower() if isinstance(item, bool) else str(item)))
        headers = {"Authorization": f"Bearer {self.__api_key}", "Accept": "*/*" if route.binary else "application/json"}
        content = None
        if route.body:
            if not isinstance(params.get("body"), dict):
                raise TypeError("Supply a JSON object as body.")
            content = json.dumps(params["body"], ensure_ascii=False, allow_nan=False).encode("utf-8")
            headers["Content-Type"] = "application/json"
        duration = self._timeout if timeout is DEFAULT_TIMEOUT else check_timeout(timeout)
        return {"method": route.method, "url": self._origin + path, "params": query,
                "headers": headers, "content": content, "timeout": duration}


def envelope(response: httpx.Response, data: T) -> ApiResponse[T]:
    return ApiResponse(data, response.status_code, response.headers, response.headers.get("x-request-id"))


def is_download(route: Route, response: httpx.Response) -> bool:
    return route.binary and response.status_code in route.success_statuses


def decode_response(route: Route, response: httpx.Response) -> ApiResponse[Any]:
    """Run only after consuming the body. Never coerce or discard JSON fields."""
    try:
        data = response.json()
    except (ValueError, UnicodeDecodeError):
        data = response.text
    if not response.is_success:
        raise CheramiApiError(response.status_code, response.headers, data)
    if (response.status_code not in route.success_statuses or not isinstance(data, dict)
        or not re.search(r"\bapplication/(?:[\w.-]+\+)?json\b", response.headers.get("content-type", ""), re.I)):
        raise CheramiTransportError(
            "Unexpected Cherami success response. A write may have happened; inspect saved resources before resubmitting.",
            status=response.status_code, request_id=response.headers.get("x-request-id"),
        )
    return envelope(response, data)


def transport_error(response: httpx.Response | None) -> CheramiTransportError:
    return CheramiTransportError(
        "No usable complete Cherami response. A write may have happened; recover the original operation, not a replacement send.",
        status=response.status_code if response is not None else None,
        request_id=response.headers.get("x-request-id") if response is not None else None,
    )
