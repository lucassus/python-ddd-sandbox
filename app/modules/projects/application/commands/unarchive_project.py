from dataclasses import dataclass

from app.infrastructure.message_bus import Command, CommandHandler
from app.modules.projects.domain.project import ProjectID


@dataclass(frozen=True)
class UnarchiveProject(Command[None]):
    project_id: ProjectID


class UnarchiveProjectHandler(CommandHandler[UnarchiveProject, None]):
    def __init__(self, uow):
        self._uow = uow

    def __call__(self, command: UnarchiveProject):
        with self._uow as ouw:
            project = ouw.projects.get_archived(command.project_id)
            project.unarchive()

            ouw.commit()
