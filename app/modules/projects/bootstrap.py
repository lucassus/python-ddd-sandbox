from sqlalchemy.orm import registry

from app.infrastructure.db import async_engine, engine
from app.modules.projects.application.event_handlers import CreateUserExampleProjectHandler, SendProjectCreatedMessage
from app.modules.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.projects.domain.project import Project
from app.modules.projects.infrastructure.containers import Container
from app.modules.projects.infrastructure.mappers import start_mappers
from app.modules.shared_kernel.events import UserAccountCreated
from app.shared.message_bus import MessageBus


def _create_container(bus: MessageBus) -> Container:
    container = Container(
        engine=engine,
        async_engine=async_engine,
        bus=bus,
    )

    container.wire(
        modules=[
            ".application.event_handlers",
            ".entrypoints.dependencies",
        ],
        packages=[".entrypoints.routes"],
    )

    return container


def _register_event_handlers(bus: MessageBus, uow: AbstractUnitOfWork) -> None:
    bus.listen(UserAccountCreated, CreateUserExampleProjectHandler(bus))
    bus.listen(Project.Created, SendProjectCreatedMessage(uow))


def bootstrap_projects_module(mappers: registry, bus: MessageBus) -> Container:
    start_mappers(mappers)

    container = _create_container(bus)
    uow = container.uow()

    container.register_command_handlers()
    _register_event_handlers(bus, uow)

    return container
