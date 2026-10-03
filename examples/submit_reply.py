"""Submit/recover the unchanged saved intent. Makes one request, never retries."""
import json
import os
from pathlib import Path
from uuid import uuid4
from cherami import Cherami, restore_send

intent_path = Path(os.environ["CHERAMI_INTENT_PATH"])
receipt_dir = Path(os.environ["CHERAMI_RECEIPT_DIR"])
if not intent_path.is_absolute() or not receipt_dir.is_absolute() or not receipt_dir.is_dir():
    raise ValueError("Use an absolute intent filename and existing private receipt directory.")
intent = restore_send(intent_path.read_text(encoding="utf-8"))
with Cherami(os.environ["CHERAMI_API_KEY"]) as client:
    # Open the destination before any send. Every response gets its own receipt;
    # a later unknown replay must not overwrite earlier provider acceptance.
    path = receipt_dir / f"receipt-{uuid4()}.json"
    with os.fdopen(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "w", encoding="utf-8") as file:
        result = client.submit(intent)
        json.dump({"data": result.data, "status": result.status, "request_id": result.request_id}, file)
        file.flush()
        os.fsync(file.fileno())
        print(result.data["message"]["id"], result.data["message"]["status"], result.data["outcome_persisted"])
# File-write failure does not undo a send. Empty/partial files are not receipts.
