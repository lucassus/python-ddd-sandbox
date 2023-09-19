import typer

from app.infrastructure.db import engine
from app.infrastructure.tables import create_tables, drop_tables
from app.modules import bus, mapper_registry
from app.modules.accounts.application.commands import RegisterUser
from app.modules.accounts.bootstrap import bootstrap_accounts_module
from app.modules.accounts.domain.password import Password
from app.modules.projects.application.commands import (
    ArchiveProject,
    CompleteTask,
    CreateExampleProject,
    CreateProject,
    CreateTask,
    DeleteProject,
)
from app.modules.projects.bootstrap import bootstrap_projects_module
from app.modules.projects.domain.project import ProjectName
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.utc_datetime import utc_now

authentication = bootstrap_accounts_module(mapper_registry, bus)
bootstrap_projects_module(mapper_registry, bus, authentication)


def main(rebuild_db: bool = True):
    if rebuild_db:
        drop_tables(engine)
        create_tables(engine)

    user_id = bus.execute(RegisterUser(EmailAddress("test@email.com"), Password("password")))
    bus.execute(CreateExampleProject(user_id))

    project_id = bus.execute(CreateProject(user_id, ProjectName("Software Engineering")))
    task_number = bus.execute(CreateTask(project_id, name="Learn Python"))
    bus.execute(CompleteTask(project_id, task_number, now=utc_now()))

    project_id = bus.execute(CreateProject(user_id, ProjectName("Learn Domain Driven Design")))
    bus.execute(CreateTask(project_id, name="Learn Clean Architecture"))
    bus.execute(CreateTask(project_id, name="Learn Event Sourcing"))
    bus.execute(CreateTask(project_id, name="Learn CQRS"))
    bus.execute(CreateTask(project_id, name="Read Domain Driven Design book"))

    project_id = bus.execute(CreateProject(user_id, ProjectName("Household")))
    bus.execute(CreateTask(project_id, name="Do the shopping"))
    bus.execute(CreateTask(project_id, name="Clean the house"))

    project_id = bus.execute(CreateProject(user_id, ProjectName("Clean the house")))
    bus.execute(ArchiveProject(project_id, now=utc_now()))
    bus.execute(DeleteProject(project_id, now=utc_now()))

    typer.echo("\nSeeding completed 🚀")


if __name__ == "__main__":
    typer.run(main)
