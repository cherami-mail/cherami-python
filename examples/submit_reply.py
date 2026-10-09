"""Send the reply saved at CHERAMI_INTENT_PATH. If it fails with CheramiTransportError,
run this again with the same file, not prepare_reply.py: the saved retry key returns the
original attempt instead of sending twice."""
import json
import os
from pathlib import Path
from cherami import Cherami, restore_send

intent = restore_send(Path(os.environ["CHERAMI_INTENT_PATH"]).read_text(encoding="utf-8"))
with Cherami(os.environ["CHERAMI_API_KEY"]) as client:
    result = client.submit(intent)
# The receipt. If data["outcome_persisted"] is false, keep it: later reads may not show its outcome.
print(json.dumps({"data": result.data, "status": result.status, "request_id": result.request_id}))
