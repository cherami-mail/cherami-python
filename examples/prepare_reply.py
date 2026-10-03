"""Save an approved reply once. No network request or credential is needed."""
import os
from pathlib import Path
from cherami import prepare_send

path = Path(os.environ["CHERAMI_INTENT_PATH"])
if not path.is_absolute():
    raise ValueError("CHERAMI_INTENT_PATH must be an absolute private filename.")
intent = prepare_send("reply_message", {
    "inbox_id": os.environ["CHERAMI_INBOX_ID"],
    "body": {"message_id": os.environ["CHERAMI_MESSAGE_ID"], "text": os.environ["CHERAMI_REPLY_TEXT"]},
})
# Exclusive creation avoids replacing a prior intent. A partial write is not a
# usable record: do not submit until this command has completed successfully.
with os.fdopen(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "w", encoding="utf-8") as file:
    file.write(intent.to_json())
    file.flush()
    os.fsync(file.fileno())
print("Saved reply. Use submit_reply.py for initial submission or recovery.")
