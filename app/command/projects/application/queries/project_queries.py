import abc
from typing import Optional

from app.command.projects.domain.project import ProjectID
from app.command.shared_kernel.entities.user_id import UserID

# TODO: Move schemas here


class AbstractFetchProjectsQuery(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __call__(self, user_id: Optional[UserID] = None):
        raise NotImplementedError()


class AbstractFindProjectQuery(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __call__(self, *, id: ProjectID):
        raise NotImplementedError()
