import abc
from collections import defaultdict
from typing import Callable


class BaseEvent(abc.ABC):
    pass


class MessageBus:
    def __init__(self):
        self._listeners: dict[type, list[Callable]] = defaultdict(list)

    def listen(self, event_class: type, fn=None):
        def on(handler):
            self._listeners[event_class].append(handler)

        return on(fn) if fn else on

    def dispatch(self, event: BaseEvent) -> None:
        handlers = self._listeners[type(event)]

        for handle in handlers:
            handle(event)
