from datetime import datetime
from typing import Optional, Protocol

from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.task import TaskNumber
from app.modules.shared_kernel.base_schema import BaseSchema


class Task(BaseSchema):
    number: int
    name: str
    completed_at: Optional[datetime] = None


class ListTasksQueryProtocol(Protocol):
    def __call__(self, *, project_id: ProjectID) -> list[Task]:
        ...


class FindTaskQueryProtocol(Protocol):
    def __call__(self, *, project_id: ProjectID, number: TaskNumber) -> Task:
        ...
