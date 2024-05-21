import aiohttp
import asyncio
import json
import kook
from logger import logger
import event
import handler
import os

token = os.environ.get("KOOK_TOKEN")


async def main():
    global token
    if not token:
        logger.error("Kook token is missing")
        token = input("Enter your kook token: ")
    client = kook.Client(token=token)
    handler.register_events(client)
    task = asyncio.create_task(client.connect())
    done, pending = await asyncio.wait({task})


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
