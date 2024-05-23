import api.event as event
import items.events as events
import items.commands as commands
import api.command as command
import traceback
import bot.kook as kook
from logger import logger
from api.db import Db
import api.context as context


def init_handlers():
    @context.program.bus.subscribe(events.RecivedMessage)
    async def on_recived_message(e: events.RecivedMessage):
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
