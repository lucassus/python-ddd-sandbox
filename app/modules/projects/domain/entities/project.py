from dataclasses import dataclass, field
from datetime import date
from typing import NewType, Optional

from app.modules.projects.domain import ensure
from app.modules.projects.domain.entities.task import Task, TaskID
from app.modules.projects.domain.errors import TaskNotFoundError
from app.shared_kernel.aggregate_root import AggregateRoot
from app.shared_kernel.user_id import UserID

ProjectID = NewType("ProjectID", int)


@dataclass
class Project(AggregateRoot[ProjectID]):
    user_id: UserID = field(init=False)

    name: str
    maximum_number_of_incomplete_tasks: Optional[int] = None

    tasks: list[Task] = field(default_factory=list)

    def add_task(self, *, name: str) -> Task:
        ensure.project_has_allowed_number_of_incomplete_tasks(self)

        task = Task(name=name)
        self.tasks.append(task)

        return task

    def complete_task(self, id: TaskID, now: date) -> Task:
        task = self.get_task(id)
        task.complete(now)

        return task

    def incomplete_task(self, id: TaskID) -> Task:
        task = self.get_task(id)
        task.incomplete()

        ensure.project_has_allowed_number_of_incomplete_tasks(self)

        return task

    def get_task(self, id: TaskID) -> Task:
        for task in self.tasks:
            if task.id == id:
                return task

        raise TaskNotFoundError(id)

    def complete_tasks(self, now: date):
        for task in self.tasks:
            task.complete(now)
