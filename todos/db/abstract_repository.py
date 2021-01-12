import abc
from typing import List, Optional

from todos.domain.models.todo import Todo


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, id: int) -> Optional[Todo]:
        pass

    @abc.abstractmethod
    def list(self) -> List[Todo]:
        pass

    @abc.abstractmethod
    def create(self, todo: Todo) -> None:
        pass
