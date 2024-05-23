import asyncio
import api.event as event
import items.events as events
from typing import TypeVar, Type, Callable, List, Generic
from abc import ABC, abstractmethod
import api.context as context
from api.bot import Bot


class ContextExecute(context.Context):
    def __init__(
        self,
        params: List[str],
        bot: Bot,
        content: str,
        channel_id: str,
        mention: list,
        author_id: str,
        msg_id: str,
    ) -> None:
        self.params = params
        self.bot = bot
        self.content = content
        self.channel_id = channel_id
        self.mention = mention
        self.author_id = author_id
        self.msg_id = msg_id


class Section:
    def __init__(self, name: str = None) -> None:
        self.name = name
        self._parent: Section = None
        self._children: List[Section] = []
        self._usage_supplier: Callable[[None], str] = None
        self._executor: Callable[[ContextExecute], None] = lambda c: c.bot.send_message(
            target_id=c.channel_id, content=self._usage_supplier(c), type=1
        )

        self._permission = None

    def append(self, child: "Section") -> "Section":
        child._parent = self
        self._children.append(child)
        return self

    def permission(self, permission: str) -> "Section":
        self._permission = permission
        return self

    def executor(self, executor: Callable[[ContextExecute], None]) -> "Section":
        self._executor = executor
        return self

    def usage_supplier(self, usage_supplier: Callable[[None], str]) -> "Section":
        self._usage_supplier = usage_supplier
        return self

    def _get_usage(self, c):
        if self._usage_supplier:
            return self._usage_supplier(c)
        if self._parent:
            return self._parent._get_usage(c)
        return "[default] wrong usage"

    def execute(self, c: ContextExecute) -> None:
        section = self
        for param in c.params:
            matchedSection = None
            for child in section._children:
                if child.name == param or not child.name:
                    matchedSection = child
                    break
            if not matchedSection:

                asyncio.create_task(
                    (
                        c.bot.send_message(
                            target_id=c.channel_id,
                            content=section._get_usage(c),
                            type=9,
                        )
                    )
                )
                return
            else:
                section = matchedSection
        asyncio.create_task(section._executor(c))
