from typing import Optional

from app.infrastructure.tables import projects_table
from app.query.queries.abstract_query import AbstractQuery


class FetchProjectsQuery(AbstractQuery):
    def __call__(self, user_id: Optional[int] = None):
        query = projects_table.select()

        if user_id is not None:
            query.where(projects_table.c.user_id == user_id)

        result = self._connection.execute(query)
        return result.all()


class FindProjectQuery(AbstractQuery):
    def __call__(self, *, id: int):
        query = projects_table.select().where(projects_table.c.id == id)

        result = self._connection.execute(query)
        return result.first()
