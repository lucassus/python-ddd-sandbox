from app.command.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.command.projects.entities.project import Project, ProjectID
from app.command.projects.entities.specifications import ActiveProjectSpecification, ArchivedProjectSpecification


class ActiveProjectFetcher:
    def __init__(self, uow: AbstractUnitOfWork):
        self._uow = uow
        self._active = ActiveProjectSpecification()

    def __call__(self, project_id: ProjectID) -> Project:
        project = self._uow.project.get_active(project_id)

        if not self._active.is_satisfied_by(project):
            raise ValueError(f"Project {project_id} is not active")

        return project


class ArchivedProjectFetcher:
    def __init__(self, uow: AbstractUnitOfWork):
        self._uow = uow
        self._archived = ArchivedProjectSpecification()

    def __call__(self, project_id: ProjectID) -> Project:
        project = self._uow.project.get_archived(project_id)

        if not self._archived.is_satisfied_by(project):
            raise ValueError(f"Project {project_id} is not archived")

        return project
