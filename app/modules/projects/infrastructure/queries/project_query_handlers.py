from sqlalchemy import select

from app.infrastructure.base_sql_query_handler import BaseSQLQueryHandler
from app.infrastructure.tables import projects_table
from app.modules.projects.application.queries import GetProject, ListProjects


class ListProjectsQueryHandler(BaseSQLQueryHandler[ListProjects, ListProjects.Result]):
    async def __call__(self, query: ListProjects) -> ListProjects.Result:
        projects = await self._all_from(
            select(
                projects_table.c.id,
                projects_table.c.name,
            )
            .select_from(projects_table)
            .where(projects_table.c.user_id == query.user_id)
        )

        return ListProjects.Result(projects=projects)


class GetProjectQueryHandler(BaseSQLQueryHandler[GetProject, GetProject.Result]):
    async def __call__(self, query: GetProject) -> GetProject.Result:
        stmt = select(projects_table).where(projects_table.c.id == query.id)
        project = await self._first_from(stmt)

        if project is None:
            raise GetProject.NotFoundError(query.id)

        return GetProject.Result.model_validate(project)
