from typing import Iterator

from dependency_injector import containers, providers
from sqlalchemy import Connection, Engine
from sqlalchemy.orm import sessionmaker

from app.modules.authentication_contract import AuthenticationContract
from app.modules.projects.application.archivization_service import ArchivizationService
from app.modules.projects.application.create_example_project import CreateExampleProject
from app.modules.projects.application.create_project import CreateProject
from app.modules.projects.application.tasks_service import TasksService
from app.modules.projects.application.update_project import UpdateProject
from app.modules.projects.infrastructure.adapters.unit_of_work import UnitOfWork
from app.modules.projects.infrastructure.queries.project_queries import GetProjectSQLSQLQuery, ListProjectsSQLSQLQuery
from app.modules.projects.infrastructure.queries.task_queries import GetTaskSQLQuery, ListTasksSQLQuery


def init_connection(engine: Engine) -> Iterator[Connection]:
    with engine.connect() as connection:
        yield connection


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            ".dependencies",
            ".routes.project_tasks",
            ".routes.projects",
        ],
        auto_wire=False,
    )

    engine = providers.Dependency(instance_of=Engine)
    connection = providers.Resource(init_connection, engine=engine)
    session_factory = providers.Singleton(sessionmaker, bind=engine)

    uow = providers.Singleton(UnitOfWork, session_factory=session_factory)

    authentication = providers.Dependency(instance_of=AuthenticationContract)  # type: ignore[type-abstract]

    create_project = providers.Singleton(CreateProject, uow=uow)
    create_example_project = providers.Singleton(CreateExampleProject, uow=uow)
    update_project = providers.Singleton(UpdateProject, uow=uow)
    archivization_service = providers.Singleton(ArchivizationService, uow=uow)
    tasks_service = providers.Singleton(TasksService, uow=uow)

    list_projects_query = providers.Factory(ListProjectsSQLSQLQuery, connection=connection)
    get_project_query = providers.Factory(GetProjectSQLSQLQuery, connection=connection)
    list_tasks_query = providers.Factory(ListTasksSQLQuery, connection=connection)
    get_task_query = providers.Factory(GetTaskSQLQuery, connection=connection)
