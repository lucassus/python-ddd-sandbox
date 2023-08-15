from sqlalchemy import select
from sqlalchemy.sql.expression import and_

from app.infrastructure.base_query import BaseSQLQuery
from app.infrastructure.tables import tasks_table
from app.modules.projects.application.queries.task_queries import GetTaskQuery, ListTasksQuery
from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.task import TaskNumber


class ListTasksSQLQuery(BaseSQLQuery, ListTasksQuery):
    def __call__(self, *, project_id: ProjectID):
        query = select(tasks_table).where(tasks_table.c.project_id == project_id)

        tasks = self._connection.execute(query).all()
        return ListTasksSQLQuery.Result(tasks=tasks)


class GetTaskSQLQuery(BaseSQLQuery, GetTaskQuery):
    def __call__(self, *, project_id: ProjectID, number: TaskNumber):
        query = select(tasks_table).where(
            and_(
                tasks_table.c.project_id == project_id,
                tasks_table.c.number == number,
            )
        )

        task = self._first_from(query)
        return GetTaskQuery.Result.model_validate(task)