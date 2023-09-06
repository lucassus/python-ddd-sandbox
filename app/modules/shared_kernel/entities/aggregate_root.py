import abc

from app.infrastructure.message_bus import Event
from app.modules.shared_kernel.entities.entity import Entity


class AggregateRoot(Entity, metaclass=abc.ABCMeta):
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

    @abc.abstractmethod
    def __hash__(self) -> int:
        raise NotImplementedError
