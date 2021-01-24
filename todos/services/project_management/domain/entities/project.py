from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional

from todos.services.project_management.domain import ensure
from todos.services.project_management.domain.entities.task import Task
from todos.services.project_management.domain.errors import TaskNotFoundError


@dataclass
class Project:
    id: int = field(init=False)

    name: str
    max_incomplete_tasks_number: Optional[int] = None

    tasks: List[Task] = field(default_factory=list)

    def add_task(self, *, name: str) -> Task:
        ensure.project_has_allowed_number_of_incomplete_tasks(self)

        task = Task(name=name)
        self.tasks.append(task)

        return task

    def complete_task(self, id: int, now: date) -> Task:
        task = self.get_task(id)
        task.complete(now)

        return task

    def incomplete_task(self, id: int) -> Task:
        task = self.get_task(id)
        task.incomplete()

        ensure.project_has_allowed_number_of_incomplete_tasks(self)

        return task

    def get_task(self, id: int) -> Task:
        for task in self.tasks:
            if task.id == id:
                return task

        raise TaskNotFoundError

    def complete_tasks(self, now: date):
        for task in self.tasks:
            task.complete(now)
