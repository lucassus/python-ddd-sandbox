from app.command.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.command.projects.entities.factories import build_project
from app.command.projects.entities.project import ProjectID
from app.shared_kernel.user_id import UserID


class CreateProject:
    def __init__(self, *, uow: AbstractUnitOfWork):
        self._uow = uow

    def __call__(self, user_id: UserID, name: str) -> ProjectID:
        with self._uow as uow:
            new_project = build_project(user_id=user_id, name=name)
            new_project = uow.project.create(new_project)
            uow.commit()

            return new_project.id
