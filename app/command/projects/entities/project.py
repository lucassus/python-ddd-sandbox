from dataclasses import dataclass, field
from datetime import datetime
from typing import NewType, Optional

from app.command.projects.entities import ensure
from app.command.projects.entities.errors import TaskNotFoundError
from app.command.projects.entities.task import Task, TaskNumber
from app.command.shared_kernel.aggregate_root import AggregateRoot
from app.command.shared_kernel.user_id import UserID

ProjectID = NewType("ProjectID", int)


@dataclass(kw_only=False)
class Project(AggregateRoot):
    id: ProjectID = field(init=False)
    user_id: UserID

    name: str
    maximum_number_of_incomplete_tasks: Optional[int] = None

    last_task_number: TaskNumber = TaskNumber(0)
    tasks: list[Task] = field(default_factory=list)
    archived_at: None | datetime = None
    deleted_at: None | datetime = None

    @property
    def archived(self) -> bool:
        return self.archived_at is not None

    def add_task(self, *, name: str) -> Task:
        ensure.project_has_allowed_number_of_incomplete_tasks(self)

        task = Task(name=name)
        self.last_task_number = TaskNumber(self.last_task_number + 1)
        task.number = self.last_task_number

        self.tasks.append(task)

        return task

    def complete_task(self, number: TaskNumber, now: datetime) -> Task:
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

    def complete_all_tasks(self, now: datetime):
        for task in self.tasks:
            task.complete(now)

    @property
    def incomplete_tasks_count(self) -> int:
        return len([task for task in self.tasks if not task.is_completed])

    def archive(self, now: datetime) -> None:
        ensure.all_project_tasks_are_completed(self)
        self.archived_at = now

    def unarchive(self) -> None:
        self.archived_at = None

    def delete(self, now: datetime) -> None:
        ensure.project_is_archived(self)
        self.deleted_at = now
