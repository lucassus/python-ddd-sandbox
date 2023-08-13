from typing import Optional

from sqlalchemy import select

from app.infrastructure.base_query import BaseQuery
from app.infrastructure.tables import projects_table
from app.modules.projects.application.queries.project_queries import FindProjectQueryProtocol, ListProjectsQueryProtocol
from app.modules.projects.domain.project import ProjectID
from app.modules.shared_kernel.entities.user_id import UserID


class ListProjectsQuery(BaseQuery, ListProjectsQueryProtocol):
    def __call__(self, user_id: Optional[UserID] = None):
        query = select(projects_table)

        if user_id is not None:
            query.where(projects_table.c.user_id == user_id)

        return self._all_from(query)


class FindProjectQuery(BaseQuery, FindProjectQueryProtocol):
    def __call__(self, *, id: ProjectID):
        query = select(projects_table).where(projects_table.c.id == id)
        return self._first_from(query)
