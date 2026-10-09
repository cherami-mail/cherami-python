# Run the examples

These scripts read an inbox, then prepare and send a reply, using Python 3.11+. From this SDK checkout, run `uv sync --locked`, then run the commands below from the checkout root.

[Create an API key](https://cherami.to/docs/quickstart#create-an-api-key) and supply it privately as `CHERAMI_API_KEY`.

## Read an inbox

```sh
uv run python examples/read_inbox.py
```

Without `CHERAMI_INBOX_ID`, it lists your inboxes and stops; set the ID of the one you want and run it again. It reads one page of 20 messages and prints each one's text without quoted history, or its processing status if it is not ready yet. It only reads.

For async applications, the equivalent is:

```sh
uv run python examples/read_inbox_async.py
```

This version needs `CHERAMI_INBOX_ID` and prints each message's full text.

## Prepare a reply

Pick a message ID from the read output. The reply goes to that message's Reply-To address, or its From when there is none; to choose recipients yourself, prepare with `send_message` instead, as the [README](../README.md#send-and-recover) shows.

Set `CHERAMI_INBOX_ID`, `CHERAMI_MESSAGE_ID` and `CHERAMI_REPLY_TEXT`, and set `CHERAMI_INTENT_PATH` to the file to save the reply's send record to.

```sh
uv run python examples/prepare_reply.py
```

This saves the reply, its retry key and preparation time to that file. It sends nothing and needs no API key.

## Submit or recover the reply

With the same `CHERAMI_INTENT_PATH`, run the script below. **It sends the reply.**

```sh
uv run python examples/submit_reply.py
```

It prints the receipt as one JSON line, `{data, status, request_id}`. If it fails with `CheramiTransportError`, run **submit** again with the same file, not prepare: we return the original attempt instead of sending twice. After 23 hours and 59 minutes from preparation, submit refuses the record; check sent mail, and if the reply isn't there, prepare it again.

Read the outcome in `data.message.status` and `data.outcome_persisted` as the [README](../README.md#send-and-recover) explains.
