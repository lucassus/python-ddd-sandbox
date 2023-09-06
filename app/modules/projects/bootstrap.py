from fastapi import FastAPI
from sqlalchemy.orm import registry

from app import engine
from app.modules.projects.application.commands.archive_project import ArchiveProject, ArchiveProjectHandler
from app.modules.projects.application.commands.complete_task import CompleteTask, CompleteTaskHandler
from app.modules.projects.application.commands.create_example_project import (
    CreateExampleProject,
    CreateExampleProjectHandler,
)
from app.modules.projects.application.commands.create_project import CreateProject, CreateProjectHandler
from app.modules.projects.application.commands.create_task import CreateTask, CreateTaskHandler
from app.modules.projects.application.commands.delete_project import DeleteProject, DeleteProjectHandler
from app.modules.projects.application.commands.incomplete_task import IncompleteTask, IncompleteTaskHandler
from app.modules.projects.application.commands.unarchive_project import UnarchiveProject, UnarchiveProjectHandler
from app.modules.projects.application.commands.update_project import UpdateProject, UpdateProjectHandler
from app.modules.projects.entrypoints import routes
from app.modules.projects.entrypoints.containers import Container
from app.modules.projects.infrastructure.mappers import start_mappers
from app.modules.shared_kernel.message_bus import MessageBus


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
