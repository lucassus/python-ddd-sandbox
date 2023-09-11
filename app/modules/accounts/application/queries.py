from dataclasses import dataclass

from app.modules.shared_kernel.entities.user_id import UserID
from app.modules.shared_kernel.errors import EntityNotFoundError
from app.shared.base_schema import BaseSchema
from app.shared.query import Query
from app.shared.user_id_field import UserIDField


@dataclass(frozen=True)
class GetUser(Query):
    class Result(BaseSchema):
        class Project(BaseSchema):
            id: int
            name: str

        id: UserIDField
        email: str
        projects: list[Project]

    class NotFoundError(EntityNotFoundError):
        def __init__(self, id: UserID):
            super().__init__(f"User with id {id} not found")

    user_id: UserID
    include_projects: bool = True
