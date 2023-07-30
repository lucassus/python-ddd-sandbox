from datetime import date

import pytest

from app.modules.projects.domain.factories import build_project
from app.modules.projects.domain.service import Service
from app.shared_kernel.user_id import UserID


@pytest.fixture
def service(fake_uow):
    return Service(uow=fake_uow)


def test_create_example_project(service: Service, fake_uow):
    project_id = service.create_example_project(user_id=UserID(1))

    assert fake_uow.committed

    project = fake_uow.project.get(project_id)
    assert project.name == "My first project"
    assert project.user_id == UserID(1)
    assert len(project.tasks) == 3
    assert project.tasks[0].name == "Sign up!"
    assert project.tasks[0].completed_at is not None
    assert project.tasks[1].name == "Watch the tutorial"
    assert project.tasks[2].name == "Start using our awesome app"


def test_create_task(service: Service, repository, fake_uow):
    project = repository.create(build_project(name="Test Project"))
    service.create_task(project_id=project.id, name="Testing...")

    assert project.tasks[-1].name == "Testing..."
    assert fake_uow.committed


def test_complete_task(service: Service, repository, fake_uow):
    project = repository.create(build_project(name="Test Project"))
    task = project.add_task(name="Testing...")

    now = date(2021, 1, 8)
    service.complete_task(task.number, project_id=project.id, now=now)

    assert task.completed_at is now
    assert fake_uow.committed


def test_incomplete_task(service: Service, repository, fake_uow):
    project = repository.create(build_project(name="Test Project"))
    task = project.add_task(name="Testing...", completed_at=date(2021, 1, 8))

    service.incomplete_task(task.number, project_id=project.id)

    assert task.completed_at is None
    assert fake_uow.committed
