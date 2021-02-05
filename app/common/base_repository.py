import abc
from typing import Generic, TypeVar

from app.common.base_aggregate import BaseAggregate

T = TypeVar("T", bound=BaseAggregate)


# TODO: Learn more about generics, multiple inheritance and abc
# TODO: abc cheat sheet
class BaseRepository(Generic[T], abc.ABC):
    @abc.abstractmethod
    def create(self, entity: T) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int) -> T:
        raise NotImplementedError
