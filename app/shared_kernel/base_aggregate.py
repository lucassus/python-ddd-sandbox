from typing import TypeVar

from app.shared_kernel.base_entity import BaseEntity

_T_AGGREGATE_ID = TypeVar("_T_AGGREGATE_ID", bound=int)


class BaseAggregate(BaseEntity[_T_AGGREGATE_ID]):
    pass
