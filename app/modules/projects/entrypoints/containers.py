from dependency_injector import containers, providers
from sqlalchemy import Engine

from app.modules.projects.queries.project_queries import GetProjectQuery, ListProjectsQuery
from app.modules.projects.queries.task_queries import GetTaskQuery, ListTasksQuery
from app.shared.message_bus import MessageBus


class QueriesContainer(containers.DeclarativeContainer):
    engine = providers.Dependency(instance_of=Engine)

    list_projects = providers.Singleton(ListProjectsQuery, engine)
    get_project = providers.Singleton(GetProjectQuery, engine)
    list_tasks = providers.Singleton(ListTasksQuery, engine)
    get_task = providers.Singleton(GetTaskQuery, engine)


class Container(containers.DeclarativeContainer):
    engine = providers.Dependency(instance_of=Engine)
    bus = providers.Dependency(instance_of=MessageBus)

    queries = providers.Container(QueriesContainer, engine=engine)
