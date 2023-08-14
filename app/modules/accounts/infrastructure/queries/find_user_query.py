from sqlalchemy import select

from app.infrastructure.base_query import BaseSQLQuery
from app.infrastructure.tables import projects_table, users_table
from app.modules.accounts.application.queries.find_user_query import GetUserQuery, GetUserQueryError
from app.modules.shared_kernel.entities.user_id import UserID


class GetUserSQLQuery(BaseSQLQuery, GetUserQuery):
    def __call__(self, *, id: UserID) -> GetUserQuery.Result:
        query = select(users_table.c.id, users_table.c.email).select_from(users_table).where(users_table.c.id == id)
        user = self._first_from(query)

        if user is None:
            raise GetUserQueryError(id)

        query = (
            select(projects_table.c.id, projects_table.c.name)
            .select_from(projects_table)
            .where(projects_table.c.user_id == user.id)
        )
        projects = self._connection.execute(query).all()

        return GetUserQuery.Result(
            **{
                **user._asdict(),
                "email": str(user.email),
                "projects": projects,
            }
        )
