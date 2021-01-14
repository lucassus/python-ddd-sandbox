from dataclasses import dataclass, field
from typing import List, Optional

from todos.domain.models.task import Task


@dataclass
class Project:
    id: int = field(init=False)

    name: str
    tasks: Optional[List[Task]] = field(default_factory=list)
