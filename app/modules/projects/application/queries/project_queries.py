from typing import Optional, Protocol

from app.modules.projects.domain.project import ProjectID
from app.modules.shared_kernel.base_schema import BaseSchema
from app.modules.shared_kernel.entities.user_id import UserID


class Project(BaseSchema):
    id: int
    name: str


class ListProjectsQueryProtocol(Protocol):
    def __call__(self, user_id: Optional[UserID] = None) -> list[Project]:
        ...


class FindProjectQueryProtocol(Protocol):
    def __call__(self, *, id: ProjectID) -> Project:
        ...
