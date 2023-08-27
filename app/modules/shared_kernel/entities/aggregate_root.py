from app.modules.shared_kernel.entities.entity import Entity
from app.modules.shared_kernel.message_bus import Event


class AggregateRoot(Entity):
    _events: list[Event]

    def __init__(self):
        self._events = []

    @property
    def events(self) -> tuple[Event, ...]:
        return tuple(self._events)

    def queue_event(self, event: Event):
        self._events.append(event)

    def clear_events(self):
        self._events.clear()
