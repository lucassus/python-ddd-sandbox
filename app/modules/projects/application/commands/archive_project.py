from dataclasses import dataclass
from datetime import datetime

from app.modules.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.projects.domain.project import ProjectID
from app.shared.message_bus import Command, CommandHandler


@dataclass(frozen=True)
class ArchiveProject(Command[None]):
    project_id: ProjectID
    now: datetime


class ArchiveProjectHandler(CommandHandler[ArchiveProject, None]):
    def __init__(self, uow: AbstractUnitOfWork):
        self._uow = uow

    def __call__(self, command: ArchiveProject) -> None:
        with self._uow as ouw:
            project = ouw.projects.get(command.project_id)
            project.archive(command.now)

            ouw.commit()
