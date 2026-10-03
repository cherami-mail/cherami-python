"""Privately persist intended sends before submission, without renewing replay time."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
import json
import re
from typing import Any, Literal, overload
from uuid import uuid4

from . import models

SendOperation = Literal["send_message", "reply_message", "reply_all_message", "forward_message"]
_SEND_OPERATIONS = {"send_message", "reply_message", "reply_all_message", "forward_message"}


class SendRecoveryExpiredError(Exception):
    def __init__(self):
        super().__init__("The conservative send-recovery window has expired. Inspect sent resources; do not replace the key or prepare this uncertain send again.")


@dataclass(frozen=True)
class PreparedSend:
    """Immutable JSON snapshot. Inspection returns copies, never editable send intent.

    Use prepare_send or restore_send, not this constructor. The record contains mail
    content, so repr deliberately omits it. Persist to_json() before calling submit.
    """
    _json: str = field(repr=False)

    def to_json(self) -> str:
        return self._json

    @property
    def operation(self) -> SendOperation:
        return json.loads(self._json)["operation"]

    @property
    def first_request_at(self) -> str:
        return json.loads(self._json)["first_request_at"]

    @property
    def params(self) -> dict[str, Any]:
        return json.loads(self._json)["params"]


@overload
def prepare_send(operation: Literal["send_message"], params: models.SendMessageParams) -> PreparedSend: ...
@overload
def prepare_send(operation: Literal["reply_message"], params: models.ReplyMessageParams) -> PreparedSend: ...
@overload
def prepare_send(operation: Literal["reply_all_message"], params: models.ReplyAllMessageParams) -> PreparedSend: ...
@overload
def prepare_send(operation: Literal["forward_message"], params: models.ForwardMessageParams) -> PreparedSend: ...


def prepare_send(operation: SendOperation, params: Any) -> PreparedSend:
    """Snapshot an approved intent; generate a key only when none was supplied."""
    if operation not in _SEND_OPERATIONS or not isinstance(params, dict) or not isinstance(params.get("body"), dict):
        raise ValueError("Supply a supported send operation and parameter dictionary with body.")
    # JSON also rejects bytes, non-finite numbers and other non-wire objects before
    # any request. The encoded snapshot cannot be changed by a caller's mutation.
    body = dict(params["body"])
    if "idempotency_key" not in body:
        body["idempotency_key"] = str(uuid4())
    return restore_send(json.dumps({
        "version": 1,
        "operation": operation,
        "first_request_at": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        "params": {**params, "body": body},
    }, allow_nan=False, ensure_ascii=False))


def _reject_constant(value: str) -> Any:
    raise ValueError(f"Non-JSON number: {value}")


def restore_send(saved: str) -> PreparedSend:
    """Load the unchanged saved record. Never generate a key or reset its time."""
    try:
        record = json.loads(saved, parse_constant=_reject_constant)
        if not isinstance(record, dict) or type(record.get("version")) is not int or record["version"] != 1:
            raise ValueError()
        if record.get("operation") not in _SEND_OPERATIONS:
            raise ValueError()
        stamp = record.get("first_request_at")
        if not isinstance(stamp, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z", stamp):
            raise ValueError()
        datetime.fromisoformat(stamp)
        params = record["params"]
        if not isinstance(params, dict) or not isinstance(params.get("inbox_id"), str) or not params["inbox_id"]:
            raise ValueError()
        body = params["body"]
        if not isinstance(body, dict) or not isinstance(body.get("idempotency_key"), str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", body["idempotency_key"]):
            raise ValueError()
    except (ValueError, TypeError, KeyError) as cause:
        raise ValueError("Invalid send recovery record. Load the unchanged original record, not reconstructed input.") from cause
    return PreparedSend(json.dumps(record, ensure_ascii=False, allow_nan=False))


def check_send_window(record: PreparedSend) -> None:
    age = datetime.now(timezone.utc) - datetime.fromisoformat(record.first_request_at)
    if age < timedelta(0):
        raise ValueError("Send recovery timestamp is in the future. Check the system clock; do not reset the record.")
    # Preparation deliberately precedes reservation. Delayed submission shortens
    # the server's 24h protection; replay never resumes provider submission.
    if age >= timedelta(hours=24, minutes=-1):
        raise SendRecoveryExpiredError()
