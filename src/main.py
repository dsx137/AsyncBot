import asyncio
import bot.kook as kook
from api.event import Bus
import os
from logger import logger
from api.db import Db
import api.context as context
import handler


async def main():
    token = os.environ.get("KOOK_TOKEN")
    db_path = os.environ.get("DB_PATH")
    if not token:
        logger.error("Kook token is missing")
        token = input("Enter your kook token: ")
    if not db_path:
        logger.error("Db path is missing")
        db_path = input("Enter your db path: ")
    context.init_program(bus=Bus(), db=Db(path=db_path))
    handler.init_handlers()
    client = kook.Client(token=token)

    task = asyncio.create_task(client.connect())
    done, pending = await asyncio.wait({task})


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
