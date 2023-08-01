from typing import Iterator

from app.command.projects.application.ports.abstract_project_repository import AbstractProjectRepository
from app.command.projects.entities.errors import ProjectNotFoundError
from app.command.projects.entities.project import Project, ProjectID


def _project_id_generator() -> Iterator[ProjectID]:
    last_id = 1

    while True:
        yield ProjectID(last_id)
        last_id += 1


class FakeProjectRepository(AbstractProjectRepository):
    _projects: list[Project]

    def __init__(self):
        self._project_id = _project_id_generator()
        self._projects = []

    def create(self, project: Project) -> Project:
        project.id = next(self._project_id)
        self._projects.append(project)

        return project

    def get(self, id: ProjectID) -> Project:
        try:
            return next(project for project in self._projects if project.id == id and not project.archived)
        except StopIteration:
            raise ProjectNotFoundError(id)

    def get_archived(self, id: ProjectID) -> Project:
        try:
            return next(project for project in self._projects if project.id == id and project.archived)
        except StopIteration:
            raise ProjectNotFoundError(id)
