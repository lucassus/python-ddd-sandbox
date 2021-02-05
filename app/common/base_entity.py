import abc
from dataclasses import dataclass, field


@dataclass
class BaseEntity(abc.ABC):
    id: int = field(init=False)
