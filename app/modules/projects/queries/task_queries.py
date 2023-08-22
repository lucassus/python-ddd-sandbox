from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.sql.expression import and_

from app.infrastructure.base_query import BaseSQLQuery
from app.infrastructure.tables import tasks_table
from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.task import TaskNumber
from app.modules.shared_kernel.base_schema import BaseSchema
from app.modules.shared_kernel.entities.user_id import UserID
from app.modules.shared_kernel.errors import EntityNotFoundError


class ListTasksQuery(BaseSQLQuery):
    class Result(BaseSchema):
        class Task(BaseSchema):
            number: int
            name: str
            completed_at: Optional[datetime] = None

        tasks: list[Task]

    def __call__(self, project_id: ProjectID) -> Result:
        query = select(tasks_table).where(tasks_table.c.project_id == project_id)
        tasks = self._all_from(query)

        return ListTasksQuery.Result(tasks=tasks)


class GetTaskQuery(BaseSQLQuery):
    class Result(BaseSchema):
        number: int
        name: str
        created_by: Optional[UserID]
        completed_at: Optional[datetime]

    class NotFoundError(EntityNotFoundError):
        def __init__(self, project_id: ProjectID, number: TaskNumber):
            super().__init__(f"Task with number {number} in project with id {project_id} not found")

    def __call__(self, project_id: ProjectID, number: TaskNumber):
        task = self._first_from(
            select(
                tasks_table.c.id,
                tasks_table.c.number,
                tasks_table.c.name,
                tasks_table.c.created_by,
                tasks_table.c.completed_at,
            )
            .select_from(tasks_table)
            .where(
                and_(
                    tasks_table.c.project_id == project_id,
                    tasks_table.c.number == number,
                )
            )
        )

        if task is None:
            raise GetTaskQuery.NotFoundError(project_id, number)

        return GetTaskQuery.Result.model_validate(task)
