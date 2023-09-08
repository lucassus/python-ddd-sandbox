from sqlalchemy.orm import registry

from app.infrastructure.db import engine, AppSession
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
from app.modules.projects.infrastructure.adapters.unit_of_work import UnitOfWork
from app.modules.projects.infrastructure.mappers import start_mappers
from app.modules.shared_kernel.events import UserAccountCreated
from app.shared.message_bus import MessageBus


def _create_container():
    container = Container(engine=engine)
    container.wire(
        modules=[".application.event_handlers"],
        packages=[".entrypoints.routes"],
    )


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


def bootstrap_projects_module(mappers: registry, bus: MessageBus):
    start_mappers(mappers)

    _create_container()
    uow = UnitOfWork(bus, session_factory=lambda: AppSession(bind=engine))

    _register_commands(bus, uow)
    _register_event_handlers(bus, uow)
