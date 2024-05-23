import threading
import asyncio
from collections import defaultdict
from functools import wraps
from abc import ABC, abstractmethod
from typing import TypeVar, Type, Callable

E = TypeVar("E", bound="Event")


class Event:
    def __init__(self) -> None:
        pass


class Bus:

    def __init__(self) -> None:
        self._subscribers = defaultdict(list)
        self._lock = threading.Lock()

    def subscribe(self, type: E, subscriber: Callable[[E], None] = None):
        if subscriber:
            with self._lock:
                self._subscribers[type].append(subscriber)
        else:

            def decorator(subscriber: Callable[[E], None]):
                if not asyncio.iscoroutinefunction(subscriber):
                    raise TypeError("Subscriber must be a coroutine function.")

                @wraps(subscriber)
                async def wrapper(event):
                    return await subscriber(event)

                self.subscribe(type, wrapper)
                return wrapper

            return decorator

    def unsubscribe(self, type: Type[Event], subscriber: Callable[[E], None]) -> None:
        with self._lock:
            self._subscribers[type].remove(subscriber)

    def publish(self, event: E) -> None:
        with self._lock:
            for subscriber in list(self._subscribers[event.__class__]):
                if not asyncio.iscoroutinefunction(subscriber):
                    raise TypeError("Subscriber must be a coroutine function.")
                asyncio.create_task(subscriber(event))
