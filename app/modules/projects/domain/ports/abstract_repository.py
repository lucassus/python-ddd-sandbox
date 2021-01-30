import abc
from typing import List

from app.modules.projects.domain.entities import Project


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, id: int) -> Project:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[Project]:
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, project: Project) -> None:
        raise NotImplementedError
