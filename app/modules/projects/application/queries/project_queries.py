from typing import Optional, Protocol

from app.modules.projects.domain.project import ProjectID
from app.modules.shared_kernel.base_schema import BaseSchema
from app.modules.shared_kernel.entities.user_id import UserID


class ListProjectsQuery(Protocol):
    class Result(BaseSchema):
        class Project(BaseSchema):
            id: int
            name: str

        projects: list[Project]

    def __call__(self, user_id: Optional[UserID] = None) -> Result:
        ...


class GetProjectQuery(Protocol):
    class Result(BaseSchema):
        id: int
        name: str

    class NotFoundError(Exception):
        def __init__(self, id: ProjectID):
            super().__init__(f"Project with id {id} not found")

    def __call__(self, id: ProjectID) -> Result:
        ...
