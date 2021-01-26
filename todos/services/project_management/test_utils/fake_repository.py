from typing import List

from todos.services.project_management.domain.entities import Project
from todos.services.project_management.domain.errors import ProjectNotFoundError
from todos.services.project_management.domain.ports import AbstractRepository


class FakeRepository(AbstractRepository):
    def __init__(self, *, projects: List[Project]):
        self._projects = projects

    def get(self, id: int) -> Project:
        for project in self._projects:
            if project.id == id:
                return project

        raise ProjectNotFoundError(id)

    def create(self, project: Project) -> None:
        project.id = self._get_next_id()
        self._projects.append(project)

    def list(self) -> List[Project]:
        return self._projects

    def _get_next_id(self) -> int:
        ids = [project.id for project in self._projects if project.id is not None]

        if len(ids) == 0:
            return 1

        return max(ids) + 1
