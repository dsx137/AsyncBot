import json
from typing import List, Tuple, TypeVar
from message.kook.card.module import Module


class Card:
    def __init__(self, modules: List[Module] = []):
        self.body = {
            "type": "card",
            "theme": "secondary",
            "size": "lg",
            "modules": [module.body for module in modules],
        }

    def append_module(self, module: Module) -> "Card":
        self.body["modules"].append(module.body)
        return self


class CardList:
    def __init__(self, cards: List[Card] = []):
        self.body = [card.body for card in cards]

    def append_card(self, card: Card) -> "CardList":
        self.body.append(card.body)
        return self

    def to_str(self) -> str:
        return json.dumps(self.body, ensure_ascii=False)
