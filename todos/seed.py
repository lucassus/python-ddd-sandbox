from datetime import date

import typer

from todos.domain.models.todo import Todo
from todos.interfaces.db.session import SessionLocal, engine
from todos.interfaces.db.tables import metadata, start_mappers


def main(rebuild_db: bool = True):
    if rebuild_db:
        metadata.drop_all(bind=engine)
        metadata.create_all(bind=engine)

    start_mappers()

    session = SessionLocal()

    session.add(Todo(name="Learn Python", completed_at=date(2021, 1, 9)))
    session.add(Todo(name="Clean house"))
    session.add(Todo(name="Do shopping"))
    session.commit()

    typer.echo("Seeding completed 🚀")

    todos = session.query(Todo).all()
    typer.echo(todos)


if __name__ == "__main__":
    typer.run(main)
