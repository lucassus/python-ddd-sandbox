from datetime import date, datetime
from typing import Callable

from todos.db.abstract_repository import AbstractRepository
from todos.domain.models.todo import Todo
from todos.service_layer.errors import TodoNotFoundError


def complete_todo(
    id: int, repository: AbstractRepository, now: Callable[..., date] = datetime.utcnow
) -> Todo:
    todo = repository.get(id)

    if not todo:
        raise TodoNotFoundError

    todo.complete(now)

    return todo


def incomplete_todo(id: int, repository: AbstractRepository) -> Todo:
    todo = repository.get(id)

    if not todo:
        raise TodoNotFoundError

    todo.incomplete()

    return todo
