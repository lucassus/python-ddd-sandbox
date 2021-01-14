from dataclasses import dataclass, field
from typing import List

from todos.domain.models.task import Task


@dataclass
class Project:
    id: int = field(init=False)

    name: str
    tasks: List[Task] = field(default_factory=list)
