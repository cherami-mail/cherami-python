"""Original-byte helpers; no document extraction or automatic file opening."""
import base64
import binascii
import re
from collections.abc import Mapping

from .models import AttachmentInput


def attachment(filename: str, content: bytes | bytearray | memoryview, content_type: str = "application/octet-stream") -> AttachmentInput:
    """Encode original bytes for body.attachments in a send or draft."""
    if not isinstance(content, (bytes, bytearray, memoryview)):
        raise TypeError("Supply original bytes; encode text explicitly before attaching it.")
    return {"filename": filename, "type": content_type, "content": base64.b64encode(content).decode("ascii")}


def attachment_bytes(file: Mapping[str, object]) -> bytes:
    """Decode saved draft/sent attachment content, failing on invalid base64."""
    content = file.get("content")
    if not isinstance(content, str) or not re.fullmatch(r"(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?", content):
        raise ValueError("Attachment content must be padded base64 without whitespace.")
    try:
        return base64.b64decode(content, validate=True)
    except binascii.Error as cause:
        raise ValueError("Invalid attachment base64.") from cause
