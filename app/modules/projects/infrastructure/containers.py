from dependency_injector import containers, providers
from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncEngine

from app.infrastructure.db import AppSession
from app.modules.authentication_contract import AuthenticationContract
from app.modules.projects.application.commands import (
    CreateProject,
    CreateExampleProject,
    UpdateProject,
    ArchiveProject,
    UnarchiveProject,
    DeleteProject,
    CreateTask,
    CompleteTask,
    IncompleteTask,
    CreateProjectHandler,
    CreateExampleProjectHandler,
    UpdateProjectHandler,
    ArchiveProjectHandler,
    UnarchiveProjectHandler,
    DeleteProjectHandler,
    CreateTaskHandler,
    CompleteTaskHandler,
    IncompleteTaskHandler,
)
from app.modules.projects.infrastructure.adapters.unit_of_work import UnitOfWork
from app.modules.projects.infrastructure.queries.project_query_handlers import (
    GetProjectQueryHandler,
    ListProjectsQueryHandler,
)
from app.modules.projects.infrastructure.queries.task_query_handlers import GetTaskQueryHandler, ListTasksQueryHandler
from app.shared.message_bus import MessageBus


class QueriesContainer(containers.DeclarativeContainer):
    engine = providers.Dependency(instance_of=AsyncEngine)

    list_projects_handler = providers.Singleton(ListProjectsQueryHandler, engine)
    get_project_handler = providers.Singleton(GetProjectQueryHandler, engine)
    list_tasks_handler = providers.Singleton(ListTasksQueryHandler, engine)
    get_task_handler = providers.Singleton(GetTaskQueryHandler, engine)


class Container(containers.DeclarativeContainer):
    engine = providers.Dependency(instance_of=Engine)
    async_engine = providers.Dependency(instance_of=AsyncEngine)
    bus = providers.Dependency(instance_of=MessageBus)

    authentication = providers.AbstractFactory(AuthenticationContract)

    session_factory = providers.Factory(AppSession, bind=engine)
    uow = providers.Singleton(
        UnitOfWork,
        bus,
        session_factory=session_factory.provider,
    )

    register_command_handlers = providers.Callable(
        lambda bus, command_handlers: bus.register_all(command_handlers),
        bus=bus,
        command_handlers=providers.Dict(
            {
                CreateProject: providers.Factory(CreateProjectHandler, uow, bus),
                CreateExampleProject: providers.Factory(CreateExampleProjectHandler, uow),
                UpdateProject: providers.Factory(UpdateProjectHandler, uow),
                ArchiveProject: providers.Factory(ArchiveProjectHandler, uow),
                UnarchiveProject: providers.Factory(UnarchiveProjectHandler, uow),
                DeleteProject: providers.Factory(DeleteProjectHandler, uow),
                CreateTask: providers.Factory(CreateTaskHandler, uow),
                CompleteTask: providers.Factory(CompleteTaskHandler, uow),
                IncompleteTask: providers.Factory(IncompleteTaskHandler, uow),
            }
        ),
    )

    queries = providers.Container(QueriesContainer, engine=async_engine)
