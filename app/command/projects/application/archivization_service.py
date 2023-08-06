from datetime import datetime

from app.command.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.command.projects.entities.project import ProjectID
from app.utc_datetime import utc_now


class ArchivizationService:
    def __init__(self, uow: AbstractUnitOfWork):
        self._uow = uow

    def archive(self, project_id: ProjectID, now: None | datetime = None) -> None:
        if now is None:
            now = utc_now()

        with self._uow as ouw:
            project = ouw.project.get(project_id)
            project.archive(now)

            ouw.commit()

    def unarchive(self, project_id: ProjectID) -> None:
        with self._uow as ouw:
            project = ouw.project.get_archived(project_id)
            project.unarchive()

            ouw.commit()

    def delete(self, project_id: ProjectID, now: None | datetime = None) -> None:
        if now is None:
            now = utc_now()

        with self._uow as ouw:
            project = ouw.project.get_archived(project_id)
            project.delete(now)

            ouw.commit()
