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


def register_module(
    app: FastAPI,
    mappers: registry,
    bus: MessageBus,
) -> Container:
    container = Container(engine=engine, bus=bus)
    container.wire()

    bus.register(
        CreateProject,
        CreateProjectHandler(
            uow=container.application.uow(),
            bus=bus,
        ),
    )
    bus.register(
        CreateExampleProject,
        CreateExampleProjectHandler(uow=container.application.uow()),
    )
    bus.register(
        UpdateProject,
        UpdateProjectHandler(uow=container.application.uow()),
    )
    bus.register(
        ArchiveProject,
        ArchiveProjectHandler(uow=container.application.uow()),
    )
    bus.register(
        UnarchiveProject,
        UnarchiveProjectHandler(uow=container.application.uow()),
    )
    bus.register(
        DeleteProject,
        DeleteProjectHandler(uow=container.application.uow()),
    )
    bus.register(
        CreateTask,
        CreateTaskHandler(uow=container.application.uow()),
    )
    bus.register(
        CompleteTask,
        CompleteTaskHandler(uow=container.application.uow()),
    )
    bus.register(
        IncompleteTask,
        IncompleteTaskHandler(uow=container.application.uow()),
    )

    start_mappers(mappers)
    app.include_router(routes.router)

    return container
