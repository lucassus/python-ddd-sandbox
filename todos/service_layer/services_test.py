from datetime import date

from todos.factories import build_task
from todos.interfaces.fake_unit_of_work import FakeUnitOfWork
from todos.service_layer.services import complete_task, create_task, incomplete_task


def test_create_task():
    # Given
    fake_unit_of_work = FakeUnitOfWork([])

    task = create_task(
        "Testing...",
        uow=fake_unit_of_work,
    )

    assert task
    assert task.id == 1
    assert task.name == "Testing..."

    assert fake_unit_of_work.committed
    assert fake_unit_of_work.repository.get(1) == task


def test_complete():
    # Given
    task = build_task(id=1, name="Test task")
    fake_uow = FakeUnitOfWork([task])

    # When
    now = date(2021, 1, 8)
    completed_task = complete_task(
        task,
        uow=fake_uow,
        now=lambda: now,
    )

    # Then
    assert completed_task == task
    assert completed_task.completed_at is now
    assert fake_uow.committed


def test_incomplete():
    # Given
    task = build_task(id=1, name="Test task", completed_at=date(2021, 1, 5))
    fake_uow = FakeUnitOfWork([task])

    # When
    completed_task = incomplete_task(task, uow=fake_uow)

    # Then
    assert completed_task == task
    assert completed_task.completed_at is None
    assert fake_uow.committed
