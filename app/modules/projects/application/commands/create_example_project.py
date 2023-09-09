from dataclasses import dataclass

from app.modules.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.projects.domain.factories import build_example_project
from app.modules.projects.domain.project import ProjectID
from app.modules.shared_kernel.entities.user_id import UserID
from app.shared.message_bus import Command, CommandHandler


@dataclass(frozen=True)
class CreateExampleProject(Command[ProjectID]):
    user_id: UserID


class CreateExampleProjectHandler(CommandHandler[CreateExampleProject, ProjectID]):
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def __call__(self, command: CreateExampleProject) -> ProjectID:
        new_project = build_example_project(command.user_id)

        with self.uow:
            self.uow.projects.create(new_project)
            self.uow.commit()

        return new_project.id
