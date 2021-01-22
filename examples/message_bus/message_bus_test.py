from dataclasses import dataclass
from unittest import mock

from examples.message_bus.message_bus import BaseEvent, MessageBus


@dataclass
class SomeEvent(BaseEvent):
    message: str


@dataclass
class SomeOtherEvent(BaseEvent):
    id: int


class TestMessageBus:
    def test_simple_listener(self):
        # Given
        bus = MessageBus()

        handle_some_event = mock.Mock()
        bus.listen(SomeEvent, handle_some_event)

        # When
        bus.dispatch(SomeEvent(message="Hello!"))

        # Then
        handle_some_event.assert_called()
        handle_some_event.assert_called_with(SomeEvent(message="Hello!"))

    def test_decorator_listener(self):
        # Given
        bus = MessageBus()

        results = []

        @bus.listen(SomeEvent)
        def handle_some_event(event: SomeEvent):
            results.append(event.message)

        # When
        bus.dispatch(SomeEvent(message="Hello!"))

        # Then
        assert len(results) == 1
        assert results[-1] == "Hello!"

    def test_event_can_have_multiple_handlers(self):
        # Given
        bus = MessageBus()

        handle_event_1 = mock.Mock()
        bus.listen(SomeEvent, handle_event_1)
        bus.listen(SomeOtherEvent, handle_event_1)

        handle_event_2 = mock.Mock()
        bus.listen(SomeEvent, handle_event_2)

        # When
        bus.dispatch(SomeEvent(message="Hello!"))
        bus.dispatch(SomeOtherEvent(id=123))

        # Then
        assert handle_event_1.call_count == 2
        assert handle_event_2.call_count == 1

    def test_do_nothing_when_the_message_cannot_be_handled(self):
        bus = MessageBus()
        bus.dispatch(SomeEvent(message="Hello!"))
