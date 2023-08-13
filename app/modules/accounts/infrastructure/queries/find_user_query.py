from sqlalchemy import select

from app.infrastructure.base_query import BaseQuery
from app.infrastructure.tables import projects_table, users_table
from app.modules.accounts.application.queries.find_user_query import (
    FindUserQueryError,
    FindUserQueryProtocol,
    UserDetails,
)
from app.modules.shared_kernel.entities.user_id import UserID


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
