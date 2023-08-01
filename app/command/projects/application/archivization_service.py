from datetime import date

from app.command.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.command.projects.entities.project import ProjectID


class ArchivizationService:
    def __init__(self, uow: AbstractUnitOfWork):
        self._uow = uow

    def archive(self, project_id: ProjectID, now: None | date = None) -> None:
        if now is None:
            now = date.today()

        with self._uow as ouw:
            project = ouw.project.get(project_id)
            project.archive(now)

            ouw.commit()

    def unarchive(self, project_id: ProjectID) -> None:
        with self._uow as ouw:
            project = ouw.project.get_archived(project_id)
            project.unarchive()

            ouw.commit()
