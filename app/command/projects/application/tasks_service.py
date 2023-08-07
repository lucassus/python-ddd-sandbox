from datetime import datetime

from app.command.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.command.projects.application.specifications import ActiveProjectSpecification
from app.command.projects.entities.project import Project, ProjectID
from app.command.projects.entities.task import TaskNumber
from app.utc_datetime import utc_now


class TasksService:
    def __init__(self, *, uow: AbstractUnitOfWork):
        self._uow = uow
        self._active = ActiveProjectSpecification()

    def _get_active_project(self, project_id: ProjectID) -> Project:
        return self._active.satisfied_from(self._uow.project, by=project_id)

    def create_task(
        self,
        project_id: ProjectID,
        name: str,
    ) -> TaskNumber:
        with self._uow as uow:
            project = self._get_active_project(project_id)
            task = project.add_task(name=name)

            uow.commit()
            return task.number

    def complete_task(
        self,
        project_id: ProjectID,
        number: TaskNumber,
        now: None | datetime = None,
    ) -> None:
        if now is None:
            now = utc_now()

        with self._uow as uow:
            project = self._get_active_project(project_id)
            project.complete_task(number, now)

            uow.commit()

    def incomplete_task(
        self,
        project_id: ProjectID,
        number: TaskNumber,
    ) -> None:
        with self._uow as uow:
            project = self._get_active_project(project_id)
            project.incomplete_task(number)

            uow.commit()
