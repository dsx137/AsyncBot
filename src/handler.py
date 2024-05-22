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
        self.db.create_table(
            "candidate",
            {
                "name": "TEXT",
                "url": "TEXT",
                "description": "TEXT",
            },
        )
        bus.subscribe(events.RecivedMessage, self.on_recived_message)

    async def on_recived_message(self, e: events.RecivedMessage):
        reply = lambda content: e.bot.send_message(
            target_id=e.channel_id,
            content=content,
            type=9,
        )

        if e.bot.id != e.author_id and e.bot.id in e.mention:
            params = e.content.replace(f"(met){e.bot.id}(met)", "").strip().split(" ")
            command = params[0]
            if command == "添加待选":
                name = params[1]
                url = params[2]
                description = ",".join(params[3:])
                self.db.insert(
                    "candidate",
                    {
                        "name": name,
                        "url": url,
                        "description": description,
                    },
                )
                await reply("添加成功")
            if command == "查看待选":
                candidates = self.db.select("candidate")
                await reply(
                    "\n".join(
                        [
                            f"{candidate['name']} {candidate['url']} {candidate['description']}"
                            for candidate in candidates
                        ]
                    )
                )
