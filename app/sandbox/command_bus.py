import abc
from typing import Any, Generic, TypeVar, Type, cast

CR = TypeVar("CR", bound=Any)


class Command(Generic[CR]):
    pass


C = TypeVar("C", bound=Command[Any])


class CommandHandler(Generic[C, CR]):
    @abc.abstractmethod
    def __call__(self, command: C) -> CR:
        raise NotImplementedError


# TODO: Incorporate this with the main MessageBus class
class CommandBus:
    _handlers: dict[type[Command[Any]], CommandHandler[Command[Any], Any]]

    def __init__(self) -> None:
        self._handlers = {}

    def register(
        self,
        command_type: Type[C],
        handler: CommandHandler[C, CR],
    ) -> None:
        self._handlers[command_type] = cast(CommandHandler[Any, Command[Any]], handler)

    def execute(self, command: Command[CR]) -> CR:
        handler = self._handlers[type(command)]
        return handler(command)
