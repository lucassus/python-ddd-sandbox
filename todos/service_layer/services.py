from datetime import date

from todos.domain.entities import Project, Task
from todos.interfaces.abstract_unit_of_work import AbstractUnitOfWork


def create_task(
    name: str,
    *,
    project: Project,
    uow: AbstractUnitOfWork,
) -> Task:
    task = project.add_task(name=name)
    uow.commit()

    return task


def complete_task(
    id: int,
    *,
    project: Project,
    now: date,
    uow: AbstractUnitOfWork,
) -> Task:
    task = project.complete_task(id, now)
    uow.commit()

    return task


def incomplete_task(
    id: int,
    *,
    project: Project,
    uow: AbstractUnitOfWork,
) -> Task:
    task = project.incomplete_task(id)
    uow.commit()

    return task
