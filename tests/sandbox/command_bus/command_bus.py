import abc
from typing import Any, Generic, TypeVar, Type


class Command(metaclass=abc.ABCMeta):
    pass


C = TypeVar("C", bound=Command)


class CommandHandler(Generic[C], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __call__(self, command: C) -> None:
        raise NotImplementedError


class CommandBus:
    def __init__(self) -> None:
        self._handlers: dict[type[Command], CommandHandler[Any]] = {}

    def register(
        self,
        command_class: Type[Command],
        handler: CommandHandler[Command],
    ) -> None:
        self._handlers[command_class] = handler

    def execute(self, command: Command) -> None:
        handler = self._handlers[type(command)]
        handler(command)
