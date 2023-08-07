from datetime import datetime

from app.command.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.command.projects.application.specifications import ActiveProjectSpecification, ArchivedProjectSpecification
from app.command.projects.entities.project import Project, ProjectID
from app.utc_datetime import utc_now


class ArchivizationService:
    def __init__(self, uow: AbstractUnitOfWork):
        self._uow = uow

        self._active = ActiveProjectSpecification()
        self._archived = ArchivedProjectSpecification()

    def _get_active_project(self, project_id: ProjectID) -> Project:
        return self._active.satisfied_from(self._uow.project, by=project_id)

    def _get_archived_project(self, project_id: ProjectID) -> Project:
        return self._archived.satisfied_from(self._uow.project, by=project_id)

    def archive(self, project_id: ProjectID, now: None | datetime = None) -> None:
        if now is None:
            now = utc_now()

        with self._uow as uow:
            project = self._get_active_project(project_id)
            project.archive(now)

            uow.commit()

    def unarchive(self, project_id: ProjectID) -> None:
        with self._uow as uow:
            project = self._get_archived_project(project_id)
            project.unarchive()

            uow.commit()

    def delete(self, project_id: ProjectID, now: None | datetime = None) -> None:
        if now is None:
            now = utc_now()

        with self._uow as uow:
            project = self._get_archived_project(project_id)
            project.delete(now)

            uow.commit()
