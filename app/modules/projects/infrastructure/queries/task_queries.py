from sqlalchemy import Connection, select
from sqlalchemy.sql.expression import and_

from app.infrastructure.tables import tasks_table
from app.modules.projects.application.queries.task_queries import AbstractFetchTasksQuery, AbstractFindTaskQuery
from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.task import TaskNumber


class FetchTasksQuery(AbstractFetchTasksQuery):
    def __init__(self, connection: Connection):
        self._connection = connection

    def __call__(self, *, project_id: ProjectID):
        query = select(tasks_table).where(tasks_table.c.project_id == project_id)
        return list(self._connection.execute(query).all())


class FindTaskQuery(AbstractFindTaskQuery):
    def __init__(self, connection: Connection):
        self._connection = connection

    def __call__(self, *, project_id: ProjectID, number: TaskNumber):
        query = select(tasks_table).where(
            and_(
                tasks_table.c.project_id == project_id,
                tasks_table.c.number == number,
            )
        )

        return self._connection.execute(query).first()
