import pytest

from app.modules.projects.application.tasks_service import TasksService
from app.modules.projects.domain.project_builder import ProjectBuilder
from app.utc_datetime import utc_datetime


@pytest.fixture()
def service(fake_uow):
    return TasksService(uow=fake_uow)


def test_create_task(service: TasksService, repository, fake_uow):
    project = repository.create(ProjectBuilder().build())
    service.create_task(project_id=project.id, name="Testing...")

    assert project.tasks[-1].name == "Testing..."
    assert fake_uow.committed


def test_complete_task(service: TasksService, repository, fake_uow):
    project = repository.create(ProjectBuilder().build())
    task = project.add_task(name="Testing...")

    now = utc_datetime(2021, 1, 8)
    service.complete_task(project.id, task.number, now=now)

    assert task.completed_at is now
    assert fake_uow.committed


def test_incomplete_task(service: TasksService, repository, fake_uow):
    project = repository.create(ProjectBuilder().build())
    task = project.add_task(name="Testing...")
    project.complete_task(task.number, now=utc_datetime(2021, 1, 8))

    service.incomplete_task(project.id, task.number)

    assert task.completed_at is None
    assert fake_uow.committed