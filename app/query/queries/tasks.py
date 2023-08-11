from sqlalchemy import select
from sqlalchemy.sql.expression import and_

from app.command.shared_kernel.query import Query
from app.infrastructure.tables import tasks_table


class FetchTasksQuery(Query):
    def __call__(self, *, project_id: int):
        query = select(tasks_table).where(tasks_table.c.project_id == project_id)
        return self._all_from(query)


class FindTaskQuery(Query):
    def __call__(self, *, project_id: int, number: int):
        query = select(tasks_table).where(
            and_(
                tasks_table.c.project_id == project_id,
                tasks_table.c.number == number,
            )
        )

        return self._first_from(query)
