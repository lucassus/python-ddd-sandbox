from datetime import date

from todos.domain.entities import Task
from todos.domain.ports import AbstractUnitOfWork


class Service:
    def __init__(self, *, project_id: int, uow: AbstractUnitOfWork):
        self._project_id = project_id
        self._uow = uow

    def create_task(self, name: str) -> Task:
        with self._uow as uow:
            project = uow.repository.get(self._project_id)
            task = project.add_task(name=name)

            uow.commit()

        return task

    def complete_task(self, id: int, *, now: date):
        with self._uow as uow:
            project = uow.repository.get(self._project_id)
            task = project.complete_task(id, now)

            uow.commit()

        return task

    def incomplete_task(self, id: int):
        with self._uow as uow:
            project = uow.repository.get(self._project_id)
            task = project.incomplete_task(id)

            uow.commit()

        return task
