from fastapi import FastAPI
from sqlalchemy.orm import registry

from app.infrastructure.db import engine
from app.infrastructure.message_bus import MessageBus
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
from app.modules.projects.entrypoints import routes
from app.modules.projects.entrypoints.containers import Container
from app.modules.projects.infrastructure.mappers import start_mappers


def _create_container(bus: MessageBus) -> Container:
    container = Container(engine=engine, bus=bus)
    container.wire()

    return container


def _register_commands(bus: MessageBus, container: Container) -> None:
    uow = container.application.uow()

    bus.register(CreateProject, CreateProjectHandler(uow=uow, bus=bus))
    bus.register(CreateExampleProject, CreateExampleProjectHandler(uow=uow))
    bus.register(UpdateProject, UpdateProjectHandler(uow=uow))
    bus.register(ArchiveProject, ArchiveProjectHandler(uow=uow))
    bus.register(UnarchiveProject, UnarchiveProjectHandler(uow=uow))
    bus.register(DeleteProject, DeleteProjectHandler(uow=uow))
    bus.register(CreateTask, CreateTaskHandler(uow=uow))
    bus.register(CompleteTask, CompleteTaskHandler(uow=uow))
    bus.register(IncompleteTask, IncompleteTaskHandler(uow=uow))


def bootstrap_projects_module(
    app: FastAPI,
    mappers: registry,
    bus: MessageBus,
) -> Container:
    start_mappers(mappers)
    app.include_router(routes.router)

    container = _create_container(bus)
    _register_commands(bus, container)

    return container
