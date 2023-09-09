from sqlalchemy.orm import registry

from app.infrastructure.db import engine
from app.modules.projects.application.commands import (
    ArchiveProject,
    ArchiveProjectHandler,
    CompleteTask,
    CompleteTaskHandler,
    CreateExampleProject,
    CreateExampleProjectHandler,
    CreateProject,
    CreateProjectHandler,
    CreateTask,
    CreateTaskHandler,
    DeleteProject,
    DeleteProjectHandler,
    IncompleteTask,
    IncompleteTaskHandler,
    UnarchiveProject,
    UnarchiveProjectHandler,
    UpdateProject,
    UpdateProjectHandler,
)
from app.modules.projects.application.event_handlers import CreateUserExampleProjectHandler, SendProjectCreatedMessage
from app.modules.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.projects.domain.project import Project
from app.modules.projects.entrypoints.containers import Container
from app.modules.projects.infrastructure.mappers import start_mappers
from app.modules.shared_kernel.events import UserAccountCreated
from app.shared.message_bus import MessageBus


def _create_container(bus: MessageBus) -> Container:
    container = Container(engine=engine, bus=bus)
    container.wire(
        modules=[
            ".application.event_handlers",
            ".entrypoints.dependencies",
        ],
        packages=[".entrypoints.routes"],
    )

    return container


def _register_commands(bus: MessageBus, uow: AbstractUnitOfWork) -> None:
    bus.register(CreateProject, CreateProjectHandler(uow, bus))
    bus.register(CreateExampleProject, CreateExampleProjectHandler(uow))
    bus.register(UpdateProject, UpdateProjectHandler(uow))
    bus.register(ArchiveProject, ArchiveProjectHandler(uow))
    bus.register(UnarchiveProject, UnarchiveProjectHandler(uow))
    bus.register(DeleteProject, DeleteProjectHandler(uow))
    bus.register(CreateTask, CreateTaskHandler(uow))
    bus.register(CompleteTask, CompleteTaskHandler(uow))
    bus.register(IncompleteTask, IncompleteTaskHandler(uow))


def _register_event_handlers(bus: MessageBus, uow: AbstractUnitOfWork) -> None:
    bus.listen(UserAccountCreated, CreateUserExampleProjectHandler(bus))
    bus.listen(Project.Created, SendProjectCreatedMessage(uow))


def bootstrap_projects_module(mappers: registry, bus: MessageBus) -> Container:
    start_mappers(mappers)

    container = _create_container(bus)
    uow = container.uow()

    _register_commands(bus, uow)
    _register_event_handlers(bus, uow)

    return container
