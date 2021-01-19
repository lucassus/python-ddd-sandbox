from datetime import datetime

import typer
from tabulate import tabulate

from todos.adapters.db.tables import start_mappers
from todos.adapters.db.unit_of_work import UnitOfWork
from todos.domain.errors import TaskNotFoundError
from todos.service_layer.service import Service

app = typer.Typer()


start_mappers()
uow = UnitOfWork()
service = Service(project_id=1, uow=uow)


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

    service.create_task(name)
    list()


@app.command(help="Completes a task with the given ID")
def complete(id: int = typer.Option(..., help="ID of task to complete")):
    project = uow.repository.get(1)
    assert project

    try:
        service.complete_task(id, now=datetime.utcnow())
        list()
    except TaskNotFoundError:
        typer.secho(f"Cannot find a task with ID={id}", fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command(help="Undo a task with the given ID")
def incomplete(id: int = typer.Option(..., help="ID of task to incomplete")):
    project = uow.repository.get(1)
    assert project

    try:
        service.incomplete_task(id)
        list()
    except TaskNotFoundError:
        typer.secho(f"Cannot find a task with ID={id}", fg=typer.colors.RED)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    with uow:
        app()
