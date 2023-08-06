import typer

from app.command import mapper_registry
from app.command.accounts.application.register_user import RegisterUser
from app.command.accounts.entities.email_address import EmailAddress
from app.command.accounts.entities.password import Password
from app.command.accounts.infrastructure.adapters.unit_of_work import UnitOfWork as AccountsUnitOfWork
from app.command.accounts.infrastructure.mappers import start_mappers as start_account_mappers
from app.command.projects.application.archivization_service import ArchivizationService
from app.command.projects.application.create_example_project import CreateExampleProject
from app.command.projects.application.create_project import CreateProject
from app.command.projects.application.tasks_service import TasksService
from app.command.projects.entities.project import ProjectName
from app.command.projects.infrastructure.adapters.unit_of_work import UnitOfWork as ProjectsUnitOfWork
from app.command.projects.infrastructure.mappers import start_mappers as start_project_mappers
from app.command.shared_kernel.message_bus import BaseEvent, MessageBus
from app.infrastructure.db import AppSession, engine
from app.infrastructure.tables import create_tables, drop_tables


class NoopMessageBus(MessageBus):
    def dispatch(self, event: BaseEvent) -> None:
        pass


def main(rebuild_db: bool = True):
    if rebuild_db:
        drop_tables(engine)
        create_tables(engine)

    start_account_mappers(mapper_registry)
    start_project_mappers(mapper_registry)

    register_user = RegisterUser(
        uow=AccountsUnitOfWork(session_factory=AppSession),
        bus=NoopMessageBus(),
    )
    user_id = register_user(
        email=EmailAddress("test@email.com"),
        password=Password("password"),
    )

    projects_uow = ProjectsUnitOfWork(session_factory=AppSession)
    create_example_project = CreateExampleProject(uow=projects_uow)
    create_example_project(user_id)

    create_project = CreateProject(uow=projects_uow)
    project_id = create_project(user_id, ProjectName("Software Engineering"))

    tasks_service = TasksService(uow=projects_uow)
    task_number = tasks_service.create_task(project_id, name="Learn Python")
    tasks_service.complete_task(project_id, task_number)
    tasks_service.create_task(project_id, name="Learn Domain Driven Design")
    tasks_service.create_task(project_id, name="Do the shopping")
    tasks_service.create_task(project_id, name="Clean the house")

    project_id = create_project(user_id, ProjectName("Clean the house"))
    archivization = ArchivizationService(uow=projects_uow)
    archivization.archive(project_id)
    archivization.delete(project_id)

    typer.echo("\nSeeding completed 🚀")


if __name__ == "__main__":
    typer.run(main)
