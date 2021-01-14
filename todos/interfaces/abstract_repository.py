import abc
from typing import List, Optional

from todos.domain.models import Task


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, id: int) -> Optional[Task]:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[Task]:
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, task: Task) -> None:
        raise NotImplementedError
