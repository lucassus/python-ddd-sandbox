import abc
from dataclasses import dataclass, field
from typing import Generic, TypeVar

_T_ID = TypeVar("_T_ID", bound=int)


@dataclass
class BaseEntity(Generic[_T_ID], metaclass=abc.ABCMeta):
    id: _T_ID = field(init=False)
