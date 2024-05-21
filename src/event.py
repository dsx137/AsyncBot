import threading
import asyncio
from collections import defaultdict
from functools import wraps
from abc import ABC, abstractmethod


class Bus:
    def __init__(self):
        self._subscribers = defaultdict(list)
        self._lock = threading.Lock()

    def subscribe(self, type: str, subscriber: callable):
        with self._lock:
            self._subscribers[type].append(subscriber)

    def unsubscribe(self, type: str, subscriber: callable):
        with self._lock:
            self._subscribers[type].remove(subscriber)

    def publish(self, publisher, type: str, data=None):
        with self._lock:
            for subscriber in list(self._subscribers[type]):
                if not asyncio.iscoroutinefunction(subscriber):
                    raise TypeError("Subscriber must be a coroutine function.")
                asyncio.create_task(subscriber(publisher, data))


# class AbstractPublisher(ABC):
#     def __init__(self) -> None:
#         self._bus = Bus()

#     def publish(self, type: str, data=None) -> None:
#         self._bus.publish(type, data)


# class AbstractHandler(ABC):
#     def __init__(self, publisher: AbstractPublisher) -> None:
#         self._publisher = publisher

#     def subscribe(self, *types: str) -> callable:
#         def decorator(func):
#             if not asyncio.iscoroutinefunction(func):
#                 raise TypeError("Subscriber must be a coroutine function.")

#             @wraps(func)
#             async def wrapper(*args, **kwargs):
#                 return await func(*args, **kwargs)

#             for type in types:
#                 self._publisher._bus.subscribe(type, wrapper)
#             return wrapper

#         return decorator

#     @abstractmethod
#     def _on_init(self):
#         pass
