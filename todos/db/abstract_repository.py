import abc
from typing import List, Optional

from todos.domain.models.todo import Todo


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, id: int) -> Optional[Todo]:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[Todo]:
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, name: str) -> Todo:
        raise NotImplementedError
