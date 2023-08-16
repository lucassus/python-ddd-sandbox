from typing import Any

from sqlalchemy import Select, and_, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from app.infrastructure.tables import projects_table
from app.modules.projects.application.ports.abstract_project_repository import AbstractProjectRepository
from app.modules.projects.domain.errors import ProjectNotFoundError
from app.modules.projects.domain.project import Project, ProjectID


class ProjectRepository(AbstractProjectRepository):
    def __init__(self, session: Session):
        self._session = session

    def create(self, project: Project) -> Project:
        self._session.add(project)
        return project

    def _project_query(self, id: ProjectID) -> Select[Any]:
        return select(Project).where(
            projects_table.c.id == id,
        )

    def get(self, id: ProjectID) -> Project:
        query = self._project_query(id).where(
            projects_table.c.archived_at.is_(None),
        )

        try:
            project = self._session.execute(query).scalar_one()
        except NoResultFound as e:
            raise ProjectNotFoundError(id) from e

        return project

    def get_archived(self, id: ProjectID) -> Project:
        query = self._project_query(id).where(
            and_(
                projects_table.c.archived_at.isnot(None),
                projects_table.c.deleted_at.is_(None),
            )
        )

        try:
            project = self._session.execute(query).scalar_one()
        except NoResultFound as e:
            raise ProjectNotFoundError(id) from e

        return project
