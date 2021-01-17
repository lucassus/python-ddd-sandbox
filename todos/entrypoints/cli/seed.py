from datetime import date

import typer
from tabulate import tabulate

from todos.domain.models import Project
from todos.interfaces.db.session import SessionLocal, engine
from todos.interfaces.db.tables import metadata, start_mappers

start_mappers()
session = SessionLocal()


def main(rebuild_db: bool = True):
    if rebuild_db:
        metadata.drop_all(bind=engine)
        metadata.create_all(bind=engine)

    project = Project(name="Work")

    task = project.add_task(name="Learn Python")
    task.completed_at = date(2021, 1, 9)

    project.add_task(name="Learn Domain Driven Design")
    project.add_task(name="Do the shopping")
    project.add_task(name="Clean the house")

    session.add(project)
    session.commit()

    typer.echo("Seeding tasks completed 🚀\n")

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


if __name__ == "__main__":
    typer.run(main)
