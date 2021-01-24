from datetime import date

from todos.services.project_management.domain.service import Service
from todos.services.project_management.test_utils.factories import (
    build_project,
    build_task,
)
from todos.services.project_management.test_utils.fake_unit_of_work import (
    FakeUnitOfWork,
)

project = build_project(id=1)
task = build_task(id=2)
project.tasks = [task]
fake_uow = FakeUnitOfWork([project])
service = Service(uow=fake_uow)


def test_create_task():
    service.create_task(project_id=project.id, name="Testing...")

    assert project.tasks[-1].name == "Testing..."
    assert fake_uow.committed


def test_complete_task():
    now = date(2021, 1, 8)
    service.complete_task(project_id=project.id, id=task.id, now=now)

    assert task.completed_at is now
    assert fake_uow.committed


def test_incomplete_task():
    service.incomplete_task(project_id=project.id, id=task.id)

    assert task.completed_at is None
    assert fake_uow.committed
