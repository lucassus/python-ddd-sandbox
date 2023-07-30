from datetime import date

from app.modules.projects.domain.entities import ProjectID, TaskID
from app.modules.projects.domain.factories import build_example_project
from app.modules.projects.domain.ports import AbstractUnitOfWork
from app.shared_kernel.user_id import UserID


# TODO: Split it into smaller services / use cases
class Service:
    def __init__(self, *, uow: AbstractUnitOfWork):
        self._uow = uow

    def create_example_project(self, *, user_id: UserID) -> ProjectID:
        with self._uow as uow:
            new_project = build_example_project(user_id)
            uow.project.create(new_project)
            uow.commit()

            return new_project.id

    def create_task(self, *, project_id: ProjectID, name: str) -> TaskID:
        with self._uow as uow:
            project = uow.project.get(project_id)
            task = project.add_task(name=name)

            uow.commit()
            return task.id

    def complete_task(self, id: TaskID, *, project_id: ProjectID, now: date) -> None:
        with self._uow as uow:
            project = uow.project.get(project_id)
            project.complete_task(id, now)

            uow.commit()

    def incomplete_task(self, id: TaskID, *, project_id: ProjectID) -> None:
        with self._uow as uow:
            project = uow.project.get(project_id)
            project.incomplete_task(id)

            uow.commit()
