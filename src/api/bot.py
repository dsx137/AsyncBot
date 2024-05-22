from abc import ABC, abstractmethod
from api.db import Db


class Bot:
    def __init__(self, id: str, db: Db) -> None:
        self.id = id
        self.db = db

    @abstractmethod
    async def send_message(
        self,
        target_id: str,
        content: str,
        type: int = 1,
        quote: str = None,
        nonce: str = None,
        temp_target_id: str = None,
    ) -> None:
        pass
