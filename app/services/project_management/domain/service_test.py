from datetime import date

import pytest

from app.services.project_management.domain.service import Service
from app.services.project_management.test_utils.factories import (
    build_project,
    build_task,
)
from app.services.project_management.test_utils.fake_unit_of_work import FakeUnitOfWork


@pytest.fixture
def project():
    project = build_project(id=1)
    project.tasks = [build_task(id=2)]

    return project


@pytest.fixture
def fake_uow(project):
    return FakeUnitOfWork([project])


@pytest.fixture
def service(fake_uow):
    return Service(uow=fake_uow)


def test_create_task(service, project, fake_uow):
    service.create_task(project_id=project.id, name="Testing...")

    assert project.tasks[-1].name == "Testing..."
    assert fake_uow.committed


def test_complete_task(service, project, fake_uow):
    task = project.tasks[-1]
    now = date(2021, 1, 8)
    service.complete_task(project_id=project.id, id=task.id, now=now)

    assert task.completed_at is now
    assert fake_uow.committed


def test_incomplete_task(service, project, fake_uow):
    task = project.tasks[-1]
    service.incomplete_task(project_id=project.id, id=task.id)

    assert task.completed_at is None
    assert fake_uow.committed
