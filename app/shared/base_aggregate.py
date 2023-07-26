from typing import TypeVar

from app.shared.base_entity import BaseEntity

_T_ID = TypeVar("_T_ID", bound=int)


class BaseAggregate(BaseEntity[_T_ID]):
    pass
