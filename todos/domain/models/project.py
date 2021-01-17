from dataclasses import dataclass, field
from datetime import date
from typing import List

from todos.domain.errors import TaskNotFoundError
from todos.domain.models.task import Task


@dataclass
class Project:
    id: int = field(init=False)

    name: str
    tasks: List[Task] = field(default_factory=list)

    # TODO: Can have max 3 incomplete tasks per project
    def add_task(self, *, name: str) -> Task:
        task = Task(name=name)
        self.tasks.append(task)

        return task

    def complete_task(
        self,
        id: int,
        now: date,
    ) -> Task:
        task = self.get_task(id)
        task.complete(now)

        return task

    def incomplete_task(self, id: int) -> Task:
        task = self.get_task(id)
        task.incomplete()

        return task

    def get_task(self, id: int) -> Task:
        try:
            # TODO: Add python cheat sheet with list, filters, maps etc
            return next(iter(filter(lambda t: t.id == id, self.tasks)))
        except StopIteration:
            raise TaskNotFoundError

    def complete_tasks(self, now: date):
        for task in self.tasks:
            task.complete(now)
