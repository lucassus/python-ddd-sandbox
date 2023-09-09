from dependency_injector import containers, providers
from sqlalchemy import Engine

from app.infrastructure.db import AppSession
from app.modules.authentication_contract import AuthenticationContract
from app.modules.projects.infrastructure.adapters.unit_of_work import UnitOfWork
from app.modules.projects.queries.project_queries import GetProjectQuery, ListProjectsQuery
from app.modules.projects.queries.task_queries import GetTaskQuery, ListTasksQuery
from app.shared.message_bus import MessageBus


class QueriesContainer(containers.DeclarativeContainer):
    engine = providers.Dependency(instance_of=Engine)

    list_projects = providers.Singleton(ListProjectsQuery, engine=engine)
    get_project = providers.Singleton(GetProjectQuery, engine=engine)
    list_tasks = providers.Singleton(ListTasksQuery, engine=engine)
    get_task = providers.Singleton(GetTaskQuery, engine=engine)


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
