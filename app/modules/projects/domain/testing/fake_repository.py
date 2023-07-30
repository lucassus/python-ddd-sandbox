from app.modules.projects.domain.entities import Project, ProjectID, TaskID
from app.modules.projects.domain.errors import ProjectNotFoundError
from app.modules.projects.domain.ports import AbstractRepository


def _project_id_generator():
    id = ProjectID(1)
    while True:
        yield id
        id = ProjectID(id + 1)


def _task_id_generator():
    id = TaskID(1)
    while True:
        yield id
        id = TaskID(id + 1)


class FakeRepository(AbstractRepository):
    _projects: list[Project]

    def __init__(self):
        self._project_id = _project_id_generator()
        self._task_id = _task_id_generator()
        self._projects = []

    def get(self, id: ProjectID) -> Project:
        for project in self._projects:
            if project.id == id:
                return project

        raise ProjectNotFoundError(id)

    def create(self, project: Project) -> Project:
        project.id = next(self._project_id)
        for task in project.tasks:
            task.id = next(self._task_id)

        self._projects.append(project)

        return project
