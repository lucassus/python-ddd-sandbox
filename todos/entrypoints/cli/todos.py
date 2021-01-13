import typer
from tabulate import tabulate

from todos.interfaces.db.repository import Repository
from todos.interfaces.db.session import SessionLocal
from todos.interfaces.db.tables import start_mappers
from todos.service_layer.services import complete_todo, create_todo, incomplete_todo

app = typer.Typer()


# TODO: Move to utils or something like that
def _print_todos(todos):
    typer.echo(
        tabulate(
            [[todo.id, todo.name, todo.completed_at] for todo in todos],
            headers=["Id", "Name", "Completed At"],
        ),
    )


start_mappers()
session = SessionLocal()
repository = Repository(session=session)


@app.command()
def list():
    _print_todos(repository.list())


@app.command()
def create(name: str):
    create_todo(name, session=session, repository=repository)
    _print_todos(repository.list())


# TODO: Handle TodoNotFoundError
@app.command()
def complete(id: int):
    complete_todo(id, session=session, repository=repository)
    _print_todos(repository.list())


# TODO: Handle TodoNotFoundError
@app.command()
def incomplete(id: int):
    incomplete_todo(id, session=session, repository=repository)
    _print_todos(repository.list())


if __name__ == "__main__":
    app()
