from typing import List, Optional

from todos.domain.models import Task
from todos.interfaces.abstract_repository import AbstractRepository


class FakeRepository(AbstractRepository):
    def __init__(self, *, tasks: List[Task]):
        self._tasks = tasks

    def get(self, id: int) -> Optional[Task]:
        try:
            return next(task for task in self._tasks if task.id == id)
        except StopIteration:
            return None

    def create(self, task: Task) -> None:
        task.id = self._get_next_id()
        self._tasks.append(task)

    def list(self) -> List[Task]:
        return self._tasks

    def _get_next_id(self) -> int:
        ids = [task.id for task in self._tasks if task.id is not None]

        if len(ids) == 0:
            return 1

        return max(ids) + 1
