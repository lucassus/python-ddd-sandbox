from sqlalchemy.orm.session import Session

from app.modules.projects.domain.entities import Project
from app.modules.projects.domain.errors import ProjectNotFoundError
from app.modules.projects.domain.ports import AbstractRepository


class Repository(AbstractRepository):
    def __init__(self, session: Session):
        self._session = session

    def get(self, id: int) -> Project:
        project = self._session.query(Project).get(id)

        if project is None:
            raise ProjectNotFoundError(id)

        return project

    def list(self) -> list[Project]:
        return self._session.query(Project).all()

    def create(self, project: Project) -> Project:
        self._session.add(project)
        return project
