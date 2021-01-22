from dataclasses import dataclass

from examples.message_bus.event import Event
from examples.message_bus.message_bus import MessageBus


@dataclass
class SomeEvent(Event):
    message: str


def test_message_bus():
    bus = MessageBus()

    results = []

    def callback(event: SomeEvent):
        results.append(event.message)

    bus.listen(SomeEvent, callback)

    bus.dispatch(SomeEvent(message="Hello!"))

    assert len(results) == 1
    assert results[-1] == "Hello!"
