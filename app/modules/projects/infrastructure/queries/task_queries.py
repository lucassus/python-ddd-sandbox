from sqlalchemy import select
from sqlalchemy.sql.expression import and_

from app.infrastructure.base_query import BaseQuery
from app.infrastructure.tables import tasks_table
from app.modules.projects.application.queries.task_queries import FindTaskQueryProtocol, ListTasksQueryProtocol
from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.task import TaskNumber


class ListTasksQuery(BaseQuery, ListTasksQueryProtocol):
    def __call__(self, *, project_id: ProjectID):
        query = select(tasks_table).where(tasks_table.c.project_id == project_id)
        return self._all_from(query)


class FindTaskQuery(BaseQuery, FindTaskQueryProtocol):
    def __call__(self, *, project_id: ProjectID, number: TaskNumber):
        query = select(tasks_table).where(
            and_(
                tasks_table.c.project_id == project_id,
                tasks_table.c.number == number,
            )
        )

        return self._first_from(query)
