from datetime import date

import typer
from tabulate import tabulate

from todos.domain.models.task import Task
from todos.interfaces.db.session import SessionLocal, engine
from todos.interfaces.db.tables import metadata, start_mappers

start_mappers()
session = SessionLocal()


def main(rebuild_db: bool = True):
    if rebuild_db:
        metadata.drop_all(bind=engine)
        metadata.create_all(bind=engine)

    session.add(Task(name="Learn Python", completed_at=date(2021, 1, 9)))
    session.add(Task(name="Clean the house"))
    session.add(Task(name="Do the shopping"))
    session.add(Task(name="Learn Domain Driven Design"))
    session.commit()

    typer.echo("Seeding tasks completed 🚀\n")

    tasks = session.query(Task).all()
    typer.echo(
        tabulate(
            [[task.id, task.name, task.completed_at] for task in tasks],
            headers=["Id", "Name", "Completed At"],
        ),
    )


if __name__ == "__main__":
    typer.run(main)
