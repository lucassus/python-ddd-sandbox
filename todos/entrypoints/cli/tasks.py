import typer
from tabulate import tabulate

from todos.interfaces.db.tables import start_mappers
from todos.service_layer.services import complete_task, create_task, incomplete_task
from todos.service_layer.unit_of_work import UnitOfWork

app = typer.Typer()


start_mappers()
uow = UnitOfWork()


@app.command(help="Prints the list of all tasks")
def list():
    tasks = uow.repository.list()

    typer.echo(
        tabulate(
            [[task.id, task.name, task.completed_at] for task in tasks],
            headers=["Id", "Name", "Completed At"],
        )
    )


@app.command(help="Creates a new task")
def create(
    name: str = typer.Option(..., help="Task name", prompt="Enter new task name")
):
    create_task(name, uow=uow)
    list()


@app.command(help="Completes a task with the given ID")
def complete(id: int = typer.Option(..., help="ID of task to complete")):
    task = uow.repository.get(id)

    if task is None:
        typer.secho(f"Cannot find a task with ID={id}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    complete_task(task, uow=uow)
    list()


@app.command(help="Undo a task with the given ID")
def incomplete(id: int = typer.Option(..., help="ID of task to incomplete")):
    task = uow.repository.get(id)

    if task is None:
        typer.secho(f"Cannot find a task with ID={id}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    incomplete_task(task, uow=uow)
    list()


if __name__ == "__main__":
    with uow:
        app()
