from sqlalchemy import select
from sqlalchemy.sql.expression import and_

from app.infrastructure.tables import tasks_table
from app.query.queries.abstract_query import AbstractQuery


class FetchTasksQuery(AbstractQuery):
    def __call__(self, *, project_id: int):
        query = select(tasks_table).where(tasks_table.c.project_id == project_id)
        return self._all_from(query)


class FindTaskQuery(AbstractQuery):
    def __call__(self, *, project_id: int, number: int):
        query = select(tasks_table).where(
            and_(
                tasks_table.c.project_id == project_id,
                tasks_table.c.number == number,
            )
        )

        return self._first_from(query)
