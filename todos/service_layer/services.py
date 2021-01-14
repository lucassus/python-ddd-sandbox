from datetime import date, datetime
from typing import Callable, Protocol

from todos.domain.models import Task
from todos.service_layer.unit_of_work import UnitOfWork


class SupportsCommit(Protocol):
    def commit(self) -> None:
        ...


def create_task(
    name: str,
    *,
    uof: UnitOfWork,  # TODO: Should use an abstraction
) -> Task:
    task = Task(name=name)

    with uof:
        uof.repository.create(task)
        uof.commit()

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
