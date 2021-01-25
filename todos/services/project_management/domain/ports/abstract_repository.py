import abc
from typing import List

from todos.services.project_management.domain.entities import Project


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
