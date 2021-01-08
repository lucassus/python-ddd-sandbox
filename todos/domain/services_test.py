from datetime import date

from todos.db.fake_repository import FakeRepository
from todos.domain.models import Todo
from todos.domain.services import complete_todo, incomplete_todo


def test_complete():
    # Given
    todo = Todo(id=1, name="Test todo")
    repository = FakeRepository([todo])

    # When
    now = date(2021, 1, 8)
    completed_todo = complete_todo(todo.id, now=lambda: now, repository=repository)

    # Then
    assert completed_todo == todo
    assert completed_todo.completed_at is now


def test_incomplete():
    # Given
    todo = Todo(id=1, name="Test todo", completed_at=date(2021, 1, 5))
    repository = FakeRepository([todo])

    # When
    completed_todo = incomplete_todo(todo.id, repository=repository)

    # Then
    assert completed_todo == todo
    assert completed_todo.completed_at is None
