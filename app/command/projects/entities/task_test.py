from datetime import date

from app.command.projects.entities.task import Task


def test_task_is_completed_returns_false():
    task = Task(name="Foo", completed_at=None)
    assert not task.is_completed


def test_task_is_completed_returns_true():
    task = Task(name="Foo", completed_at=date(2020, 12, 31))
    assert task.is_completed


def test_complete_task_sets_completed_at():
    task = Task(name="Foo")
    now = date(2020, 12, 31)

    task.complete(now=now)

    assert task.completed_at is not None
    assert task.completed_at == now


def test_complete_task_does_nothing_when_task_is_already_completed():
    completed_at = date(2020, 12, 31)
    task = Task(name="Foo", completed_at=completed_at)

    task.complete(now=date(2021, 1, 17))

    assert task.completed_at == completed_at


def test_incomplete_task_sets_completed_at():
    task = Task(name="Foo", completed_at=date(2020, 12, 31))
    task.incomplete()
    assert task.completed_at is None


def test_incomplete_task_does_nothing_when_task_is_already_completed():
    task = Task(name="Foo", completed_at=None)
    task.incomplete()
    assert task.completed_at is None
