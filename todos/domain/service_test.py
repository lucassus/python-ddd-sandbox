from datetime import date

from todos.domain.service import Service
from todos.test_utils.factories import build_project, build_task
from todos.test_utils.fake_unit_of_work import FakeUnitOfWork

project = build_project(id=1)
task = build_task(id=2)
project.tasks = [task]
fake_uow = FakeUnitOfWork([project])
service = Service(project_id=1, uow=fake_uow)


def test_create_task():
    new_task = service.create_task("Testing...")

    assert new_task
    assert new_task.name == "Testing..."
    assert project.tasks[-1] == new_task

    assert fake_uow.committed


def test_complete_task():
    # Given
    now = date(2021, 1, 8)

    # When
    updated_task = service.complete_task(task.id, now=now)

    # Then
    assert updated_task == task
    assert updated_task.completed_at is now

    assert fake_uow.committed


def test_incomplete_task():
    # When
    updated_task = service.incomplete_task(task.id)

    # Then
    assert updated_task == task
    assert updated_task.completed_at is None

    assert fake_uow.committed
