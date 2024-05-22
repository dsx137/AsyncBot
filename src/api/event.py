import threading
import asyncio
from collections import defaultdict
from functools import wraps
from abc import ABC, abstractmethod
from typing import TypeVar, Type, Callable

E = TypeVar("E", bound="Event")


class Event:
    pass


class Bus:
    def __init__(self):
        self._subscribers = defaultdict(list)
        self._lock = threading.Lock()

    def subscribe(self, type: Type[Event], subscriber: Callable[[E], None]):
        with self._lock:
            self._subscribers[type].append(subscriber)

    def unsubscribe(self, type: Type[Event], subscriber: Callable[[E], None]):
        with self._lock:
            self._subscribers[type].remove(subscriber)

    def publish(self, event: E):
        with self._lock:
            for subscriber in list(self._subscribers[event.__class__]):
                if not asyncio.iscoroutinefunction(subscriber):
                    raise TypeError("Subscriber must be a coroutine function.")
                asyncio.create_task(subscriber(event))
