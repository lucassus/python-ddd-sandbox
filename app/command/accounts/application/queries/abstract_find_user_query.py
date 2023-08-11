import abc
from typing import Optional

from app.base_schema import BaseSchema


class Project(BaseSchema):
    id: int
    name: str


class UserDetails(BaseSchema):
    id: int
    email: str
    projects: list[Project]


class AbstractFindUserQuery:
    @abc.abstractmethod
    def __call__(self, *, id: int) -> Optional[UserDetails]:
        # TODO: Do not use Optional, raise an error when not found, less work for the caller
        raise NotImplementedError()
