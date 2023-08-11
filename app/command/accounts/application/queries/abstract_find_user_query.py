import abc

from app.base_schema import BaseSchema


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


class AbstractFindUserQuery:
    @abc.abstractmethod
    def __call__(self, *, id: int) -> UserDetails:
        raise NotImplementedError()
