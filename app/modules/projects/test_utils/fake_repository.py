from typing import Optional

from app.modules.projects.domain.entities import Project, ProjectID
from app.modules.projects.domain.errors import ProjectNotFoundError
from app.modules.projects.domain.ports import AbstractRepository


# TODO: Move to domain/testing
class FakeRepository(AbstractRepository):
    def __init__(self, *, projects: Optional[list[Project]] = None):
        if projects is None:
            projects = []

        self._projects = projects

    def get(self, id: int) -> Project:
        for project in self._projects:
            if project.id == id:
                return project

        raise ProjectNotFoundError(id)

    def create(self, project: Project) -> Project:
        project.id = self._get_next_id()
        self._projects.append(project)

        return project

    def _get_next_id(self) -> ProjectID:
        ids = [project.id for project in self._projects if project.id is not None]
        return ProjectID(max(ids, default=0) + 1)
