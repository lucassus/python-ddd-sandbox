from sqlalchemy import select

from app.infrastructure.base_sql_query_handler import BaseSQLQueryHandler
from app.infrastructure.tables import projects_table, users_table
from app.modules.accounts.application.queries import GetUser


class GetUserQueryHandler(BaseSQLQueryHandler[GetUser, GetUser.Result]):
    def __call__(self, query: GetUser) -> GetUser.Result:
        user_id = query.user_id

        user = self._first_from(
            # fmt: off
            select(users_table.c.id, users_table.c.email)
            .select_from(users_table)
            .where(users_table.c.id == user_id)
            # fmt: on
        )

        if user is None:
            raise GetUser.NotFoundError(user_id)

        data = {"id": user.id, "email": user.email}

        if query.include_projects:
            projects = self._all_from(
                select(projects_table.c.id, projects_table.c.name)
                .select_from(projects_table)
                .where(projects_table.c.user_id == user_id)
            )

            data["projects"] = projects

        return GetUser.Result(
            **{
                "id": user.id,
                "email": str(user.email),
                "projects": data["projects"],
            }
        )
