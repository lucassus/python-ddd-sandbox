from sqlalchemy.orm import relationship

from app.command.projects.entities.project import Project, Task
from app.infrastructure.tables import projects_table, tasks_table


def start_mappers(mapper_registry):
    mapper_registry.map_imperatively(
        Project,
        projects_table,
        properties={
            "tasks": relationship(Task, order_by=tasks_table.c.id),
        },
    )

    mapper_registry.map_imperatively(Task, tasks_table)
