from dependency_injector import containers, providers
from sqlalchemy import Engine

from app.infrastructure.db import AppSession
from app.modules.authentication_contract import AuthenticationContract
from app.modules.projects.infrastructure.adapters.unit_of_work import UnitOfWork
from app.modules.projects.infrastructure.queries.project_query_handlers import (
    GetProjectQueryHandler,
    ListProjectsQueryHandler,
)
from app.modules.projects.infrastructure.queries.task_query_handlers import GetTaskQueryHandler, ListTasksQueryHandler
from app.shared.message_bus import MessageBus


class QueriesContainer(containers.DeclarativeContainer):
    engine = providers.Dependency(instance_of=Engine)

    list_projects_handler = providers.Singleton(ListProjectsQueryHandler, engine=engine)
    get_project_handler = providers.Singleton(GetProjectQueryHandler, engine=engine)
    list_tasks_handler = providers.Singleton(ListTasksQueryHandler, engine=engine)
    get_task_handler = providers.Singleton(GetTaskQueryHandler, engine=engine)


class Container(containers.DeclarativeContainer):
    engine = providers.Dependency(instance_of=Engine)
    bus = providers.Dependency(instance_of=MessageBus)

    authentication = providers.AbstractFactory(AuthenticationContract)

    session_factory = providers.Factory(AppSession, bind=engine)
    uow = providers.Singleton(
        UnitOfWork,
        bus,
        session_factory=session_factory.provider,
    )

    queries = providers.Container(QueriesContainer, engine=engine)
