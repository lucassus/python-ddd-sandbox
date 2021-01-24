from datetime import datetime

import typer
from tabulate import tabulate

from todos.commands.adapters.mappers import start_mappers
from todos.commands.domain.entities import Project
from todos.infrastructure.session import engine, get_session
from todos.infrastructure.tables import create_tables, drop_tables

start_mappers()
session = get_session()


# TODO: Think again about seen and bounded contexts
# TODO: Should I use raw sqls without entities?
def main(rebuild_db: bool = True):
    if rebuild_db:
        drop_tables(engine)
        create_tables(engine)

    project = Project(name="Work", max_incomplete_tasks_number=4)

    task = project.add_task(name="Learn Python")
    project.add_task(name="Learn Domain Driven Design")
    project.add_task(name="Do the shopping")
    project.add_task(name="Clean the house")
    session.add(project)
    session.commit()

    project.complete_task(id=task.id, now=datetime.utcnow())
    session.commit()

    typer.echo(
        tabulate(
            [
                [
                    task.id,
                    task.name,
                    task.completed_at,
                ]
                for task in project.tasks
            ],
            headers=["Id", "Name", "Completed At"],
        ),
    )
    typer.echo("\nSeeding completed 🚀")


if __name__ == "__main__":
    typer.run(main)
