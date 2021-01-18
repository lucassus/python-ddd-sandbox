from sqlalchemy import Column, Date, ForeignKey, Integer, MetaData, String, Table
from sqlalchemy.orm import mapper, relationship

from todos.domain.entities import Project, Task

metadata = MetaData()

projects = Table(
    "projects",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
    Column("allowed_number_of_unfinished_tasks", Integer),
)

tasks = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("project_id", Integer, ForeignKey("projects.id")),
    Column("name", String(255)),
    Column("completed_at", Date, nullable=True),
)


def start_mappers():
    mapper(
        Project,
        projects,
        properties={
            "tasks": relationship(Task, backref="project", order_by=tasks.c.id),
        },
    )

    mapper(Task, tasks)
