from datetime import date

import typer
from tabulate import tabulate

from app.infrastructure.session import engine
from app.infrastructure.tables import create_tables, drop_tables, projects_table, tasks_table


def main(rebuild_db: bool = True):
    if rebuild_db:
        drop_tables(engine)
        create_tables(engine)

    connection = engine.connect()

    connection.execute(
        projects_table.insert(),
        {"id": 1, "name": "Project One"},
    )

    connection.execute(
        tasks_table.insert(),
        [
            {
                "id": 1,
                "project_id": 1,
                "name": "Learn Python",
                "completed_at": date(2021, 1, 6),
            },
            {
                "id": 2,
                "project_id": 1,
                "name": "Learn Domain Driven Design",
                "completed_at": None,
            },
            {
                "id": 3,
                "project_id": 1,
                "name": "Do the shopping",
                "completed_at": None,
            },
            {
                "id": 4,
                "project_id": 1,
                "name": "Clean the house",
                "completed_at": None,
            },
        ],
    )

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
