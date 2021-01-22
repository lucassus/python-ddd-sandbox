from collections import defaultdict
from typing import Any, Callable, Dict, List

from examples.message_bus.event import Event


class MessageBus:
    def __init__(self):
        self._listeners: Dict[type, List[Callable]] = defaultdict(list)

    # TODO: How to type a class?
    def listen(self, event_class, handler: Callable[[Any, Event], None]):
        if event_class not in self._listeners:
            self._listeners[event_class] = []

        self._listeners[event_class].append(handler)

    def dispatch(self, event: Event) -> None:
        handlers = self._listeners.get(type(event), [])

        for handle in handlers:
            handle(event)
