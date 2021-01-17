from datetime import date

from todos.service_layer.services import complete_task, create_task, incomplete_task
from todos.test_utils.factories import build_project
from todos.test_utils.fake_unit_of_work import FakeUnitOfWork


def test_create_task():
    # Given
    fake_unit_of_work = FakeUnitOfWork([])

    project = create_task(
        "Testing...",
        uow=fake_unit_of_work,
    )

    assert project
    assert project.id == 1
    assert project.name == "Testing..."

    assert fake_unit_of_work.committed
    assert fake_unit_of_work.repository.get(1) == project


def test_complete_task():
    # Given
    project = build_project(id=1, name="Test project")
    fake_uow = FakeUnitOfWork([project])

    # When
    now = date(2021, 1, 8)
    completed_project = complete_task(
        project,
        uow=fake_uow,
        now=lambda: now,
    )

    # Then
    assert completed_project == project
    assert completed_project.completed_at is now
    assert fake_uow.committed


def test_incomplete_task():
    # Given
    project = build_project(id=1, name="Test project")
    fake_uow = FakeUnitOfWork([project])

    # When
    completed_project = incomplete_task(project, uow=fake_uow)

    # Then
    assert completed_project == project
    assert completed_project.completed_at is None
    assert fake_uow.committed
