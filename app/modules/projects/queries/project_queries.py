from sqlalchemy import select

from app.infrastructure.base_query import BaseSQLQuery
from app.infrastructure.tables import projects_table
from app.modules.projects.domain.project import ProjectID
from app.modules.shared_kernel.base_schema import BaseSchema
from app.modules.shared_kernel.entities.user_id import UserID


class ListProjectsQuery(BaseSQLQuery):
    class Result(BaseSchema):
        class Project(BaseSchema):
            id: int
            name: str

        projects: list[Project]

    def __call__(self, user_id: UserID) -> Result:
        projects = self._all_from(
            select(
                projects_table.c.id,
                projects_table.c.name,
            )
            .select_from(projects_table)
            .where(projects_table.c.user_id == user_id)
        )

        return ListProjectsQuery.Result(projects=projects)


class GetProjectQuery(BaseSQLQuery):
    class Result(BaseSchema):
        id: int
        name: str

    class NotFoundError(Exception):
        def __init__(self, id: ProjectID):
            super().__init__(f"Project with id {id} not found")

    def __call__(self, id: ProjectID) -> Result:
        query = select(projects_table).where(projects_table.c.id == id)
        project = self._first_from(query)

        if project is None:
            raise GetProjectQuery.NotFoundError(id)

        return GetProjectQuery.Result.model_validate(project)
