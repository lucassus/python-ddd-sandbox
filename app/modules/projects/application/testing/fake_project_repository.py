from typing import Iterator

from app.modules.projects.application.ports.abstract_project_repository import AbstractProjectRepository
from app.modules.projects.domain.errors import ProjectNotFoundError
from app.modules.projects.domain.project import Project, ProjectID


def _project_id_generator() -> Iterator[ProjectID]:
    last_id = 1

    while True:
        yield ProjectID(last_id)
        last_id += 1


class FakeProjectRepository(AbstractProjectRepository):
    _projects_by_id: dict[ProjectID, Project]

    def __init__(self):
        super().__init__()
        self._project_id = _project_id_generator()
        self._projects_by_id = {}

    def _create(self, project: Project) -> Project:
        project._id = next(self._project_id)
        self._projects_by_id[project.id] = project

        return project

    def _get(self, id: ProjectID) -> Project:
        project = self._projects_by_id.get(id)

        if project is None or project.archived:
            raise ProjectNotFoundError(id)

        return project

    def _get_archived(self, id: ProjectID) -> Project:
        project = self._projects_by_id.get(id)

        if project is None or not project.archived:
            raise ProjectNotFoundError(id)

        return project
