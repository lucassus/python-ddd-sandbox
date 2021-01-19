from datetime import date

from todos.domain.entities import Project, Task
from todos.service_layer.abstract_unit_of_work import AbstractUnitOfWork


class Service:
    def __init__(self, *, project_id: int, uow: AbstractUnitOfWork):
        self._project_id = project_id
        self._uow = uow

    def create_task(self, name: str) -> Task:
        project = self.get_project()
        task = project.add_task(name=name)

        self._uow.commit()

        return task

    def complete_task(self, id: int, *, now: date):
        project = self.get_project()
        task = project.complete_task(id, now)

        self._uow.commit()

        # TODO: Send a notification

        return task

    def incomplete_task(self, id: int):
        project = self.get_project()
        task = project.incomplete_task(id)

        self._uow.commit()

        return task

    def get_project(self) -> Project:
        project = self._uow.repository.get(self._project_id)
        assert project
        return project
