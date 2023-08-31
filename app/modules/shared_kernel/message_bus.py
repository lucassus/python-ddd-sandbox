import abc
from collections import defaultdict
from typing import Callable, Protocol


class Event(abc.ABC):
    pass


class Command(abc.ABC):
    pass


Message = Command | Event


class SupportsDispatchingEvents(Protocol):
    def dispatch(self, event: Event) -> None:
        ...


class MessageBus(SupportsDispatchingEvents):
    _listeners: dict[type[Event], list[Callable[[Event], None]]]

    def __init__(self):
        self._listeners = defaultdict(list)

    def dispatch(self, event: Event) -> None:
        handlers = self._listeners[type(event)]

        for handle in handlers:
            handle(event)

    def listen(self, event_class: type[Event], fn=None):
        def on(handler):
            self._listeners[event_class].append(handler)

        return on(fn) if fn else on
