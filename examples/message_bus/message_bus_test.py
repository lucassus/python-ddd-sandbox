from dataclasses import dataclass

from examples.message_bus.event import Event
from examples.message_bus.message_bus import MessageBus


@dataclass
class SomeEvent(Event):
    message: str


class TestMessageBus:
    def test_simple_listener(self):
        bus = MessageBus()

        # TODO: Find a more pythonic way
        results = []

        def handle_some_event(event: SomeEvent):
            results.append(event.message)

        bus.listen(SomeEvent, handle_some_event)

        bus.dispatch(SomeEvent(message="Hello!"))

        assert len(results) == 1
        assert results[-1] == "Hello!"

    def test_decorator_listener(self):
        bus = MessageBus()

        results = []

        @bus.listen(SomeEvent)
        def handle_some_event(event: SomeEvent):
            results.append(event.message)

        bus.dispatch(SomeEvent(message="Hello!"))

        assert len(results) == 1
        assert results[-1] == "Hello!"

    def test_event_can_have_multiple_handlers(self):
        bus = MessageBus()

        results = []

        def handle_event_1(event: SomeEvent):
            results.append(event.message)

        bus.listen(SomeEvent, handle_event_1)

        def handle_event_2(event: SomeEvent):
            results.append(event.message)

        bus.listen(SomeEvent, handle_event_2)

        bus.dispatch(SomeEvent(message="Hello!"))

        assert len(results) == 2

    def test_do_nothing_when_the_message_cannot_be_handled(self):
        bus = MessageBus()
        bus.dispatch(SomeEvent(message="Hello!"))
