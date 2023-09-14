from sqlalchemy import select
from sqlalchemy.sql.expression import and_

from app.infrastructure.base_sql_query_handler import BaseSQLQueryHandler
from app.infrastructure.tables import tasks_table
from app.modules.projects.application.queries import GetTask, ListTasks


class ListTasksQueryHandler(BaseSQLQueryHandler[ListTasks, ListTasks.Result]):
    async def __call__(self, query: ListTasks) -> ListTasks.Result:
        stmt = select(tasks_table).where(tasks_table.c.project_id == query.project_id)
        tasks = await self._all_from(stmt)

        return ListTasks.Result(tasks=tasks)


class GetTaskQueryHandler(BaseSQLQueryHandler[GetTask, GetTask.Result]):
    async def __call__(self, query: GetTask) -> GetTask.Result:
        task = await self._first_from(
            select(
                tasks_table.c.id,
                tasks_table.c.number,
                tasks_table.c.name,
                tasks_table.c.completed_at,
            )
            .select_from(tasks_table)
            .where(
                and_(
                    tasks_table.c.project_id == query.project_id,
                    tasks_table.c.number == query.number,
                )
            )
        )

        if task is None:
            raise GetTask.NotFoundError(query.project_id, query.number)

        return GetTask.Result.model_validate(task)
