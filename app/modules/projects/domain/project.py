from dataclasses import dataclass
from datetime import datetime
from typing import NewType, Optional

from app.modules.projects.domain import ensure
from app.modules.projects.domain.errors import TaskNotFoundError
from app.modules.projects.domain.task import Task, TaskNumber
from app.modules.shared_kernel.entities.aggregate_root import AggregateRoot
from app.modules.shared_kernel.entities.user_id import UserID
from app.modules.shared_kernel.message_bus import Event

ProjectID = NewType("ProjectID", int)

ProjectName = NewType("ProjectName", str)

MaximumNumberOfIncompleteTasks = NewType("MaximumNumberOfIncompleteTasks", int)


class Project(AggregateRoot):
    @dataclass(frozen=True)
    class Created(Event):
        project_id: ProjectID

    _id: ProjectID
    _user_id: UserID

    _name: ProjectName
    _maximum_number_of_incomplete_tasks: None | MaximumNumberOfIncompleteTasks

    _last_task_number: TaskNumber
    _tasks_by_number: dict[TaskNumber, Task]

    _archived_at: None | datetime
    _deleted_at: None | datetime

    def __init__(
        self,
        user_id: UserID,
        name: ProjectName,
        maximum_number_of_incomplete_tasks: None | MaximumNumberOfIncompleteTasks = None,
    ):
        super().__init__()

        self._user_id = user_id
        self._name = name
        self._maximum_number_of_incomplete_tasks = maximum_number_of_incomplete_tasks

        self._last_task_number = TaskNumber(0)
        self._tasks_by_number = {}

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

    @name.setter
    def name(self, name: ProjectName):
        self._name = name

    @property
    def maximum_number_of_incomplete_tasks(self) -> None | int:
        return self._maximum_number_of_incomplete_tasks

    @property
    def tasks(self) -> tuple[Task, ...]:
        return tuple(self._tasks_by_number.values())

    @property
    def archived_at(self) -> None | datetime:
        return self._archived_at

    @property
    def archived(self) -> bool:
        return self._archived_at is not None

    @property
    def deleted_at(self) -> None | datetime:
        return self._deleted_at

    def add_task(self, *, name: str, created_by: Optional[UserID] = None) -> Task:
        ensure.project_has_allowed_number_of_incomplete_tasks(self)

        self._last_task_number = TaskNumber(self._last_task_number + 1)
        task = Task(name=name, number=self._last_task_number, created_by=created_by)

        self._tasks_by_number[task.number] = task

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
        try:
            return self._tasks_by_number[number]
        except KeyError as e:
            raise TaskNotFoundError(number) from e

    def complete_all_tasks(self, now: datetime):
        for task in self.tasks:
            task.complete(now)

    @property
    def incomplete_tasks_count(self) -> int:
        return len([task for task in self.tasks if not task.is_completed])

    def archive(self, now: datetime) -> None:
        ensure.all_project_tasks_are_completed(self)
        self._archived_at = now

    def unarchive(self) -> None:
        self._archived_at = None

    def delete(self, now: datetime) -> None:
        ensure.project_is_archived(self)
        self._deleted_at = now

    def __hash__(self):
        return hash(self._id)
