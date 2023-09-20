import abc
from collections import defaultdict
from typing import Any, Generic, Protocol, TypeVar, cast


class Event(metaclass=abc.ABCMeta):
    pass


CR = TypeVar("CR", bound=Any)


class CommandThatReturns(Generic[CR], metaclass=abc.ABCMeta):
    pass


class Command(CommandThatReturns[None], metaclass=abc.ABCMeta):
    pass


C = TypeVar("C", bound=CommandThatReturns[Any])


class CommandHandler(Generic[C, CR], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __call__(self, command: C) -> CR:
        raise NotImplementedError


E = TypeVar("E", bound=Event)


class EventHandler(Generic[E], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __call__(self, event: E) -> None:
        raise NotImplementedError


class SupportsDispatchingEvents(Protocol):
    def dispatch(self, event: Event) -> None:
        ...


class CommandHandlerNotFoundError(Exception):
    def __init__(self, command: CommandThatReturns[Any]) -> None:
        super().__init__(f"Command handler not found for {type(command)}")


class MessageBus(SupportsDispatchingEvents):
    _command_handlers: dict[type[CommandThatReturns[Any]], CommandHandler[CommandThatReturns[Any], Any]]

    _event_listeners: dict[type[Event], list[EventHandler[Any]]]

    def __init__(self):
        self._event_listeners = defaultdict(list)
        self._command_handlers = {}

    def execute(self, command: CommandThatReturns[CR]) -> CR:
        handler = self._command_handlers.get(type(command))
        if handler is None:
            raise CommandHandlerNotFoundError(command)

        return handler(command)

    def dispatch(self, event: Event) -> None:
        handlers = self._event_listeners[type(event)]

        for handle in handlers:
            handle(event)

    def register(
        self,
        command_class: type[C],
        handler: CommandHandler[C, CR],
    ):
        if command_class in self._command_handlers:
            raise ValueError(f"Command {command_class} is already registered")

        self._command_handlers[command_class] = cast(CommandHandler[Any, CommandThatReturns[Any]], handler)

    def listen(self, event_class: type[Event], handler: EventHandler[E]):
        self._event_listeners[event_class].append(handler)
