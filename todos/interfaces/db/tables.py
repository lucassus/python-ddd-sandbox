from sqlalchemy import Column, Date, Integer, MetaData, String, Table
from sqlalchemy.orm import mapper

from todos.domain.models.task import Task

metadata = MetaData()

todos = Table(
    "todos",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
    Column("completed_at", Date, nullable=True),
)


def start_mappers():
    mapper(Task, todos)
