from dataclasses import dataclass

from app.modules.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.projects.domain.project import ProjectID, ProjectName
from app.shared.message_bus import Command, CommandHandler


@dataclass(frozen=True)
class UpdateProject(Command[None]):
    project_id: ProjectID
    name: ProjectName


class UpdateProjectHandler(CommandHandler[UpdateProject, None]):
    def __init__(self, uow: AbstractUnitOfWork):
        self._uow = uow

    def __call__(self, command: UpdateProject) -> None:
        project_id, name = command.project_id, command.name

        with self._uow as uow:
            project = uow.projects.get(project_id)
            project.name = name
            uow.commit()
