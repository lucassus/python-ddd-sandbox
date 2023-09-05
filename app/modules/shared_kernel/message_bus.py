import abc
from collections import defaultdict
from typing import Callable, Generic, Protocol, TypeVar, Any


class Event(abc.ABC):
    pass


class Command(abc.ABC):
    pass


C = TypeVar("C", bound=Command, contravariant=True)


class CommandHandler(Generic[C], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __call__(self, command: C) -> None:
        raise NotImplementedError


class SupportsDispatchingEvents(Protocol):
    def dispatch(self, event: Event) -> None:
        ...


class MessageBus(SupportsDispatchingEvents):
    _command_handlers: dict[type[Command], CommandHandler[Any]]

    _event_listeners: dict[type[Event], list[Callable[[Event], None]]]

    def __init__(self):
        self._event_listeners = defaultdict(list)
        self._command_handlers = {}

    def execute(self, command: Command):
        handler = self._command_handlers[type(command)]
        handler(command)

    def dispatch(self, event: Event) -> None:
        handlers = self._event_listeners[type(event)]

        for handle in handlers:
            handle(event)

    def register(
        self,
        command_class: type[C],
        handler: CommandHandler[C],
    ):
        self._command_handlers[command_class] = handler

    def listen(
        self,
        event_class: type[Event],
        handler=None,
    ):
        def on(handler):
            self._event_listeners[event_class].append(handler)

        return on(handler) if handler else on
