from typing import Optional

from sqlalchemy import Connection, select

import app.command.accounts.application.queries.abstract_find_user_query
from app.command.accounts.application.queries.abstract_find_user_query import AbstractFindUserQuery, UserDetails
from app.infrastructure.tables import projects_table, users_table


# TODO: Write integration tests for this query
class FindUserQuery(AbstractFindUserQuery):
    def __init__(self, connection: Connection):
        self._connection = connection

    def __call__(self, *, id: int) -> Optional[UserDetails]:
        query = select(users_table.c.id, users_table.c.email).select_from(users_table).where(users_table.c.id == id)
        user = self._connection.execute(query).first()

        if user is None:
            return None  # TODO: Raise an exception

        query = (
            select(projects_table.c.id, projects_table.c.name)
            .select_from(projects_table)
            .where(projects_table.c.user_id == user.id)
        )
        projects = list(self._connection.execute(query).all())

        return app.command.accounts.application.queries.abstract_find_user_query.UserDetails(
            **{
                **user._asdict(),
                "email": user.email.address,
                "projects": projects,
            }
        )
