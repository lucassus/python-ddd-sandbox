import pytest

from app.modules.projects.application.testing.fake_project_repository import FakeProjectRepository
from app.modules.projects.application.testing.fake_unit_of_work import FakeUnitOfWork
from app.shared.message_bus import MessageBus


@pytest.fixture
def repository():
    return FakeProjectRepository()


@pytest.fixture
def message_bus() -> MessageBus:
    return MessageBus()


@pytest.fixture
def fake_uow(repository, message_bus):
    return FakeUnitOfWork(repository, bus=message_bus)
