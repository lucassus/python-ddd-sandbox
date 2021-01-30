from sqlalchemy.orm import mapper, relationship

from app.infrastructure.tables import projects_table, tasks_table
from app.services.projects.domain.entities import Project, Task


def start_mappers():
    mapper(
        Project,
        projects_table,
        properties={
            "tasks": relationship(Task, order_by=tasks_table.c.id),
        },
    )

    mapper(Task, tasks_table)
