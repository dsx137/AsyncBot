import api.event as event
from api.bot import Bot


class RecivedMessage(event.Event):
    def __init__(
        self, bot: Bot, content: str, channel_id: str, mention: list, author_id: str
    ):
        self.bot = bot
        self.content = content
        self.mention = mention
        self.channel_id = channel_id
        self.author_id = author_id
