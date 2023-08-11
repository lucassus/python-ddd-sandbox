from sqlalchemy.orm import attribute_keyed_dict, relationship

from app.command.projects.domain.project import Project, Task
from app.infrastructure.tables import projects_table, tasks_table


def start_mappers(mapper_registry):
    mapper_registry.map_imperatively(
        Project,
        projects_table,
        properties={
            "_id": projects_table.c.id,
            "_user_id": projects_table.c.user_id,
            "_name": projects_table.c.name,
            "_maximum_number_of_incomplete_tasks": projects_table.c.maximum_number_of_incomplete_tasks,
            "_last_task_number": projects_table.c.last_task_number,
            "_tasks_by_number": relationship(
                Task,
                collection_class=attribute_keyed_dict("number"),
            ),
            "_archived_at": projects_table.c.archived_at,
            "_deleted_at": projects_table.c.deleted_at,
        },
    )

    mapper_registry.map_imperatively(
        Task,
        tasks_table,
        properties={
            "_number": tasks_table.c.number,
            "_name": tasks_table.c.name,
            "_completed_at": tasks_table.c.completed_at,
        },
    )
