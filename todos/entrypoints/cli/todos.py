from typing import Optional

import typer
from tabulate import tabulate

from todos.interfaces.db.repository import Repository
from todos.interfaces.db.session import SessionLocal
from todos.interfaces.db.tables import start_mappers
from todos.service_layer.errors import TodoNotFoundError
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


@app.command(help="Prints the list of all tasks")
def list():
    _print_todos(repository.list())


@app.command(help="Creates a new task")
def create(
    name: str = typer.Option(..., help="Task name", prompt="Enter new task name")
):
    create_todo(name, session=session, repository=repository)
    _print_todos(repository.list())


@app.command(help="Completes a task with the given ID")
def complete(id: int = typer.Option(..., help="ID of task to complete")):
    try:
        complete_todo(id, session=session, repository=repository)
        _print_todos(repository.list())
    except TodoNotFoundError:
        typer.secho(f"Cannot find a todo with id={id}", fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command(help="Undo a task with the given ID")
def incomplete(id: int = typer.Option(..., help="ID of task to incomplete")):
    try:
        incomplete_todo(id, session=session, repository=repository)
        _print_todos(repository.list())
    except TodoNotFoundError:
        typer.secho(f"Cannot find a todo with id={id}", fg=typer.colors.RED)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
