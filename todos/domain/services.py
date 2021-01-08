from datetime import datetime

from todos.db.abstract_repository import AbstractRepository
from todos.domain.errors import TodoNotFoundError
from todos.domain.models import Todo


# TODO: Refactor to regular methods
class Service:
    def __init__(self, repository: AbstractRepository):
        self._repository = repository

    def complete(self, id: int) -> Todo:
        todo = self._repository.get(id)
        if not todo:
            raise TodoNotFoundError

        if todo.is_completed:
            return todo

        return self._repository.update(todo, completed_at=datetime.now())

    def incomplete(self, id: int) -> Todo:
        todo = self._repository.get(id)

        if not todo:
            raise TodoNotFoundError

        if not todo.is_completed:
            return todo

        return self._repository.update(todo, completed_at=None)
