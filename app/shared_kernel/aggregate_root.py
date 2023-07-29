from typing import TypeVar

from app.shared_kernel.entity import Entity

_T_AGGREGATE_ID = TypeVar("_T_AGGREGATE_ID", bound=int)


class AggregateRoot(Entity[_T_AGGREGATE_ID]):
    pass
