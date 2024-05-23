import aiohttp
import asyncio
import json
import websockets
import logging
import zlib

import api.event as event
import items.events as events
import items.commands as commands
import api.command as command
import traceback
import bot.kook as kook
from logger import logger
from api.db import Db
import api.context as context


class Handler:
    def __init__(self):
        logger.info("Registering events...")
        context.program.bus.subscribe(events.RecivedMessage, self.on_recived_message)

    async def on_recived_message(self, e: events.RecivedMessage):
        if e.bot.id != e.author_id and e.bot.id in e.mention:
            params = e.content.replace(f"(met){e.bot.id}(met)", "").strip().split(" ")
            commands.root.execute(
                c=command.ContextExecute(
                    params=params,
                    bot=e.bot,
                    content=e.content,
                    channel_id=e.channel_id,
                    mention=e.mention,
                    author_id=e.author_id,
                    msg_id=e.msg_id,
                ),
            )
