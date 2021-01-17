from datetime import date

from todos.service_layer.services import complete_task, create_task, incomplete_task
from todos.test_utils.factories import build_project, build_task
from todos.test_utils.fake_unit_of_work import FakeUnitOfWork


def test_create_task():
    # Given
    project = build_project()
    fake_unit_of_work = FakeUnitOfWork([project])

    task = create_task(
        "Testing...",
        project=project,
        uow=fake_unit_of_work,
    )

    assert task
    assert project.tasks == [task]

    assert fake_unit_of_work.committed


def test_complete_task():
    # Given
    project = build_project(id=1)
    task = build_task(id=1)
    project.tasks = [task]
    fake_uow = FakeUnitOfWork([project])

    # When
    now = date(2021, 1, 8)
    updated_task = complete_task(
        task.id,
        project=project,
        uow=fake_uow,
        now=lambda: now,
    )

    # Then
    assert updated_task == task
    assert updated_task.completed_at is now

    assert fake_uow.committed


def test_incomplete_task():
    # Given
    project = build_project(id=1)
    task = build_task(id=1)
    project.tasks = [task]
    fake_uow = FakeUnitOfWork([project])

    # When
    updated_task = incomplete_task(
        task.id,
        project=project,
        uow=fake_uow,
    )

    # Then
    assert updated_task == task
    assert updated_task.completed_at is None

    assert fake_uow.committed
