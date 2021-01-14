from datetime import date, datetime
from typing import Callable, Protocol

from todos.domain.models import Task
from todos.interfaces.abstract_repository import AbstractRepository


class SupportsCommit(Protocol):
    def commit(self) -> None:
        ...


def create_task(
    name: str,
    *,
    repository: AbstractRepository,
    session: SupportsCommit,
) -> Task:
    task = Task(name=name)

    repository.create(task)
    session.commit()

    return task


def complete_task(
    task: Task,
    *,
    session: SupportsCommit,
    now: Callable[..., date] = datetime.utcnow,
) -> Task:
    task.complete(now)
    session.commit()

    return task


def incomplete_task(task: Task, *, session: SupportsCommit) -> Task:
    task.incomplete()
    session.commit()

    return task
