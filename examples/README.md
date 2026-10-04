# Run the examples

Use Python 3.11+ and an existing [human-approved API key](https://cherami.to/docs/quickstart). No MCP connection is required. The scripts operate only when you run them; none starts a background poller.

From this SDK checkout, install it and its development environment with `uv sync --locked`. Run the commands below from this directory's parent with `uv run python examples/…`. Applications can install the published package with `pip install cherami` or `uv add cherami`.

## Read correspondence

Supply `CHERAMI_API_KEY` privately through your environment. Do not put its value in commands, source, chat, or logs.

```sh
uv run python examples/read_inbox.py
```

Without `CHERAMI_INBOX_ID`, this lists available inbox IDs and addresses, then stops. Choose the inbox assigned to your application, set that ID, and run again. The example reads one page of 20 messages and prints prepared message text. Run in a private terminal: the text may contain confidential or hostile material. It does not label messages or treat reading as approval to act.

For async applications, the equivalent is:

```sh
uv run python examples/read_inbox_async.py
```

That version requires the inbox ID and prints original plaintext. Both leave unfinished message preparation visible rather than pretending the message is empty.

## Prepare an approved reply

Inspect the chosen message's From and Reply-To, and confirm the recipient and reply content before continuing. `reply_message` derives recipients from the source; use an explicitly addressed `send_message` intent instead when you need to override them.

Set `CHERAMI_INBOX_ID`, `CHERAMI_MESSAGE_ID` (the Cherami message ID, not an RFC Message-ID), and `CHERAMI_REPLY_TEXT`. Set `CHERAMI_INTENT_PATH` to a new absolute filename in an existing private directory outside your repository.

```sh
uv run python examples/prepare_reply.py
```

This saves the payload, original key and preparation time with private permissions and exclusive creation. It sends nothing and requires no API key. Use a separate record for each intended reply. Keep the saved file unchanged; do not rerun this command to recover an uncertain send.

## Submit or recover that reply

Set `CHERAMI_RECEIPT_DIR` to an existing absolute private directory and retain `CHERAMI_INTENT_PATH` and `CHERAMI_API_KEY`.

```sh
uv run python examples/submit_reply.py
```

Initial submission and recovery use this same command and original record. Each run makes exactly one request, saving `{data, status, request_id}` in a new private receipt file before printing the message ID, outcome and persistence flag. An empty/partial receipt file means recording failed, not that sending failed. Preserve every complete receipt.

`accepted` is provider acceptance, not delivery; `rejected` is explicit provider rejection; `unknown` leaves submission uncertain. If `outcome_persisted` is false, preserve the immediate result even if later reads lag. The helper refuses submission after 23 hours and 59 minutes from preparation. Do not replace the key or reprepare an uncertain send after expiry; inspect sent resources. Recovery never resumes provider submission.

See the [sending guide](https://cherami.to/docs/guides/sending) for the complete contract.
