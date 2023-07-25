from typing import Optional

from app.infrastructure.tables import projects_table, users_table
from app.query import schemas
from app.query.queries.abstract_query import AbstractQuery


class FindUserQuery(AbstractQuery):
    def __call__(self, *, id: int) -> Optional[schemas.User]:
        query = users_table.select().where(users_table.c.id == id)
        user = self._first_from(query)

        if user is None:
            return None

        query = projects_table.select().where(projects_table.c.user_id == id)
        projects = self._all_from(query)

        return schemas.User(
            **{
                **user._asdict(),
                "email": user.email.address,
                "projects": [schemas.Project(**project._asdict()) for project in projects],
            }
        )
