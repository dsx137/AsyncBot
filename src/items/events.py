import api.event as event
from api.bot import Bot


class RecivedMessage(event.Event):
    def __init__(
        self,
        bot: Bot,
        content: str,
        channel_id: str,
        mention: list,
        author_id: str,
        msg_id: str,
    ) -> None:
        self.bot = bot
        self.content = content
        self.channel_id = channel_id
        self.mention = mention
        self.author_id = author_id
        self.msg_id = msg_id


class ButtonClicked(event.Event):
    def __init__(
        self,
        bot: Bot,
        msg_id: str,
        user_id: str,
        value: str,
        targer_id: str,
    ) -> None:
        self.bot = bot
        self.msg_id = msg_id
        self.user_id = user_id
        self.value = value
        self.targer_id = targer_id
