from datetime import date

from todos.domain.ports import AbstractUnitOfWork


class Service:
    def __init__(self, *, uow: AbstractUnitOfWork):
        self._uow = uow

    def create_task(self, *, project_id, name: str) -> id:
        with self._uow as uow:
            project = uow.repository.get(project_id)
            task = project.add_task(name=name)

            uow.commit()
            return task.id

    def complete_task(self, id: int, *, project_id: int, now: date) -> int:
        with self._uow as uow:
            project = uow.repository.get(project_id)
            task = project.complete_task(id, now)

            uow.commit()
            return task.id

    def incomplete_task(self, id: int, *, project_id: int) -> int:
        with self._uow as uow:
            project = uow.repository.get(project_id)
            task = project.incomplete_task(id)

            uow.commit()
            return task.id
