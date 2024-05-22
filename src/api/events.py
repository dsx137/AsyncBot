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
        super().__init__(**{k: v for k, v in locals().items() if k != "self"})


class ButtonClicked(event.Event):
    def __init__(
        self,
        bot: Bot,
        msg_id: str,
        user_id: str,
        value: str,
        targer_id: str,
    ) -> None:
        super().__init__(**{k: v for k, v in locals().items() if k != "self"})
