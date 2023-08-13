from app.modules.projects.domain.task import Task, TaskNumber
from app.utc_datetime import utc_datetime


def test_task_is_completed_returns_false():
    task = Task(number=TaskNumber(1), name="Foo")
    assert not task.is_completed


def test_task_is_completed_returns_true():
    task = Task(number=TaskNumber(1), name="Foo")
    task.complete(now=utc_datetime(2020, 12, 31))

    assert task.is_completed


def test_complete_task_sets_completed_at():
    task = Task(number=TaskNumber(1), name="Foo")
    now = utc_datetime(2020, 12, 31)

    task.complete(now=now)

    assert task.completed_at is not None
    assert task.completed_at == now


def test_complete_task_does_nothing_when_task_is_already_completed():
    completed_at = utc_datetime(2020, 12, 31)
    task = Task(number=TaskNumber(1), name="Foo")
    task.complete(now=completed_at)

    task.complete(now=utc_datetime(2021, 1, 17))

    assert task.completed_at == completed_at


def test_incomplete_task_sets_completed_at():
    task = Task(number=TaskNumber(1), name="Foo")
    task.complete(now=utc_datetime(2020, 12, 31))

    task.incomplete()
    assert task.completed_at is None


def test_incomplete_task_does_nothing_when_task_is_already_completed():
    task = Task(number=TaskNumber(1), name="Foo")
    task.incomplete()
    assert task.completed_at is None
