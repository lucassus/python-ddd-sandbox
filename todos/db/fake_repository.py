from typing import List, Optional

from todos.db.abstract_repository import AbstractRepository
from todos.domain.models.todo import Todo


class FakeRepository(AbstractRepository):
    def __init__(self, todos: List[Todo]):
        self._todos = todos

    def get(self, id: int) -> Optional[Todo]:
        try:
            return next(todo for todo in self._todos if todo.id == id)
        except StopIteration:
            return None

    def create(self, todo: Todo) -> None:
        todo.id = self._get_next_id()
        self._todos.append(todo)

    def list(self) -> List[Todo]:
        return self._todos

    def _get_next_id(self) -> int:
        return (
            max(todo.id for todo in self._todos if todo.id) + 1
            if len(self._todos) > 0
            else 1
        )
