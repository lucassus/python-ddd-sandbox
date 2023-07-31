from datetime import date

from app.command.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.command.projects.entities.project import ProjectID
from app.command.projects.entities.task import TaskNumber


class TasksService:
    def __init__(self, *, uow: AbstractUnitOfWork):
        self._uow = uow

    def create_task(self, *, project_id: ProjectID, name: str) -> TaskNumber:
        with self._uow as uow:
            project = uow.project.get(project_id)
            task = project.add_task(name=name)

            uow.commit()
            return task.number

    def complete_task(self, number: TaskNumber, *, project_id: ProjectID, now: date) -> None:
        with self._uow as uow:
            project = uow.project.get(project_id)
            project.complete_task(number, now)

            uow.commit()

    def incomplete_task(self, number: TaskNumber, *, project_id: ProjectID) -> None:
        with self._uow as uow:
            project = uow.project.get(project_id)
            project.incomplete_task(number)

            uow.commit()