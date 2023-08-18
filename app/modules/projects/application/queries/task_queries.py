from datetime import datetime
from typing import Optional, Protocol

from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.task import TaskNumber
from app.modules.shared_kernel.base_schema import BaseSchema
from app.modules.shared_kernel.entities.user_id import UserID


class ListTasksQuery(Protocol):
    class Result(BaseSchema):
        class Task(BaseSchema):
            number: int
            name: str
            completed_at: Optional[datetime] = None

        tasks: list[Task]

    def __call__(self, project_id: ProjectID) -> Result:
        ...


class GetTaskQuery(Protocol):
    class Result(BaseSchema):
        number: int
        name: str
        created_by: Optional[UserID]
        completed_at: Optional[datetime]

    class NotFoundError(Exception):
        def __init__(self, project_id: ProjectID, number: TaskNumber):
            super().__init__(f"Task with number {number} in project with id {project_id} not found")

    def __call__(self, project_id: ProjectID, number: TaskNumber) -> Result:
        ...
