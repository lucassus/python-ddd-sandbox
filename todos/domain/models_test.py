from datetime import date

from todos.domain.models import Todo


def test_todo_is_completed_returns_false():
    todo = Todo(name="Test 1", completed_at=None)
    assert not todo.is_completed


def test_todo_is_completed_returns_true():
    todo = Todo(name="Test 2", completed_at=date(2020, 12, 31))
    assert todo.is_completed
