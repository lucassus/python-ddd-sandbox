import abc
from datetime import date
from typing import List, Optional

from todos.domain.models import Todo


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, id: int) -> Optional[Todo]:
        pass

    @abc.abstractmethod
    def list(self) -> List[Todo]:
        pass

    @abc.abstractmethod
    def update(
        self,
        todo: Todo,
        name: Optional[str] = None,
        completed_at: Optional[date] = None,
    ) -> Todo:
        pass

    @abc.abstractmethod
    def create(self, name: str) -> Todo:
        pass
