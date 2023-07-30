from datetime import date

import pytest

from app.modules.projects.domain.factories import build_project
from app.modules.projects.domain.use_cases.tasks_service import TasksService


@pytest.fixture
def service(fake_uow):
    return TasksService(uow=fake_uow)


def test_create_task(service: TasksService, repository, fake_uow):
    project = repository.create(build_project(name="Test Project"))
    service.create_task(project_id=project.id, name="Testing...")

    assert project.tasks[-1].name == "Testing..."
    assert fake_uow.committed


def test_complete_task(service: TasksService, repository, fake_uow):
    project = repository.create(build_project(name="Test Project"))
    task = project.add_task(name="Testing...")

    now = date(2021, 1, 8)
    service.complete_task(task.number, project_id=project.id, now=now)

    assert task.completed_at is now
    assert fake_uow.committed


def test_incomplete_task(service: TasksService, repository, fake_uow):
    project = repository.create(build_project(name="Test Project"))
    task = project.add_task(name="Testing...", completed_at=date(2021, 1, 8))

    service.incomplete_task(task.number, project_id=project.id)

    assert task.completed_at is None
    assert fake_uow.committed
