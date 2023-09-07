from dataclasses import dataclass

from app.modules.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.projects.domain.project import Project, ProjectID, ProjectName
from app.modules.shared_kernel.entities.user_id import UserID
from app.shared.message_bus import Command, CommandHandler, MessageBus


@dataclass(frozen=True)
class CreateProject(Command[ProjectID]):
    user_id: UserID
    name: ProjectName


class CreateProjectHandler(CommandHandler[CreateProject, ProjectID]):
    def __init__(self, *, uow: AbstractUnitOfWork, bus: MessageBus):
        self._uow = uow
        self._bus = bus

    def __call__(self, command: CreateProject) -> ProjectID:
        new_project = Project(user_id=command.user_id, name=command.name)

        with self._uow as uow:
            new_project = uow.projects.create(new_project)
            uow.commit()

        # In this example events are raised in the service layer
        self._bus.dispatch(Project.Created(project_id=new_project.id))

        return new_project.id
