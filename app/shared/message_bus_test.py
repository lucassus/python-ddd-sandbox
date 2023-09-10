from dataclasses import dataclass
from typing import assert_type
from unittest import mock

import pytest

from app.shared.message_bus import Event, MessageBus, Command, CommandHandler


@dataclass(frozen=True)
class SomeEvent(Event):
    message: str


@dataclass(frozen=True)
class SomeOtherEvent(Event):
    id: int


@pytest.fixture()
def bus() -> MessageBus:
    return MessageBus()


class TestMessageBus:
    def test_simple_listener(self, bus: MessageBus):
        # Given
        handle_some_event = mock.Mock()
        bus.listen(SomeEvent, handle_some_event)

        # When
        event = SomeEvent(message="Hello!")
        bus.dispatch(event)

        # Then
        handle_some_event.assert_called()
        handle_some_event.assert_called_with(event)

    def test_event_can_have_multiple_handlers(self, bus: MessageBus):
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

    def test_do_nothing_when_the_message_cannot_be_handled(self, bus: MessageBus):
        # Given
        mock_handle = mock.Mock()
        bus.listen(SomeEvent, mock_handle)

        # When
        bus.dispatch(SomeOtherEvent(id=123))

        # Then
        mock_handle.assert_not_called()

    def test_command_without_return_value(self, bus: MessageBus):
        # Given
        @dataclass(frozen=True)
        class Increment(Command[None]):
            value: int

        class IncrementHandler(CommandHandler[Increment, None]):
            def __init__(self, by: int):
                self._by = by

            def __call__(self, command: Increment) -> None:
                pass

        bus.register(Increment, IncrementHandler(2))

        # When
        result = bus.execute(Increment(3))

        # Then
        assert_type(result, None)
        assert result is None

    def test_command_with_return_value(self, bus: MessageBus):
        # Given
        @dataclass(frozen=True)
        class Increment(Command[int]):
            value: int

        class IncrementHandler(CommandHandler[Increment, int]):
            def __init__(self, by: int):
                self._by = by

            def __call__(self, command: Increment) -> int:
                return command.value + self._by

        bus.register(Increment, IncrementHandler(2))

        # When
        result = bus.execute(Increment(3))

        # Then
        assert_type(result, int)
        assert result == 5
