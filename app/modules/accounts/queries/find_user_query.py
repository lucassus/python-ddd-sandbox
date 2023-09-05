from sqlalchemy import select

from app.infrastructure.base_query import BaseSQLQuery
from app.infrastructure.tables import projects_table, users_table
from app.modules.shared_kernel.entities.user_id import UserID
from app.modules.shared_kernel.errors import EntityNotFoundError
from app.shared.base_schema import BaseSchema
from app.shared.user_id_field import UserIDField


class GetUserQuery(BaseSQLQuery):
    class Result(BaseSchema):
        class Project(BaseSchema):
            id: int
            name: str

        id: UserIDField
        email: str
        projects: list[Project]

    class NotFoundError(EntityNotFoundError):
        def __init__(self, id: UserID):
            super().__init__(f"User with id {id} not found")

    # TODO: Add include_projects flag
    def __call__(self, id: UserID) -> Result:
        user = self._first_from(
            # fmt: off
            select(users_table.c.id, users_table.c.email)
            .select_from(users_table)
            .where(users_table.c.id == id)
            # fmt: on
        )

        if user is None:
            raise GetUserQuery.NotFoundError(id)

        projects = self._all_from(
            select(projects_table.c.id, projects_table.c.name)
            .select_from(projects_table)
            .where(projects_table.c.user_id == user.id)
        )

        return GetUserQuery.Result(
            **{
                **user._asdict(),
                "email": str(user.email),
                "projects": projects,
            }
        )
