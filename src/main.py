import aiohttp
import asyncio
import json
import bot.kook as kook
import api.event as event
import handler
import os
from logger import logger
from api.db import Db

token = os.environ.get("KOOK_TOKEN")
db_path = os.environ.get("DB_PATH")


async def main():
    global token
    global db_path
    if not token:
        logger.error("Kook token is missing")
        token = input("Enter your kook token: ")
    if not db_path:
        logger.error("Db path is missing")
        db_path = "db.sqlite"
    bus = event.Bus()
    db = Db(path=db_path)
    db.create_table("main", ["content TEXT"])
    client = kook.Client(token=token, bus=bus, db=db)
    handler.register_events(bus=bus)
    task = asyncio.create_task(client.connect())
    done, pending = await asyncio.wait({task})


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
