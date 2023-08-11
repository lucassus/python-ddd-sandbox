from typing import Optional

from sqlalchemy import select

from app.command.accounts.application.queries import schemas
from app.command.accounts.application.queries.abstract_find_user_query import AbstractFindUserQuery
from app.infrastructure.tables import projects_table, users_table


# TODO: Write integration tests for this query
class FindUserQuery(AbstractFindUserQuery):
    def __call__(self, *, id: int) -> Optional[schemas.UserDetails]:
        query = select(users_table.c.id, users_table.c.email).select_from(users_table).where(users_table.c.id == id)
        user = self._first_from(query)

        if user is None:
            return None  # TODO: Raise an exception

        query = (
            select(projects_table.c.id, projects_table.c.name)
            .select_from(projects_table)
            .where(projects_table.c.user_id == user.id)
        )
        projects = self._all_from(query)

        return schemas.UserDetails(
            **{
                **user._asdict(),
                "email": user.email.address,
                "projects": projects,
            }
        )
