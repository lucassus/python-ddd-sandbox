import abc
from datetime import date
from typing import List, Optional, overload

from todos.domain.models import Todo


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, id: int) -> Optional[Todo]:
        pass

    @abc.abstractmethod
    def list(self) -> List[Todo]:
        pass

    @overload
    def update(self, id: int) -> Todo:
        ...

    @overload
    def update(
        self, id: int, name: Optional[str] = None, completed_at: Optional[date] = None
    ) -> Todo:
        ...

    @abc.abstractmethod
    def update(self, id: int, *args, **kwargs) -> Todo:
        pass

    @abc.abstractmethod
    def create(self, name: str) -> Todo:
        pass
