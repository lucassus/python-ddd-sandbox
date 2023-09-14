from dataclasses import dataclass

from app.modules.projects.domain.project import ProjectID
from app.shared.message_bus import Command, CommandHandler


@dataclass(frozen=True)
class UnarchiveProject(Command):
    project_id: ProjectID


class UnarchiveProjectHandler(CommandHandler[UnarchiveProject, None]):
    def __init__(self, uow):
        self._uow = uow

    def __call__(self, command: UnarchiveProject):
        with self._uow as ouw:
            project = ouw.projects.get_archived(command.project_id)
            project.unarchive()

            ouw.commit()
