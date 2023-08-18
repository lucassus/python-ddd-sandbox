from sqlalchemy import select

from app.infrastructure.base_query import BaseSQLQuery
from app.infrastructure.tables import projects_table
from app.modules.projects.application.queries.project_queries import GetProjectQuery, ListProjectsQuery
from app.modules.projects.domain.project import ProjectID
from app.modules.shared_kernel.entities.user_id import UserID


class ListProjectsSQLSQLQuery(BaseSQLQuery, ListProjectsQuery):
    def __call__(self, user_id: UserID) -> ListProjectsQuery.Result:
        query = (
            select(
                projects_table.c.id,
                projects_table.c.name,
            )
            .select_from(projects_table)
            .where(projects_table.c.user_id == user_id)
        )

        projects = self._connection.execute(query).fetchall()

        return ListProjectsQuery.Result(projects=projects)


class GetProjectSQLSQLQuery(BaseSQLQuery, GetProjectQuery):
    def __call__(self, id: ProjectID) -> GetProjectQuery.Result:
        query = select(projects_table).where(projects_table.c.id == id)
        project = self._first_from(query)

        if project is None:
            raise GetProjectQuery.NotFoundError(id)

        return GetProjectQuery.Result.model_validate(project)
