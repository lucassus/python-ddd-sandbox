import typer

from app.infrastructure.db import AppSession, engine
from app.infrastructure.message_bus import Event, MessageBus
from app.infrastructure.tables import create_tables, drop_tables
from app.modules import mapper_registry
from app.modules.accounts.application.commands import RegisterUser, RegisterUserHandler
from app.modules.accounts.domain.password import Password
from app.modules.accounts.infrastructure.adapters.password_hasher import PasswordHasher
from app.modules.accounts.infrastructure.adapters.unit_of_work import UnitOfWork as AccountsUnitOfWork
from app.modules.accounts.infrastructure.mappers import start_mappers as start_account_mappers
from app.modules.projects.application.commands import (
    ArchiveProject,
    ArchiveProjectHandler,
    CompleteTask,
    CompleteTaskHandler,
    CreateExampleProject,
    CreateExampleProjectHandler,
    CreateProject,
    CreateProjectHandler,
    CreateTask,
    CreateTaskHandler,
    DeleteProject,
    DeleteProjectHandler,
)
from app.modules.projects.domain.project import ProjectName
from app.modules.projects.infrastructure.adapters.unit_of_work import UnitOfWork as ProjectsUnitOfWork
from app.modules.projects.infrastructure.mappers import start_mappers as start_project_mappers
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.utc_datetime import utc_now


def _session_factory():
    return AppSession(bind=engine)


class NoopMessageBus(MessageBus):
    # TODO: This is confusing, refactor this
    def dispatch(self, event: Event) -> None:
        pass


bus = NoopMessageBus()

# TODO: Re-use register logic from accounts module
accounts_uow = AccountsUnitOfWork(session_factory=_session_factory, bus=bus)
bus.register(RegisterUser, RegisterUserHandler(uow=accounts_uow, password_hasher=PasswordHasher()))

# TODO: Re-use register logic from projects module
projects_uow = ProjectsUnitOfWork(session_factory=_session_factory, bus=bus)
bus.register(CreateProject, CreateProjectHandler(uow=projects_uow, bus=bus))
bus.register(CreateExampleProject, CreateExampleProjectHandler(uow=projects_uow))
bus.register(CreateTask, CreateTaskHandler(uow=projects_uow))
bus.register(CompleteTask, CompleteTaskHandler(uow=projects_uow))
bus.register(ArchiveProject, ArchiveProjectHandler(uow=projects_uow))
bus.register(DeleteProject, DeleteProjectHandler(uow=projects_uow))


def main(rebuild_db: bool = True):
    if rebuild_db:
        drop_tables(engine)
        create_tables(engine)

    start_account_mappers(mapper_registry)
    start_project_mappers(mapper_registry)

    user_id = bus.execute(RegisterUser(EmailAddress("test@email.com"), Password("password")))
    bus.execute(CreateExampleProject(user_id))

    project_id = bus.execute(CreateProject(user_id, ProjectName("Software Engineering")))

    task_number = bus.execute(CreateTask(project_id, name="Learn Python"))
    bus.execute(CompleteTask(project_id, task_number, now=utc_now()))

    bus.execute(CreateTask(project_id, name="Learn Domain Driven Design"))
    bus.execute(CreateTask(project_id, name="Do the shopping"))
    bus.execute(CreateTask(project_id, name="Clean the house"))

    project_id = bus.execute(CreateProject(user_id, ProjectName("Clean the house")))
    bus.execute(ArchiveProject(project_id, now=utc_now()))
    bus.execute(DeleteProject(project_id, now=utc_now()))

    typer.echo("\nSeeding completed 🚀")


if __name__ == "__main__":
    typer.run(main)
