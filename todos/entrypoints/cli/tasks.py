from datetime import datetime

import typer
from tabulate import tabulate

from todos.domain.errors import TaskNotFoundError
from todos.interfaces.db.tables import start_mappers
from todos.interfaces.db.unit_of_work import UnitOfWork
from todos.service_layer.services import complete_task, create_task, incomplete_task

app = typer.Typer()


start_mappers()
uow = UnitOfWork()


@app.command(help="Prints the list of all tasks")
def list():
    project = uow.repository.get(1)
    assert project

    typer.echo(
        tabulate(
            [[task.id, task.name, task.completed_at] for task in project.tasks],
            headers=["Id", "Name", "Completed At"],
        )
    )


@app.command(help="Creates a new task")
def create(
    name: str = typer.Option(..., help="Task name", prompt="Enter new task name")
):
    project = uow.repository.get(1)
    assert project

    create_task(name, project=project, uow=uow)
    list()


@app.command(help="Completes a task with the given ID")
def complete(id: int = typer.Option(..., help="ID of task to complete")):
    project = uow.repository.get(1)
    assert project

    try:
        complete_task(id, project=project, now=datetime.utcnow(), uow=uow)
        list()
    except TaskNotFoundError:
        typer.secho(f"Cannot find a task with ID={id}", fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command(help="Undo a task with the given ID")
def incomplete(id: int = typer.Option(..., help="ID of task to incomplete")):
    project = uow.repository.get(1)
    assert project

    try:
        incomplete_task(id, project=project, uow=uow)
        list()
    except TaskNotFoundError:
        typer.secho(f"Cannot find a task with ID={id}", fg=typer.colors.RED)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    with uow:
        app()
