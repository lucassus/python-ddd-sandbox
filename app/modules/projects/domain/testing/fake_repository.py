from typing import Iterator

from app.modules.projects.domain.entities import Project, ProjectID
from app.modules.projects.domain.errors import ProjectNotFoundError
from app.modules.projects.domain.ports import AbstractRepository


def _project_id_generator() -> Iterator[ProjectID]:
    last_id = 1

    while True:
        last_id += 1
        yield ProjectID(last_id)


class FakeRepository(AbstractRepository):
    _projects: list[Project]

    def __init__(self):
        self._project_id = _project_id_generator()
        self._projects = []

    def get(self, id: ProjectID) -> Project:
        for project in self._projects:
            if project.id == id:
                return project

        raise ProjectNotFoundError(id)

    def create(self, project: Project) -> Project:
        project.id = next(self._project_id)
        self._projects.append(project)

        return project
