from typing import List, Optional

from todos.domain.models.task import Task
from todos.interfaces.abstract_repository import AbstractRepository


class FakeRepository(AbstractRepository):
    def __init__(self, todos: List[Task]):
        self._todos = todos

    def get(self, id: int) -> Optional[Task]:
        try:
            return next(todo for todo in self._todos if todo.id == id)
        except StopIteration:
            return None

    def create(self, todo: Task) -> None:
        todo.id = self._get_next_id()
        self._todos.append(todo)

    def list(self) -> List[Task]:
        return self._todos

    def _get_next_id(self) -> int:
        return (
            max(todo.id for todo in self._todos if todo.id) + 1
            if len(self._todos) > 0
            else 1
        )
