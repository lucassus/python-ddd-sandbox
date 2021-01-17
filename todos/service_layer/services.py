from datetime import date, datetime
from typing import Callable

from todos.domain.models import Task
from todos.interfaces.abstract_unit_of_work import AbstractUnitOfWork


def create_task(
    name: str,
    *,
    uow: AbstractUnitOfWork,
) -> Task:
    project = uow.repository.get()
    task = project.add_task(name=name)
    uow.commit()

    return task


def complete_task(
    task: Task,
    *,
    uow: AbstractUnitOfWork,
    now: Callable[..., date] = datetime.utcnow,
) -> Task:
    task.complete(now)
    uow.commit()

    return task


def incomplete_task(
    task: Task,
    *,
    uow: AbstractUnitOfWork,
) -> Task:
    task.incomplete()
    uow.commit()

    return task
