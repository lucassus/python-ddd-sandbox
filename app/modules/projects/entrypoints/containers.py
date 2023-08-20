from dependency_injector import containers, providers
from sqlalchemy import Engine

from app.infrastructure.db import AppSession
from app.modules.authentication_contract import AuthenticationContract
from app.modules.projects.application.archivization_service import ArchivizationService
from app.modules.projects.application.create_example_project import CreateExampleProject
from app.modules.projects.application.create_project import CreateProject
from app.modules.projects.application.tasks_service import TasksService
from app.modules.projects.application.update_project import UpdateProject
from app.modules.projects.infrastructure.adapters.unit_of_work import UnitOfWork
from app.modules.projects.infrastructure.queries.project_queries import GetProjectSQLSQLQuery, ListProjectsSQLSQLQuery
from app.modules.projects.infrastructure.queries.task_queries import GetTaskSQLQuery, ListTasksSQLQuery


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
    session_factory = providers.Factory(AppSession, bind=engine)
    uow = providers.Singleton(UnitOfWork, session_factory=session_factory.provider)

    authentication = providers.AbstractFactory(AuthenticationContract)

    create_project = providers.Singleton(CreateProject, uow=uow)
    create_example_project = providers.Singleton(CreateExampleProject, uow=uow)
    update_project = providers.Singleton(UpdateProject, uow=uow)
    archivization_service = providers.Singleton(ArchivizationService, uow=uow)
    tasks_service = providers.Singleton(TasksService, uow=uow)

    list_projects_query = providers.Singleton(ListProjectsSQLSQLQuery, engine=engine)
    get_project_query = providers.Singleton(GetProjectSQLSQLQuery, engine=engine)
    list_tasks_query = providers.Singleton(ListTasksSQLQuery, engine=engine)
    get_task_query = providers.Singleton(GetTaskSQLQuery, engine=engine)
