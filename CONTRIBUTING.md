# Contributing

For a bug report, include a minimal reproduction, Python and SDK versions, the operation, and a request ID when available. Omit API keys, mail bodies and private attachments. Send security issues or private account questions to hello@cherami.to rather than a public issue.

Use Python 3.11+, uv and Bun. Applications consuming the package need only Python and its runtime dependencies.

```sh
uv sync --locked
bun scripts/generate.mts
```

The selected `openapi.json` and `operations.json` are the generation inputs. Discuss contract changes or new operations with a maintainer before implementing them; behavior must agree with the service's [HTTP reference](https://cherami.to/docs/api). Do not edit `models.py`, `_operations.py` or `_routes.py` directly. The generator produces static `TypedDict` models and method/pagination signatures; it does not add runtime response coercion. A narrow receipt-refinement normalization works around the model generator's conflicting TypedDict inheritance while leaving the public snapshot unchanged.

Keep transport, serialization, errors, pagination and send-recovery policy shared between sync and async clients. Only HTTPX I/O and iterator syntax differ. Preserve omitted versus null values, original file bytes, request IDs and accepted/rejected/unknown outcomes. No automatic retries or redirects. A broken response or cancellation cannot establish that a write was rolled back.

Use focused manual checks with a substituted HTTPX transport for fault paths. Real requests require an appropriately authorized account and workflow; never send mail or mutate an inbox merely to check an example. Do not commit credentials, mail, recovery records or private operation material. The runnable examples explain private file handling and explicit sending.

## Distribution

`uv build` prepares a wheel and source archive in `dist/`. Inspect their contents and consume the wheel in an isolated environment before release. The wheel contains `cherami` source, `py.typed`, license and package metadata, not generation tools or workspace dependencies. The source archive includes everything needed for standalone generation, including `uv.lock`.

Maintainers publish releases manually. Verify that the source archive regenerates independently and that source and package metadata agree. Publish the reviewed artifact rather than rebuilding an unchecked tree; update installation guidance alongside package availability. No registry credential is required for local development.

In a pull request, explain the problem, proposed change and what you checked. Update examples or documentation when usage changes, and distinguish local fixture results from live service behavior.
