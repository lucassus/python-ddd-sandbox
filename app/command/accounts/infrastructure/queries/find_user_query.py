from typing import Any

from sqlalchemy import Connection, Executable, select

from app.command.accounts.application.queries.find_user_query_protocol import (
    FindUserQueryError,
    FindUserQueryProtocol,
    UserDetails,
)
from app.command.shared_kernel.entities.user_id import UserID
from app.infrastructure.tables import projects_table, users_table


# TODO: Bring back a base class for queries with connection and helper methods
class BaseQuery:
    def __init__(self, connection: Connection):
        self._connection = connection

    def _first_from(self, query: Executable) -> Any:
        return self._connection.execute(query).first()

    def _all_from(self, query: Executable) -> list[Any]:
        return list(self._connection.execute(query).all())


class FindUserQuery(BaseQuery, FindUserQueryProtocol):
    def __call__(self, *, id: UserID) -> UserDetails:
        query = select(users_table.c.id, users_table.c.email).select_from(users_table).where(users_table.c.id == id)
        user = self._first_from(query)

        if user is None:
            raise FindUserQueryError(id)

        query = (
            select(projects_table.c.id, projects_table.c.name)
            .select_from(projects_table)
            .where(projects_table.c.user_id == user.id)
        )
        projects = self._all_from(query)

        return UserDetails(
            **{
                **user._asdict(),
                "email": user.email.address,
                "projects": projects,
            }
        )
