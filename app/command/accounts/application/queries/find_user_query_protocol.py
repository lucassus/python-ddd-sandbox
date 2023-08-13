from typing import Protocol

from app.command.shared_kernel.base_schema import BaseSchema
from app.command.shared_kernel.entities.user_id import UserID


class UserDetails(BaseSchema):
    class Project(BaseSchema):
        id: int
        name: str

    id: int
    email: str
    projects: list[Project]


class FindUserQueryError(Exception):
    def __init__(self, id: int):
        super().__init__(f"User with id {id} not found")


class FindUserQueryProtocol(Protocol):
    def __call__(self, *, id: UserID) -> UserDetails:
        ...
