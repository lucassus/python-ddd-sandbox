from dataclasses import dataclass, field
from typing import List

from todos.domain.models.task import Task


@dataclass
class Project:
    id: int = field(init=False)

    name: str
    tasks: List[Task] = field(default_factory=list)

    # TODO: Can have max 3 incomplete tasks per project
    # TODO: Throw domain exception
    def add_task(self, *, name):
        task = Task(name=name)
        self.tasks.append(task)

        return task
