from typing import Optional

from app.modules.projects.domain.entities import Project
from app.modules.projects.domain.errors import ProjectNotFoundError
from app.modules.projects.domain.ports import AbstractRepository


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

    def create(self, project: Project) -> None:
        project.id = self._get_next_id()
        self._projects.append(project)

    def _get_next_id(self) -> int:
        ids = [project.id for project in self._projects if project.id is not None]

        if len(ids) == 0:
            return 1

        return max(ids) + 1
