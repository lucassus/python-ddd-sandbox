from dataclasses import dataclass, field
from datetime import date
from typing import NewType, Optional

from app.command.projects.entities import ensure
from app.command.projects.entities.errors import TaskNotFoundError
from app.command.projects.entities.task import Task, TaskNumber
from app.shared_kernel.aggregate_root import AggregateRoot
from app.shared_kernel.user_id import UserID

ProjectID = NewType("ProjectID", int)


@dataclass
class Project(AggregateRoot):
    id: ProjectID = field(init=False)
    user_id: UserID = field(init=False)

    name: str
    maximum_number_of_incomplete_tasks: Optional[int] = None

    last_task_number: TaskNumber = field(init=False, default_factory=lambda: TaskNumber(0))
    tasks: list[Task] = field(default_factory=list)
    archived_at: None | date = field(init=False, default=None)

    @property
    def archived(self) -> bool:
        return self.archived_at is not None

    def add_task(self, *, name: str, completed_at: Optional[date] = None) -> Task:
        ensure.project_has_allowed_number_of_incomplete_tasks(self)

        task = Task(name=name, completed_at=completed_at)
        self.last_task_number = TaskNumber(self.last_task_number + 1)
        task.number = self.last_task_number

        self.tasks.append(task)

        return task

    def complete_task(self, number: TaskNumber, now: date) -> Task:
        task = self._get_task(number)
        task.complete(now)

        return task

    def incomplete_task(self, number: TaskNumber) -> Task:
        task = self._get_task(number)
        task.incomplete()

        ensure.project_has_allowed_number_of_incomplete_tasks(self)

        return task

    def _get_task(self, number: TaskNumber) -> Task:
        for task in self.tasks:
            if task.number == number:
                return task

        raise TaskNotFoundError(number)

    def complete_all_tasks(self, now: date):
        for task in self.tasks:
            task.complete(now)

    @property
    def incomplete_tasks_count(self) -> int:
        return len([task for task in self.tasks if not task.is_completed])

    def archive(self, now) -> None:
        ensure.can_archive(self)
        self.archived_at = now

    def unarchive(self) -> None:
        self.archived_at = None
