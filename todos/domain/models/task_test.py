from datetime import date

from todos.domain.models.task import Task, complete_todos


def test_todo_is_completed_returns_false():
    todo = Task(name="Foo", completed_at=None)
    assert not todo.is_completed


def test_todo_is_completed_returns_true():
    todo = Task(name="Foo", completed_at=date(2020, 12, 31))
    assert todo.is_completed


def test_complete_todo_sets_completed_at():
    todo = Task(name="Foo")
    now = date(2020, 12, 31)

    todo.complete(now=lambda: now)

    assert todo.completed_at is not None
    assert todo.completed_at == now


def test_complete_todo_does_nothing_when_todo_is_already_completed():
    completed_at = date(2020, 12, 31)
    todo = Task(name="Foo", completed_at=completed_at)

    todo.complete()

    assert todo.completed_at == completed_at


def test_incomplete_todo_sets_completed_at():
    todo = Task(name="Foo", completed_at=date(2020, 12, 31))
    todo.incomplete()
    assert todo.completed_at is None


def test_incomplete_todo_does_nothing_when_todo_is_already_completed():
    todo = Task(name="Foo", completed_at=None)
    todo.incomplete()
    assert todo.completed_at is None


def test_complete_todos():
    todos = [
        Task(name="Foo", completed_at=None),
        Task(name="Foo", completed_at=date(2020, 12, 31)),
        Task(name="Foo", completed_at=None),
    ]

    complete_todos(todos, now=lambda: date(2021, 1, 12))

    for todo in todos:
        assert todo.is_completed
