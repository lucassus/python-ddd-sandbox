import pytest

from app.infrastructure.message_bus import MessageBus
from app.modules.projects.application.testing.fake_project_repository import FakeProjectRepository
from app.modules.projects.application.testing.fake_unit_of_work import FakeUnitOfWork


@pytest.fixture()
def repository():
    return FakeProjectRepository()


@pytest.fixture()
def message_bus() -> MessageBus:
    return MessageBus()


@pytest.fixture()
def fake_uow(repository, message_bus):
    return FakeUnitOfWork(repository, bus=message_bus)
