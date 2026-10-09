"""Save a reply's send record to CHERAMI_INTENT_PATH without sending it. Run once per reply."""
import os
from pathlib import Path
from cherami import prepare_send

intent = prepare_send("reply_message", {
    "inbox_id": os.environ["CHERAMI_INBOX_ID"],
    "body": {"message_id": os.environ["CHERAMI_MESSAGE_ID"], "text": os.environ["CHERAMI_REPLY_TEXT"]},
})
Path(os.environ["CHERAMI_INTENT_PATH"]).write_text(intent.to_json(), encoding="utf-8")
print("Saved reply. Use submit_reply.py for initial submission or recovery.")
