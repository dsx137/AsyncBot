import aiohttp
import asyncio
import json
import websockets
import logging
import zlib

from logger import logger
import event
import traceback
import kook


def register_events(client: kook.Client):
    logger.info("Registering events...")
    client.bus.subscribe(kook.Events.DELETED_MESSAGE, on_delete_message)
    client.bus.subscribe(kook.Events.KMARKDOWN_MESSAGE, on_kmarkdown_message)


async def on_delete_message(publisher: kook.Client, data):
    logger.info("hello")
    logger.info(data),


async def on_kmarkdown_message(publisher: kook.Client, data):
    id = await publisher.get_me_id()
    extra = data["extra"]
    author = extra["author"]
    mention = extra["mention"]
    if id != author["id"] and id in mention:
        await publisher.send_message(
            target_id=data["target_id"],
            content="Hello, World!",
            type=1,
        )
