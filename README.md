# Cherami Python SDK

The official Python client for [Cherami](https://cherami.to), email infrastructure for AI agents. Create inboxes for your agents, read the mail that arrives and send from their addresses.

Python 3.11+, with synchronous and asynchronous clients and typed dictionaries.

## Install and connect

```sh
pip install cherami
# or
uv add cherami
```

[Create an API key](https://cherami.to/docs/quickstart#create-an-api-key) and supply it privately as `CHERAMI_API_KEY`. Then list your inboxes:

```python
import os
from cherami import Cherami

with Cherami(os.environ["CHERAMI_API_KEY"]) as client:
    for inbox in client.list_inboxes().data["inboxes"]:
        print(inbox["id"], inbox["address"])
```

This prints every inbox on your account. Set `CHERAMI_INBOX_ID` to the one you want to work with; the examples below use it. If the list is empty, [create an inbox](https://cherami.to/docs/api/inboxes/create-inbox) with `create_inbox`.

Methods take a dictionary and return a response envelope: `.data` holds the result, and `.status`, `.headers` and `.request_id` the HTTP details. Path and query parameters go at the top level of the dictionary, and JSON request fields go in `body`. Field names match the HTTP API. Leave out optional fields you don't need, and pass `None` only where the API accepts null.

## Read mail

List recent messages, then fetch each one. Its content is available once `processing_status` is `ready`:

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

To act on mail as it arrives, [add a webhook](https://cherami.to/docs/guides/webhooks), or poll as [Receive and poll for mail](https://cherami.to/docs/guides/receiving) describes.

### Async and pagination

`AsyncCherami` has the same methods and response types. `iterate` reads across pages without you managing cursors:

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

The sync client iterates the same way with a plain `for`. `iterate` yields items and `pages` yields response envelopes; both fetch only as you consume them. Set `max_pages` to cap requests; otherwise they follow every page.

For a long-lived client outside a `with` block, call `close()`, or `await aclose()`, when your application shuts down.

## Send and recover

Prepare each email once and save the record before you submit it.

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
record = intent.to_json()
# Save record here.
```

Submit the saved record:

```python
from cherami import restore_send

saved = restore_send(record)  # the record you saved
with Cherami(os.environ["CHERAMI_API_KEY"]) as client:
    receipt = client.submit(saved).data
print(receipt["message"]["id"], receipt["message"]["status"], receipt["outcome_persisted"])
```

If `submit` raises `CheramiTransportError`, the response was lost: submit the same saved record again. It carries the original retry key, so we return the first attempt instead of sending a second email.

`receipt["message"]["status"]` tells you what happened:

| Outcome | Meaning |
| --- | --- |
| `accepted` | The email provider accepted the message. This does not confirm delivery. |
| `rejected` | The provider refused it, and `receipt["message"]["error_code"]` says why. Fix that and prepare a new record to send it again. |
| `unknown` | We couldn't confirm whether it went out. Preparing it again could send a duplicate. |

All three arrive as data, not exceptions. If `outcome_persisted` is false, keep this receipt: later reads may not show its outcome.

`submit` accepts a record for **23 hours and 59 minutes after preparation**, then raises `SendRecoveryExpiredError`. After that, check `list_sent_messages`: if the email isn't there, prepare it again.

`prepare_send` also takes `reply_message`, `reply_all_message` and `forward_message`. If you call those methods or `send_message` directly, supply your own `idempotency_key` and save the request before sending: resending it unchanged within 24 hours returns the first attempt instead of sending again. Drafts send with `send_draft` and recover by sending the same draft ID again. See the [sending guide](https://cherami.to/docs/guides/sending) and [draft guide](https://cherami.to/docs/guides/drafts) for those workflows.

## Handle errors

```python
from cherami import CheramiApiError

with Cherami(os.environ["CHERAMI_API_KEY"]) as client:
    try:
        inboxes = client.list_inboxes().data
    except CheramiApiError as error:
        print(error.status, error.code, error.request_id)
```

API errors also expose `.body`, `.headers` and `.retry_after`. `CheramiTransportError` means no usable response arrived; for a send, submit the same saved record again.

Each network operation times out after 60 seconds of inactivity by default. Pass `timeout` to a client or method to change it, or `None` to disable it. The client never retries a request or follows a redirect.

## More workflows

The SDK also covers sent mail, replies, forwarding, drafts, labels, conversations, Trash and restore, policy inspection and attachment downloads.

- [Runnable examples](https://github.com/cherami-mail/cherami-python/blob/main/examples/README.md): read mail, prepare a reply, and submit or recover it.
- [Python guide](https://cherami.to/docs/python): client configuration, attachments and downloads.
- [HTTP reference](https://cherami.to/docs/api): every operation's fields and responses.

Named types such as `SendInput`, `SendReceipt` and `ListMessagesParams` are in `cherami.models` for type checking.

For help, [contact support](https://cherami.to/support).

## Development

You don't need Bun or the model generator to use the package. See [CONTRIBUTING.md](https://github.com/cherami-mail/cherami-python/blob/main/CONTRIBUTING.md) for generation and distribution details.

MIT licensed.
