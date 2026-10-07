# Run the examples

Use Python 3.11+ and an existing [API key](https://cherami.to/docs/quickstart#create-an-api-key). The scripts operate only when you run them; none starts a background poller.

From this SDK checkout, install it and its development environment with `uv sync --locked`. Run the commands below from this directory's parent with `uv run python examples/…`. Applications can install the published package with `pip install cherami` or `uv add cherami`.

## Read correspondence

Supply `CHERAMI_API_KEY` privately through your environment.

```sh
uv run python examples/read_inbox.py
```

Without `CHERAMI_INBOX_ID`, this lists available inbox IDs and addresses, then stops. Set the ID of the inbox assigned to your application and run again. The example reads one page of 20 messages and prints prepared message text. It does not label messages.

For async applications, the equivalent is:

```sh
uv run python examples/read_inbox_async.py
```

That version requires the inbox ID and prints original plaintext. Both show unfinished message preparation as its processing status.

## Prepare an approved reply

Confirm the recipient and reply content before continuing. `reply_message` derives recipients from the source's Reply-To or From; use an explicitly addressed `send_message` intent instead when you need to override them.

Set `CHERAMI_INBOX_ID`, `CHERAMI_MESSAGE_ID` (the Cherami message ID, not an RFC Message-ID), and `CHERAMI_REPLY_TEXT`. Set `CHERAMI_INTENT_PATH` to where the send record is saved, a new file for each intended reply.

```sh
uv run python examples/prepare_reply.py
```

This saves the payload, original key and preparation time. It sends nothing and requires no API key. Keep the saved file unchanged for recovery.

## Submit or recover that reply

Keep `CHERAMI_INTENT_PATH` and `CHERAMI_API_KEY` set.

```sh
uv run python examples/submit_reply.py
```

Initial submission and recovery use this same command and original record. Each run makes exactly one request and prints the receipt as one JSON line, `{data, status, request_id}`, carrying the message ID, outcome and persistence flag. Preserve every receipt.

`accepted` is provider acceptance, not delivery; `rejected` is explicit provider rejection; `unknown` leaves submission uncertain. If `outcome_persisted` is false, preserve the immediate result even if later reads lag. The helper refuses submission after 23 hours and 59 minutes from preparation; after expiry, inspect sent resources instead.

See the [sending guide](https://cherami.to/docs/guides/sending) for the complete contract.
