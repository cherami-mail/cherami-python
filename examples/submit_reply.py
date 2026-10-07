"""Submit/recover the unchanged saved intent. Makes one request, never retries."""
import json
import os
from pathlib import Path
from cherami import Cherami, restore_send

intent = restore_send(Path(os.environ["CHERAMI_INTENT_PATH"]).read_text(encoding="utf-8"))
with Cherami(os.environ["CHERAMI_API_KEY"]) as client:
    result = client.submit(intent)
# This line is the attempt's receipt. Keep it; a later replay must not replace an earlier outcome.
print(json.dumps({"data": result.data, "status": result.status, "request_id": result.request_id}))
