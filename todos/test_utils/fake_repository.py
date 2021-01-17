from typing import List, Optional

from todos.domain.models import Project
from todos.interfaces.abstract_repository import AbstractRepository


class FakeRepository(AbstractRepository):
    def __init__(self, *, projects: List[Project]):
        self._projects = projects

    def get(self, id: Optional[int] = None) -> Optional[Project]:
        if id is not None:
            return next(
                iter(filter(lambda project: project.id == id, self._projects)), None
            )

        return self._projects[0] if len(self._projects) > 0 else None

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
