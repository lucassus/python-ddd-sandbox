from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.task import TaskNumber
from app.modules.shared_kernel.entities.user_id import UserID
from app.modules.shared_kernel.errors import EntityNotFoundError
from app.shared.base_schema import BaseSchema
from app.shared.query import Query


@dataclass(frozen=True)
class ListProjects(Query):
    class Result(BaseSchema):
        class Project(BaseSchema):
            id: int
            name: str

        projects: list[Project]

    user_id: UserID


@dataclass(frozen=True)
class GetProject(Query):
    class Result(BaseSchema):
        id: int
        name: str

    class NotFoundError(EntityNotFoundError):
        def __init__(self, id: ProjectID):
            super().__init__(f"Project with id {id} not found")

    id: ProjectID


@dataclass(frozen=True)
class ListTasks(Query):
    class Result(BaseSchema):
        class Task(BaseSchema):
            number: int
            name: str
            completed_at: Optional[datetime] = None

        tasks: list[Task]

    project_id: ProjectID


@dataclass(frozen=True)
class GetTask(Query):
    class Result(BaseSchema):
        number: int
        name: str
        completed_at: Optional[datetime]

    class NotFoundError(EntityNotFoundError):
        def __init__(self, project_id: ProjectID, number: TaskNumber):
            super().__init__(f"Task with number {number} in project with id {project_id} not found")

    project_id: ProjectID
    number: TaskNumber
