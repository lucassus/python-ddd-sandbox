from datetime import date, datetime
from typing import Callable, Protocol

from todos.domain.models.todo import Todo
from todos.interfaces.abstract_repository import AbstractRepository


class SupportsCommit(Protocol):
    def commit(self) -> None:
        ...


def create_todo(
    name: str,
    *,
    repository: AbstractRepository,
    session: SupportsCommit,
) -> Todo:
    todo = Todo(name=name)

    repository.create(todo)
    session.commit()

    return todo


def complete_todo(
    todo: Todo,
    *,
    session: SupportsCommit,
    now: Callable[..., date] = datetime.utcnow,
) -> Todo:
    todo.complete(now)
    session.commit()

    return todo


def incomplete_todo(todo: Todo, *, session: SupportsCommit) -> Todo:
    todo.incomplete()
    session.commit()

    return todo
