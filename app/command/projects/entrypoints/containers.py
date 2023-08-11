from dependency_injector import containers, providers

from app.command.projects.application.archivization_service import ArchivizationService
from app.command.projects.application.create_example_project import CreateExampleProject
from app.command.projects.application.create_project import CreateProject
from app.command.projects.application.tasks_service import TasksService
from app.command.projects.application.update_project import UpdateProject
from app.command.projects.infrastructure.adapters.unit_of_work import UnitOfWork
from app.infrastructure.db import AppSession


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            ".endpoints.project_tasks",
            ".endpoints.projects",
        ],
        auto_wire=False,
    )

    uow = providers.Singleton(UnitOfWork, session_factory=lambda: AppSession())

    create_project = providers.Singleton(CreateProject, uow=uow)
    create_example_project = providers.Singleton(CreateExampleProject, uow=uow)
    update_project = providers.Singleton(UpdateProject, uow=uow)
    archivization_service = providers.Singleton(ArchivizationService, uow=uow)
    tasks_service = providers.Singleton(TasksService, uow=uow)
