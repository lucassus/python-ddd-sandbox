from typing import List, Optional

from todos.domain.models import Project
from todos.interfaces.abstract_repository import AbstractRepository


class FakeRepository(AbstractRepository):
    def __init__(self, *, projects: List[Project]):
        self._projects = projects

    def get(self, id: int) -> Optional[Project]:
        try:
            return next(project for project in self._projects if project.id == id)
        except StopIteration:
            return None

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
