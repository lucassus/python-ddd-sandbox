from sqlalchemy import Connection, select

from app.command.accounts.application.queries.abstract_find_user_query import (
    AbstractFindUserQuery,
    FindUserQueryError,
    UserDetails,
)
from app.infrastructure.tables import projects_table, users_table


class FindUserQuery(AbstractFindUserQuery):
    def __init__(self, connection: Connection):
        self._connection = connection

    def __call__(self, *, id: int) -> UserDetails:
        query = select(users_table.c.id, users_table.c.email).select_from(users_table).where(users_table.c.id == id)
        user = self._connection.execute(query).first()

        if user is None:
            raise FindUserQueryError(id)  # TODO: Find a better name for this exception

        query = (
            select(projects_table.c.id, projects_table.c.name)
            .select_from(projects_table)
            .where(projects_table.c.user_id == user.id)
        )
        projects = list(self._connection.execute(query).all())

        return UserDetails(
            **{
                **user._asdict(),
                "email": user.email.address,
                "projects": projects,
            }
        )
