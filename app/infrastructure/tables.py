from sqlalchemy.sql.schema import Column, ForeignKey, MetaData, Table
from sqlalchemy.sql.sqltypes import Date, Integer, String

metadata = MetaData()

users_table = Table(
    "users",
    metadata,
    Column("id", Integer(), primary_key=True, autoincrement=True),
    Column("email", String(255), nullable=False, unique=True),
    Column("password", String(255), nullable=False),
)

projects_table = Table(
    "projects",
    metadata,
    Column("id", Integer(), primary_key=True, autoincrement=True),
    Column("user_id", Integer(), ForeignKey(users_table.c.id), nullable=False),
    Column("name", String(255), nullable=False),
    Column("max_incomplete_tasks_number", Integer(), nullable=True),
)

tasks_table = Table(
    "tasks",
    metadata,
    Column("id", Integer(), primary_key=True, autoincrement=True),
    Column("project_id", Integer(), ForeignKey(projects_table.c.id), nullable=False),
    Column("name", String(255), nullable=False),
    Column("completed_at", Date(), nullable=True),
)


def create_tables(engine):
    metadata.create_all(bind=engine)


def drop_tables(engine):
    metadata.drop_all(bind=engine)
