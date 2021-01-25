from sqlalchemy.orm import mapper, relationship

from todos.infrastructure.tables import projects_table, tasks_table
from todos.services.project_management.domain.entities import Project, Task


def start_mappers():
    mapper(
        Project,
        projects_table,
        properties={
            "tasks": relationship(Task, order_by=tasks_table.c.id),
        },
    )

    mapper(Task, tasks_table)
