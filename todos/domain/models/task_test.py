from datetime import date

from todos.domain.models import Task, complete_tasks


def test_task_is_completed_returns_false():
    task = Task(name="Foo", completed_at=None)
    assert not task.is_completed


def test_task_is_completed_returns_true():
    task = Task(name="Foo", completed_at=date(2020, 12, 31))
    assert task.is_completed


def test_complete_task_sets_completed_at():
    task = Task(name="Foo")
    now = date(2020, 12, 31)

    task.complete(now=lambda: now)

    assert task.completed_at is not None
    assert task.completed_at == now


def test_complete_task_does_nothing_when_task_is_already_completed():
    completed_at = date(2020, 12, 31)
    task = Task(name="Foo", completed_at=completed_at)

    task.complete()

    assert task.completed_at == completed_at


def test_incomplete_task_sets_completed_at():
    task = Task(name="Foo", completed_at=date(2020, 12, 31))
    task.incomplete()
    assert task.completed_at is None


def test_incomplete_task_does_nothing_when_task_is_already_completed():
    task = Task(name="Foo", completed_at=None)
    task.incomplete()
    assert task.completed_at is None


def test_complete_tasks():
    tasks = [
        Task(name="Foo", completed_at=None),
        Task(name="Foo", completed_at=date(2020, 12, 31)),
        Task(name="Foo", completed_at=None),
    ]

    complete_tasks(tasks, now=lambda: date(2021, 1, 12))

    for task in tasks:
        assert task.is_completed
