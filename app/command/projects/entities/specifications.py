from app.command.projects.application.ports.abstract_project_repository import AbstractProjectRepository
from app.command.projects.entities.project import Project, ProjectID
from app.command.shared_kernel.specification import Specification


class DeletedProjectSpecification(Specification[Project]):
    def is_satisfied_by(self, project: Project) -> bool:
        return project.deleted_at is not None


class ArchivedProjectSpecification(Specification[Project]):
    def is_satisfied_by(self, candidate: Project) -> bool:
        if DeletedProjectSpecification().is_satisfied_by(candidate):
            return False

        return candidate.archived_at is not None

    # TODO: Add a better exception
    def satisfied_from(self, repository: AbstractProjectRepository, *, by: ProjectID) -> Project:
        project = repository.get_archived(by)

        if not self.is_satisfied_by(project):
            raise ValueError(f"Project {by} is not archived")

        return project


class ActiveProjectSpecification(Specification[Project]):
    def __init__(self):
        self._specification = ~ArchivedProjectSpecification() & ~DeletedProjectSpecification()

    def is_satisfied_by(self, candidate: Project) -> bool:
        return self._specification.is_satisfied_by(candidate)

    def satisfied_from(self, repository: AbstractProjectRepository, *, by: ProjectID) -> Project:
        project = repository.get_active(by)

        # TODO: Add a better exception
        if not self.is_satisfied_by(project):
            raise ValueError(f"Project {by} is not active")

        return project
