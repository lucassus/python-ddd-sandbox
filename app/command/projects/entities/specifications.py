from typing import TYPE_CHECKING

from app.command.shared_kernel.specification import Specification

if TYPE_CHECKING:
    from app.command.projects.entities.project import Project


class DeletedProjectSpecification(Specification["Project"]):
    def is_satisfied_by(self, project: "Project") -> bool:
        return project.deleted_at is not None


class ArchivedProjectSpecification(Specification["Project"]):
    def __init__(self):
        self._deleted_project_spec = DeletedProjectSpecification()

    def is_satisfied_by(self, candidate: "Project") -> bool:
        if self._deleted_project_spec.is_satisfied_by(candidate):
            return False

        return candidate.archived_at is not None


class ActiveProjectSpecification(Specification["Project"]):
    def __init__(self):
        self._specification = ~ArchivedProjectSpecification() & ~DeletedProjectSpecification()

    def is_satisfied_by(self, candidate: "Project") -> bool:
        return self._specification.is_satisfied_by(candidate)
