from sqlalchemy.orm.session import Session

from app.command.projects.application.ports.abstract_project_repository import AbstractProjectRepository
from app.command.projects.entities.errors import ProjectNotFoundError
from app.command.projects.entities.project import Project, ProjectID


class SQLAProjectRepository(AbstractProjectRepository):
    def __init__(self, session: Session):
        self._session = session

    def create(self, project: Project) -> Project:
        self._session.add(project)
        return project

    def get(self, id: ProjectID) -> Project:
        project = self._session.get(Project, id)

        if project is None or project.archived:
            raise ProjectNotFoundError(id)

        return project

    def get_archived(self, id: ProjectID) -> Project:
        pass