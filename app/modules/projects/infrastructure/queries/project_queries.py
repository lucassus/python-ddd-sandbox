from typing import Optional

from sqlalchemy import Connection, select

from app.infrastructure.tables import projects_table
from app.modules.projects.application.queries.project_queries import (
    AbstractFetchProjectsQuery,
    AbstractFindProjectQuery,
)
from app.modules.projects.domain.project import ProjectID
from app.modules.shared_kernel.entities.user_id import UserID


class FetchProjectsQuery(AbstractFetchProjectsQuery):
    def __init__(self, connection: Connection):
        # TODO: This is tedious, re-consider create a base class
        self._connection = connection

    def __call__(self, user_id: Optional[UserID] = None):
        query = select(projects_table)

        if user_id is not None:
            query.where(projects_table.c.user_id == user_id)

        return list(self._connection.execute(query).all())


class FindProjectQuery(AbstractFindProjectQuery):
    def __init__(self, connection: Connection):
        self._connection = connection

    def __call__(self, *, id: ProjectID):
        query = select(projects_table).where(projects_table.c.id == id)
        return self._connection.execute(query).first()
