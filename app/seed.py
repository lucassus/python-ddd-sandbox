import typer

from app.infrastructure.db import AppSession, engine
from app.infrastructure.tables import create_tables, drop_tables
from app.modules import mapper_registry
from app.modules.accounts.application.commands.register_user import RegisterUser, RegisterUserHandler
from app.modules.accounts.domain.password import Password
from app.modules.accounts.infrastructure.adapters.password_hasher import PasswordHasher
from app.modules.accounts.infrastructure.adapters.unit_of_work import UnitOfWork as AccountsUnitOfWork
from app.modules.accounts.infrastructure.mappers import start_mappers as start_account_mappers
from app.modules.projects.application.archivization_service import ArchivizationService
from app.modules.projects.application.create_example_project import CreateExampleProject
from app.modules.projects.application.create_project import CreateProject
from app.modules.projects.application.tasks_service import TasksService
from app.modules.projects.domain.project import ProjectName
from app.modules.projects.infrastructure.adapters.unit_of_work import UnitOfWork as ProjectsUnitOfWork
from app.modules.projects.infrastructure.mappers import start_mappers as start_project_mappers
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID
from app.modules.shared_kernel.message_bus import Event, MessageBus


def _session_factory():
    return AppSession(bind=engine)


class NoopMessageBus(MessageBus):
    def dispatch(self, event: Event) -> None:
        pass


bus = NoopMessageBus()

accounts_uow = AccountsUnitOfWork(session_factory=_session_factory, bus=bus)
register_user = RegisterUserHandler(uow=accounts_uow, password_hasher=PasswordHasher())

projects_uow = ProjectsUnitOfWork(session_factory=_session_factory, bus=bus)
create_example_project = CreateExampleProject(uow=projects_uow)
create_project = CreateProject(uow=projects_uow, bus=bus)
archivization = ArchivizationService(uow=projects_uow)
tasks_service = TasksService(uow=projects_uow)


def main(rebuild_db: bool = True):
    if rebuild_db:
        drop_tables(engine)
        create_tables(engine)

    start_account_mappers(mapper_registry)
    start_project_mappers(mapper_registry)

    user_id = UserID.generate()
    register_user(
        RegisterUser(
            user_id=user_id,
            email=EmailAddress("test@email.com"),
            password=Password("password"),
        )
    )

    create_example_project(user_id)

    project_id = create_project(user_id, ProjectName("Software Engineering"))
    task_number = tasks_service.create_task(project_id, name="Learn Python")
    tasks_service.complete_task(project_id, task_number)
    tasks_service.create_task(project_id, name="Learn Domain Driven Design")
    tasks_service.create_task(project_id, name="Do the shopping")
    tasks_service.create_task(project_id, name="Clean the house")

    project_id = create_project(user_id, ProjectName("Clean the house"))
    archivization.archive(project_id)
    archivization.delete(project_id)

    typer.echo("\nSeeding completed 🚀")


if __name__ == "__main__":
    typer.run(main)
