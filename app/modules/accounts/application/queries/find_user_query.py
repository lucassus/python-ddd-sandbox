from typing import Protocol

from app.modules.shared_kernel.base_schema import BaseSchema
from app.modules.shared_kernel.entities.user_id import UserID


# TODO: It seems to be redundant...
class GetUserQuery(Protocol):
    class Result(BaseSchema):
        class Project(BaseSchema):
            id: int
            name: str

        id: int
        email: str
        projects: list[Project]

    class NotFoundError(Exception):
        def __init__(self, id: UserID):
            super().__init__(f"User with id {id} not found")

    def __call__(self, id: UserID) -> Result:
        ...
