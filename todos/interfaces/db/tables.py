from sqlalchemy import Column, Date, ForeignKey, Integer, MetaData, String, Table
from sqlalchemy.orm import mapper

from todos.domain.models.project import Project
from todos.domain.models.task import Task

metadata = MetaData()

projects = Table(
    "projects",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
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
    mapper(Project, projects)
    mapper(Task, tasks)
