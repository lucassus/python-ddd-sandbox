from sqlalchemy.orm.session import Session

from app.modules.projects.application.ports.abstract_project_repository import AbstractProjectRepository
from app.modules.projects.entities.errors import ProjectNotFoundError
from app.modules.projects.entities.project import Project, ProjectID


class SQLAProjectRepository(AbstractProjectRepository):
    def __init__(self, session: Session):
        self._session = session

    def get(self, id: ProjectID) -> Project:
        project = self._session.get(Project, id)

        if project is None:
            raise ProjectNotFoundError(id)

        return project

    def create(self, project: Project) -> Project:
        self._session.add(project)
        return project
