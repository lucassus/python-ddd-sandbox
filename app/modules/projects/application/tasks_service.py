from datetime import datetime
from typing import Optional

from app.modules.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.task import TaskNumber
from app.modules.shared_kernel.entities.user_id import UserID
from app.utc_datetime import utc_now


class TasksService:
    def __init__(self, *, uow: AbstractUnitOfWork):
        self._uow = uow

    def create_task(
        self,
        project_id: ProjectID,
        name: str,
        created_by: Optional[UserID] = None,
    ) -> TaskNumber:
        with self._uow as uow:
            project = uow.project.get(project_id)
            task = project.add_task(name=name, created_by=created_by)

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
            project = uow.project.get(project_id)
            project.complete_task(number, now)

            uow.commit()

    def incomplete_task(
        self,
        project_id: ProjectID,
        number: TaskNumber,
    ) -> None:
        with self._uow as uow:
            project = uow.project.get(project_id)
            project.incomplete_task(number)

            uow.commit()
