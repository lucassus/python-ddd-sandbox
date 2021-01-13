from datetime import date

import typer
from tabulate import tabulate

from todos.domain.models.todo import Todo
from todos.interfaces.db.session import SessionLocal, engine
from todos.interfaces.db.tables import metadata, start_mappers

start_mappers()
session = SessionLocal()


def main(rebuild_db: bool = True):
    if rebuild_db:
        metadata.drop_all(bind=engine)
        metadata.create_all(bind=engine)

    session.add(Todo(name="Learn Python", completed_at=date(2021, 1, 9)))
    session.add(Todo(name="Clean the house"))
    session.add(Todo(name="Do the shopping"))
    session.add(Todo(name="Learn Domain Driven Design"))
    session.commit()

    typer.echo("Seeding todos completed 🚀\n")

    # TODO: Dry it
    todos = session.query(Todo).all()
    typer.echo(
        tabulate(
            [[todo.id, todo.name, todo.completed_at] for todo in todos],
            headers=["Id", "Name", "Completed At"],
        ),
    )


if __name__ == "__main__":
    typer.run(main)
