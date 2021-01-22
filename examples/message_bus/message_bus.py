from collections import defaultdict
from typing import Callable, Dict, List

from examples.message_bus.event import Event


class MessageBus:
    def __init__(self):
        self._listeners: Dict[type, List[Callable]] = defaultdict(list)

    def listen(self, event_class: type, fn=None):
        def on(handler):
            self._listeners[event_class].append(handler)

        return on(fn) if fn else on

    def dispatch(self, event: Event) -> None:
        handlers = self._listeners[type(event)]

        for handle in handlers:
            handle(event)
