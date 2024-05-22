from typing import TypeVar, Type, Callable, List
from abc import ABC, abstractmethod
from handler import Handler
import api.events as events

Node = TypeVar("Node")


class Node:
    def __init__(self, id: str = None, parent: Node = None) -> None:
        self.id = id
        self.parent = parent
        self.children: List[Node] = []

    def append(self, node: Node) -> Node:
        node.parent = self
        self.children.append(node)
        return self

    def route(self, params: list) -> Node:
        for child in self.children:
            if child.id == params[0]:
                return child.route(params[1:])
        return self

    def execute(self, handler: Handler, e: events.RecivedMessage):
        pass

    def usage(self, handler: Handler, e: events.RecivedMessage):
        pass
