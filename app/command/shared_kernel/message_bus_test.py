from dataclasses import dataclass
from unittest import mock

import pytest

from app.command.shared_kernel.message_bus import BaseEvent, MessageBus


@dataclass(frozen=True)
class SomeEvent(BaseEvent):
    message: str


@dataclass(frozen=True)
class SomeOtherEvent(BaseEvent):
    id: int


@pytest.fixture()
def bus() -> MessageBus:
    return MessageBus()


class TestMessageBus:
    def test_simple_listener(self, bus):
        # Given
        handle_some_event = mock.Mock()
        bus.listen(SomeEvent, handle_some_event)

        # When
        event = SomeEvent(message="Hello!")
        bus.dispatch(event)

        # Then
        handle_some_event.assert_called()
        handle_some_event.assert_called_with(event)

    def test_decorator_listener(self, bus):
        # Given
        mock_handle = mock.Mock()

        @bus.listen(SomeEvent)
        def handle_some_event(event: SomeEvent):
            mock_handle(event)

        # When
        event = SomeEvent(message="Hello!")
        bus.dispatch(event)

        # Then
        mock_handle.assert_called_with(event)

    def test_event_can_have_multiple_handlers(self, bus):
        # Given
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

    def test_do_nothing_when_the_message_cannot_be_handled(self, bus):
        # Given
        mock_handle = mock.Mock()
        bus.listen(SomeEvent, mock_handle)

        # When
        bus.dispatch(SomeOtherEvent(id=123))

        # Then
        mock_handle.assert_not_called()
