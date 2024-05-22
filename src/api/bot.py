from abc import ABC, abstractmethod


class Bot:
    def __init__(self, id: str) -> None:
        self.id = id

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
