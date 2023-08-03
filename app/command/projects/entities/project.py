from datetime import datetime
from typing import NewType

from app.command.projects.entities import ensure
from app.command.projects.entities.errors import TaskNotFoundError
from app.command.projects.entities.task import Task, TaskNumber
from app.command.shared_kernel.aggregate_root import AggregateRoot
from app.command.shared_kernel.user_id import UserID

ProjectID = NewType("ProjectID", int)


# TODO: Write ADR for removing dataclasses
class Project(AggregateRoot):
    _id: ProjectID
    _user_id: UserID

    _name: str
    _maximum_number_of_incomplete_tasks: None | int

    _last_task_number: TaskNumber
    _tasks: list[Task]  # TODO: Figure out how to map it to Dict[TaskNumber, Task]

    _archived_at: None | datetime
    _deleted_at: None | datetime

    def __init__(
        self,
        user_id: UserID,
        name: str,
        maximum_number_of_incomplete_tasks: None | int = None,
    ):
        self._user_id = user_id
        self._name = name
        self._maximum_number_of_incomplete_tasks = maximum_number_of_incomplete_tasks

        self._last_task_number = TaskNumber(0)
        self._tasks = []

        self._archived_at = None
        self._deleted_at = None

    @property
    def id(self) -> ProjectID:
        return self._id

    @property
    def user_id(self) -> UserID:
        return self._user_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def maximum_number_of_incomplete_tasks(self) -> None | int:
        return self._maximum_number_of_incomplete_tasks

    @property
    def tasks(self) -> tuple[Task, ...]:
        return tuple(self._tasks)

    @property
    def archived_at(self) -> None | datetime:
        return self._archived_at

    @property
    def archived(self) -> bool:
        return self._archived_at is not None

    @property
    def deleted_at(self) -> None | datetime:
        return self._deleted_at

    def add_task(self, *, name: str) -> Task:
        ensure.project_has_allowed_number_of_incomplete_tasks(self)

        self._last_task_number = TaskNumber(self._last_task_number + 1)
        task = Task(name=name, number=self._last_task_number)

        self._tasks.append(task)

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
        for task in self._tasks:
            if task.number == number:
                return task

        raise TaskNotFoundError(number)

    def complete_all_tasks(self, now: datetime):
        for task in self._tasks:
            task.complete(now)

    @property
    def incomplete_tasks_count(self) -> int:
        return len([task for task in self._tasks if not task.is_completed])

    def archive(self, now: datetime) -> None:
        ensure.all_project_tasks_are_completed(self)
        self._archived_at = now

    def unarchive(self) -> None:
        self._archived_at = None

    def delete(self, now: datetime) -> None:
        ensure.project_is_archived(self)
        self._deleted_at = now
