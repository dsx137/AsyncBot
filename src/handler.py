import aiohttp
import asyncio
import json
import websockets
import logging
import zlib

from logger import logger
import api.event as event
import api.events as events
import traceback
import bot.kook as kook
from logger import logger


def register_events(bus: event.Bus):
    logger.info("Registering events...")
    bus.subscribe(events.RecivedMessage, on_recived_message)


async def on_recived_message(e: events.RecivedMessage):
    if e.bot.id != e.author_id and e.bot.id in e.mention:
        e.bot.db.insert("main", {"content": e.content})
        data = e.bot.db.select("main")
        content = f"""
Hello, World!
你好
Db content:

```json 
{json.dumps(obj=data,indent=4,ensure_ascii=False)}
```
"""
        await e.bot.send_message(
            target_id=e.channel_id,
            content=content,
            type=9,
        )
