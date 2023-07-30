from sqlalchemy.orm import relationship

from app.infrastructure.tables import projects_table, tasks_table
from app.modules.projects.domain.project import Project, Task


def start_mappers(mapper_registry):
    mapper_registry.map_imperatively(
        Project,
        projects_table,
        properties={
            "tasks": relationship(Task, order_by=tasks_table.c.id),
        },
    )

    mapper_registry.map_imperatively(Task, tasks_table)
