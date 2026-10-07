# Cherami Python SDK

The official Python client for [Cherami](https://cherami.to), email infrastructure for AI agents. Create inboxes for ongoing work, read incoming correspondence, and send messages from your application.

Python 3.11+, with synchronous and asynchronous clients and typed dictionaries.

## Install and connect

Install from PyPI:

```sh
pip install cherami
```

Or, with uv:

```sh
uv add cherami
```

[Get an API key](https://cherami.to/docs/quickstart) and set `CHERAMI_API_KEY` in your application's environment. Keep it private: it grants access to all inboxes on your account.

```python
import os
from cherami import Cherami

with Cherami(os.environ["CHERAMI_API_KEY"]) as client:
    for inbox in client.list_inboxes().data["inboxes"]:
        print(inbox["id"], inbox["address"])
```

Choose an inbox and set `CHERAMI_INBOX_ID` to its ID for the examples below.

Methods accept dictionaries and return a response envelope. `.data` contains the result; `.status`, `.headers`, and `.request_id` expose HTTP response information. Path and query parameters go at the top level of the input dictionary; JSON request fields go in `body`.

## Read mail

For repeated checks, see [webhooks and polling](https://cherami.to/docs/troubleshooting#does-cherami-provide-webhooks) and the [receiving guide](https://cherami.to/docs/guides/receiving). They cover bounded runs, pagination, unfinished content and handled-message tracking.

List messages, then fetch their content:

```python
with Cherami(os.environ["CHERAMI_API_KEY"]) as client:
    page = client.list_messages({
        "inbox_id": os.environ["CHERAMI_INBOX_ID"], "limit": 20,
    }).data
    for message in page["messages"]:
        detail = client.get_message({"message_id": message["id"]}).data
        if detail["processing_status"] == "ready":
            print(detail["content"]["text"])
        else:
            print(detail["id"], detail["processing_status"])
```

Content is available when processing is `ready`. Run this example somewhere private because it prints email bodies.

### Async and pagination

`AsyncCherami` has the same methods and response types. Use `iterate` to read across pages without managing cursors yourself:

```python
import asyncio
from cherami import AsyncCherami

async def main():
    async with AsyncCherami(os.environ["CHERAMI_API_KEY"]) as client:
        async for message in client.iterate("list_messages", {
            "inbox_id": os.environ["CHERAMI_INBOX_ID"], "limit": 20,
        }, max_pages=5):
            detail = (await client.get_message({"message_id": message["id"]})).data
            if detail["processing_status"] == "ready":
                print(detail["content"]["text"])
            else:
                print(detail["id"], detail["processing_status"])

asyncio.run(main())
```

In an existing event loop, use `await main()`. Sync clients support the same iterator with ordinary `for`. `iterate` yields items; `pages` yields response envelopes. Both fetch lazily. Set `max_pages` to bound requests; otherwise they follow all pages.

Context managers close connections. For a long-lived client, call `close()` or `await aclose()` when your application shuts down.

## Send and recover

The SDK makes no automatic retries. Its send helper separates preparing a message from submitting it so your application can save the original request before sending and, if the response is lost, recover with the same retry key instead of sending twice.

Replace the example recipient, then prepare the message:

```python
from cherami import prepare_send

intent = prepare_send("send_message", {
    "inbox_id": os.environ["CHERAMI_INBOX_ID"],
    "body": {
        "to": [{"address": "recipient@example.com", "name": "Alex"}],
        "subject": "Review ready",
        "text": "The change is ready for review.",
    },
})
saved_json = intent.to_json()
```

**Persist `saved_json` in your application's database or a private file before submitting.** It contains the message, retry key and preparation time, but not your API key. The [runnable reply examples](examples/README.md#prepare-an-approved-reply) show a complete file-based workflow, including receipt storage.

For both initial submission and recovery, load that saved JSON and restore the same intent:

```python
from cherami import restore_send

# saved_json must come from the record persisted before the first submission.
saved = restore_send(saved_json)
with Cherami(os.environ["CHERAMI_API_KEY"]) as client:
    result = client.submit(saved)
    receipt = {
        "data": result.data,
        "status": result.status,
        "request_id": result.request_id,
    }
    # Persist this receipt without replacing earlier receipts for the intent.
```

Read `result.data["message"]["status"]` to distinguish the outcome:

| Outcome | Meaning |
| --- | --- |
| `accepted` | The provider accepted submission. This is not proof of delivery. |
| `rejected` | The provider explicitly rejected submission. |
| `unknown` | Submission may have succeeded. Recover using the saved intent. |

These outcomes are data, not exceptions. Preserve every returned receipt: when `outcome_persisted` is false, it may contain an outcome that later reads do not yet show.

The helper refuses submission after **23 hours and 59 minutes from preparation**. After expiry, inspect sent resources instead.

The helper also supports `reply_message`, `reply_all_message`, and `forward_message`. Direct send methods leave retry-key and recovery-window management to your application. Drafts use `send_draft` with separate same-draft protection. See the [sending guide](https://cherami.to/docs/guides/sending) and [draft guide](https://cherami.to/docs/guides/drafts) for those workflows.

## Handle errors

```python
from cherami import CheramiApiError, CheramiTransportError

with Cherami(os.environ["CHERAMI_API_KEY"]) as client:
    try:
        inboxes = client.list_inboxes().data
    except CheramiApiError as error:
        print(error.status, error.code, error.request_id)
    except CheramiTransportError:
        # No usable API response was received.
        raise
```

API errors also expose `.body`, `.headers`, and `.retry_after`. Transport failures raise `CheramiTransportError`; for a write, the request may still have completed, so use the saved-intent workflow above for sends.

Clients use HTTPX with a default 60-second inactivity timeout per network operation. Pass `timeout` to a client or method to change it, or `None` to disable it. Requests do not automatically retry or follow redirects.

## More workflows

The SDK supports inboxes, received and sent mail, replies, forwarding, drafts, labels, conversations, policy inspection and attachment downloads.

- [Runnable examples](examples/README.md): read mail, prepare a reply, and submit or recover it.
- [Python guide](https://cherami.to/docs/python): client configuration, attachments and download handling.
- [HTTP reference](https://cherami.to/docs/api): input fields and response contracts. Named Python types are available from `cherami.models`, including `SendInput`, `SendReceipt`, and operation types such as `ListMessagesParams`.

Inputs and results are ordinary dictionaries with HTTP field names unchanged. Omit optional fields unless you intend to supply them; use `None` only where the API permits null. Types support static checking, not runtime validation.

## Development

```sh
uv sync --locked
bun scripts/generate.mts
uv build
```

Consumers need neither Bun nor the model generator. See [CONTRIBUTING.md](CONTRIBUTING.md) for generation and distribution details. MIT licensed.
