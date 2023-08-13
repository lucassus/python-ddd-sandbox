from typing import Optional

from sqlalchemy import select

from app.infrastructure.base_query import BaseSQLQuery
from app.infrastructure.tables import projects_table
from app.modules.projects.application.queries.project_queries import GetProjectQuery, ListProjectsQuery
from app.modules.projects.domain.project import ProjectID
from app.modules.shared_kernel.entities.user_id import UserID


class ListProjectsSQLSQLQuery(BaseSQLQuery, ListProjectsQuery):
    def __call__(self, *, user_id: Optional[UserID] = None) -> ListProjectsQuery.Result:
        query = select(
            projects_table.c.id,
            projects_table.c.name,
        ).select_from(projects_table)

        if user_id is not None:
            query.where(projects_table.c.user_id == user_id)

        projects = self._connection.execute(query).fetchall()

        return ListProjectsQuery.Result(
            projects=[ListProjectsQuery.Result.Project.model_validate(project) for project in projects],
        )


class GetProjectSQLSQLQuery(BaseSQLQuery, GetProjectQuery):
    def __call__(self, *, id: ProjectID) -> GetProjectQuery.Result:
        query = select(projects_table).where(projects_table.c.id == id)
        project = self._first_from(query)

        return GetProjectQuery.Result.model_validate(project)
