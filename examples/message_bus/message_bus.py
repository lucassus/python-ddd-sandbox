from typing import Any, Callable

from examples.message_bus.event import Event


class MessageBus:
    _listeners = {}

    # TODO: How to type a class?
    def listen(self, event_class, handler: Callable[[Any, Event], None]):
        if event_class not in self._listeners:
            self._listeners[event_class] = []

        self._listeners[event_class].append(handler)

    def dispatch(self, event: Event) -> None:
        handlers = self._listeners.get(type(event), [])

        for handle in handlers:
            handle(event)
