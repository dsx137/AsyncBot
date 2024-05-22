import aiohttp
import asyncio
import json
import websockets
import logging
import zlib

import api.event as event
import api.events as events
import traceback
import bot.kook as kook
from logger import logger
from api.db import Db


class Handler:
    def __init__(self, bus: event.Bus, db: Db):
        logger.info("Registering events...")
        self.db = db
        bus.subscribe(events.RecivedMessage, self.on_recived_message)

    async def on_recived_message(self, e: events.RecivedMessage):
        if e.bot.id != e.author_id and e.bot.id in e.mention:
            self.db.insert("main", {"content": e.content})
            data = self.db.select("main")
            content = "hi"
            await e.bot.send_message(
                target_id=e.channel_id,
                content=content,
                type=9,
            )
