from datetime import date

import typer
from tabulate import tabulate

from app.infrastructure.factories import create_project, create_task, create_user
from app.infrastructure.session import engine
from app.infrastructure.tables import create_tables, drop_tables, tasks_table


def main(rebuild_db: bool = True):
    if rebuild_db:
        drop_tables(engine)
        create_tables(engine)

    connection = engine.connect()

    create_project(connection)
    user_id = create_user(connection, email="test@email.com").id
    project_id = create_project(connection, user_id, name="Project One").id

    create_task(connection, project_id, name="Learn Python", completed_at=date(2021, 1, 6))
    create_task(connection, project_id, name="Learn Domain Driven Design")
    create_task(connection, project_id, name="Do the shopping")
    create_task(connection, project_id, name="Clean the house")

    tasks = connection.execute(tasks_table.select())

    typer.echo(
        tabulate(
            [
                [
                    task.id,
                    task.name,
                    task.completed_at,
                ]
                for task in tasks
            ],
            headers=["Id", "Name", "Completed At"],
        ),
    )
    typer.echo("\nSeeding completed 🚀")


if __name__ == "__main__":
    typer.run(main)
