from sqlalchemy.sql.expression import and_

from app.infrastructure.tables import tasks_table
from app.query.queries.abstract_query import AbstractQuery


class FetchTasksQuery(AbstractQuery):
    def __call__(self, *, project_id: int):
        query = tasks_table.select().where(tasks_table.c.project_id == project_id)

        return self._database.fetch_all(query)


class FindTaskQuery(AbstractQuery):
    def __call__(self, *, project_id: int, task_id: int):
        query = tasks_table.select().where(
            and_(
                tasks_table.c.project_id == project_id,
                tasks_table.c.id == task_id,
            )
        )

        return self._database.fetch_one(query)
