from typing import Iterator

from dependency_injector import containers, providers
from sqlalchemy import Connection, Engine
from sqlalchemy.orm import sessionmaker

from app.modules.projects.application.archivization_service import ArchivizationService
from app.modules.projects.application.create_example_project import CreateExampleProject
from app.modules.projects.application.create_project import CreateProject
from app.modules.projects.application.tasks_service import TasksService
from app.modules.projects.application.update_project import UpdateProject
from app.modules.projects.infrastructure.adapters.unit_of_work import UnitOfWork
from app.modules.projects.infrastructure.queries.project_queries import FindProjectQuery, ListProjectsQuery
from app.modules.projects.infrastructure.queries.task_queries import FindTaskQuery, ListTasksQuery


def init_connection(engine: Engine) -> Iterator[Connection]:
    with engine.connect() as connection:
        yield connection


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            ".routes.project_tasks",
            ".routes.projects",
        ],
        auto_wire=False,
    )

    engine = providers.Dependency(instance_of=Engine)
    connection = providers.Resource(init_connection, engine=engine)
    session_factory = providers.Singleton(sessionmaker, bind=engine)

    uow = providers.Singleton(UnitOfWork, session_factory=session_factory)

    create_project = providers.Singleton(CreateProject, uow=uow)
    create_example_project = providers.Singleton(CreateExampleProject, uow=uow)
    update_project = providers.Singleton(UpdateProject, uow=uow)
    archivization_service = providers.Singleton(ArchivizationService, uow=uow)
    tasks_service = providers.Singleton(TasksService, uow=uow)

    list_projects_query = providers.Factory(ListProjectsQuery, connection=connection)
    find_project_query = providers.Factory(FindProjectQuery, connection=connection)

    list_tasks_query = providers.Factory(ListTasksQuery, connection=connection)
    find_task_query = providers.Factory(FindTaskQuery, connection=connection)
