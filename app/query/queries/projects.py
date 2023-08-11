from typing import Optional

from sqlalchemy import select

from app.command.shared_kernel.query import Query
from app.infrastructure.tables import projects_table


class FetchProjectsQuery(Query):
    def __call__(self, user_id: Optional[int] = None):
        query = select(projects_table)

        if user_id is not None:
            query.where(projects_table.c.user_id == user_id)

        return self._all_from(query)


class FindProjectQuery(Query):
    def __call__(self, *, id: int):
        query = select(projects_table).where(projects_table.c.id == id)
        return self._first_from(query)
