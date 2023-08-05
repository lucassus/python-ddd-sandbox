from app.command.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.command.projects.entities.factories import build_example_project
from app.command.projects.entities.project import ProjectID
from app.command.shared_kernel.entities.user_id import UserID


class CreateExampleProject:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def __call__(self, user_id: UserID) -> ProjectID:
        with self.uow:
            new_project = build_example_project(user_id)
            self.uow.project.create(new_project)
            self.uow.commit()

            return new_project.id
