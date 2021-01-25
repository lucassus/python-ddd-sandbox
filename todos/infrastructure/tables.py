from sqlalchemy.sql.schema import Column, ForeignKey, MetaData, Table
from sqlalchemy.sql.sqltypes import Date, Integer, String

metadata = MetaData()

projects_table = Table(
    "projects",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
    Column("max_incomplete_tasks_number", Integer),
)

tasks_table = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("project_id", Integer, ForeignKey("projects.id")),
    Column("name", String(255)),
    Column("completed_at", Date, nullable=True),
)


def create_tables(engine):
    metadata.create_all(bind=engine)


def drop_tables(engine):
    metadata.drop_all(bind=engine)
