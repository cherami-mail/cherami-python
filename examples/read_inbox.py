"""Read recent mail. Prints message text: run privately, not in shared logs."""
import os
from cherami import Cherami

with Cherami(os.environ["CHERAMI_API_KEY"]) as client:
    inbox_id = os.environ.get("CHERAMI_INBOX_ID")
    if not inbox_id:
        for inbox in client.list_inboxes().data["inboxes"]:
            print(inbox["id"], inbox["address"])
        raise SystemExit("Choose an assigned inbox and set CHERAMI_INBOX_ID.")
    for message in client.iterate("list_messages", {"inbox_id": inbox_id, "limit": 20}, max_pages=1):
        detail = client.get_message({"message_id": message["id"]}).data
        print(detail["id"], detail["processing_status"])
        if detail["processing_status"] == "ready":
            content = detail["content"]
            # Empty extracted text is meaningful; only None falls back to original.
            text = content["reply_text"] if content["reply_text"] is not None else content["text"]
            print(text if text is not None else "No plain text; inspect original content privately.")
