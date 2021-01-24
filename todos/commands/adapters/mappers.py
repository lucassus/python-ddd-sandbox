from sqlalchemy.orm import mapper, relationship

from todos.commands.domain.entities import Project, Task
from todos.infrastructure.tables import projects_table, tasks_table


def start_mappers():
    mapper(
        Project,
        projects_table,
        properties={
            "tasks": relationship(Task, order_by=tasks_table.c.id),
        },
    )

    mapper(Task, tasks_table)
