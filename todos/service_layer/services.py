from datetime import date, datetime
from typing import Callable, Protocol

from todos.domain.models.task import Task
from todos.interfaces.abstract_repository import AbstractRepository


class SupportsCommit(Protocol):
    def commit(self) -> None:
        ...


def create_todo(
    name: str,
    *,
    repository: AbstractRepository,
    session: SupportsCommit,
) -> Task:
    todo = Task(name=name)

    repository.create(todo)
    session.commit()

    return todo


def complete_todo(
    todo: Task,
    *,
    session: SupportsCommit,
    now: Callable[..., date] = datetime.utcnow,
) -> Task:
    todo.complete(now)
    session.commit()

    return todo


def incomplete_todo(todo: Task, *, session: SupportsCommit) -> Task:
    todo.incomplete()
    session.commit()

    return todo
