import abc
from typing import Any


class ValueObject(abc.ABC):
    @abc.abstractmethod
    def __eq__(self, other: Any) -> bool: ...
