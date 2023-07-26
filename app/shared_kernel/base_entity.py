import abc
from dataclasses import dataclass, field
from typing import Generic, TypeVar

_T_ENTITY_ID = TypeVar("_T_ENTITY_ID", bound=int)


@dataclass
class BaseEntity(Generic[_T_ENTITY_ID], metaclass=abc.ABCMeta):
    id: _T_ENTITY_ID = field(init=False)
