"""Async reading uses the same models and lazy pagination, without blocking I/O."""
import asyncio
import os
from cherami import AsyncCherami


async def main() -> None:
    async with AsyncCherami(os.environ["CHERAMI_API_KEY"]) as client:
        async for message in client.iterate("list_messages", {
            "inbox_id": os.environ["CHERAMI_INBOX_ID"], "limit": 20,
        }, max_pages=1):
            detail = (await client.get_message({"message_id": message["id"]})).data
            print(detail["id"], detail["processing_status"])
            if detail["processing_status"] == "ready":
                print(detail["content"]["text"])


if __name__ == "__main__":
    asyncio.run(main())
