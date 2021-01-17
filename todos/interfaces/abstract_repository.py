import abc
from typing import List, Optional

from todos.domain.models import Project


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, id: int) -> Optional[Project]:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[Project]:
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, task: Project) -> None:
        raise NotImplementedError
