"""Connection lifetime and lazy pagination over shared wire/recovery policies."""
from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from copy import deepcopy
from typing import Any, Self

import httpx

from . import models
from ._routes import PAGE_FIELDS, ROUTES
from ._transport import (
    ApiResponse, DEFAULT_TIMEOUT, Route, Timeout, WirePolicy,
    decode_response, envelope, is_download, transport_error,
)
from .recovery import PreparedSend, check_send_window, restore_send


def _pagination(operation: str, params: Any, max_pages: int | None) -> tuple[dict[str, Any], str | None, set[str]]:
    if operation not in PAGE_FIELDS:
        raise ValueError("Operation is not paginated.")
    if max_pages is not None and (type(max_pages) is not int or max_pages < 1):
        raise ValueError("max_pages must be a positive integer or None.")
    if not isinstance(params, dict):
        raise TypeError("Supply a parameter dictionary.")
    # This runs when the iterator is obtained, not on its first advancement.
    # Caller mutations during a pause cannot change the query's meaning.
    snapshot = deepcopy(params)
    cursor = snapshot.get("cursor")
    if cursor is not None and (not isinstance(cursor, str) or not cursor):
        raise ValueError("Invalid pagination cursor.")
    return snapshot, cursor, {cursor} if cursor else set()


def _next_page(result: ApiResponse[Any], seen: set[str]) -> str | None:
    if "next_cursor" not in result.data:
        raise ValueError("Missing pagination cursor; inspect the response before restarting.")
    cursor = result.data["next_cursor"]
    if cursor is not None:
        if not isinstance(cursor, str) or not cursor or cursor in seen:
            raise ValueError("Invalid or repeated pagination cursor; inspect the response before restarting.")
        seen.add(cursor)
    return cursor


def _items(result: ApiResponse[Any], operation: str) -> list[Any]:
    items = result.data.get(PAGE_FIELDS[operation])
    if not isinstance(items, list):
        raise ValueError("Invalid paginated collection in Cherami response.")
    return items


def _intent(prepared: PreparedSend) -> PreparedSend:
    # Even direct construction of PreparedSend cannot bypass record validation.
    record = restore_send(prepared.to_json())
    check_send_window(record)
    return record


class SyncClient:
    def __init__(self, api_key: str, *, base_url: str = "https://cherami.to", timeout: float | None = 60.0, transport: httpx.BaseTransport | None = None):
        """Use an existing approved key. Custom transports must not retry writes.

        timeout is HTTPX's per-operation inactivity timeout, in seconds; None
        disables it. Environment proxies and implicit redirects are disabled.
        """
        self._wire = WirePolicy(api_key, base_url, timeout)
        self._http = httpx.Client(follow_redirects=False, trust_env=False, transport=transport)

    def __enter__(self) -> Self:
        self._http.__enter__()
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def close(self) -> None:
        self._http.close()

    def _request(self, route: Route, params: Any, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[Any]:
        request = self._http.build_request(**self._wire.request_parts(route, params, timeout))
        response = None
        download = False
        try:
            # One request only. Always stream initially so binary bodies belong to
            # the caller; JSON/error bodies are consumed and closed here instead.
            response = self._http.send(request, stream=True, follow_redirects=False)
            download = is_download(route, response)
            if download:
                return envelope(response, response)
            response.read()
            return decode_response(route, response)
        except httpx.HTTPError as cause:
            raise transport_error(response) from cause
        finally:
            if response is not None and not download:
                response.close()

    def submit(self, prepared: PreparedSend, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.SendReceipt]:
        """Submit/recover a persisted intent once, without extending its window."""
        record = _intent(prepared)
        return self._request(ROUTES[record.operation], record.params, timeout=timeout)

    def _pages(self, operation: str, params: Any, *, max_pages: int | None, timeout: Timeout) -> Iterator[ApiResponse[Any]]:
        snapshot, cursor, seen = _pagination(operation, params, max_pages)

        def generate() -> Iterator[ApiResponse[Any]]:
            nonlocal cursor
            count = 0
            while max_pages is None or count < max_pages:
                query = {**snapshot, **({"cursor": cursor} if cursor is not None else {})}
                result = self._request(ROUTES[operation], query, timeout=timeout)
                cursor = _next_page(result, seen)
                yield result
                count += 1
                if cursor is None:
                    return
        return generate()

    def _iterate(self, operation: str, params: Any, *, max_pages: int | None, timeout: Timeout) -> Iterator[Any]:
        pages = self._pages(operation, params, max_pages=max_pages, timeout=timeout)
        return (item for result in pages for item in _items(result, operation))


class AsyncClient:
    def __init__(self, api_key: str, *, base_url: str = "https://cherami.to", timeout: float | None = 60.0, transport: httpx.AsyncBaseTransport | None = None):
        """Async I/O using the same policies and models as Cherami. No retries."""
        self._wire = WirePolicy(api_key, base_url, timeout)
        self._http = httpx.AsyncClient(follow_redirects=False, trust_env=False, transport=transport)

    async def __aenter__(self) -> Self:
        await self._http.__aenter__()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self._http.aclose()

    async def _request(self, route: Route, params: Any, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[Any]:
        request = self._http.build_request(**self._wire.request_parts(route, params, timeout))
        response = None
        download = False
        try:
            response = await self._http.send(request, stream=True, follow_redirects=False)
            download = is_download(route, response)
            if download:
                return envelope(response, response)
            await response.aread()
            return decode_response(route, response)
        except httpx.HTTPError as cause:
            raise transport_error(response) from cause
        finally:
            if response is not None and not download:
                await response.aclose()
        # Cancellation (including asyncio.CancelledError) deliberately propagates
        # rather than being swallowed or retried. It cannot undo a submitted write.

    async def submit(self, prepared: PreparedSend, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.SendReceipt]:
        record = _intent(prepared)
        return await self._request(ROUTES[record.operation], record.params, timeout=timeout)

    def _pages(self, operation: str, params: Any, *, max_pages: int | None, timeout: Timeout) -> AsyncIterator[ApiResponse[Any]]:
        snapshot, cursor, seen = _pagination(operation, params, max_pages)

        async def generate() -> AsyncIterator[ApiResponse[Any]]:
            nonlocal cursor
            count = 0
            while max_pages is None or count < max_pages:
                query = {**snapshot, **({"cursor": cursor} if cursor is not None else {})}
                result = await self._request(ROUTES[operation], query, timeout=timeout)
                cursor = _next_page(result, seen)
                yield result
                count += 1
                if cursor is None:
                    return
        return generate()

    def _iterate(self, operation: str, params: Any, *, max_pages: int | None, timeout: Timeout) -> AsyncIterator[Any]:
        pages = self._pages(operation, params, max_pages=max_pages, timeout=timeout)

        async def generate() -> AsyncIterator[Any]:
            async for result in pages:
                for item in _items(result, operation):
                    yield item
        return generate()
