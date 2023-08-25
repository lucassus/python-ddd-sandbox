import uuid

from sqlalchemy.sql.schema import Column, ForeignKey, MetaData, Table, UniqueConstraint
from sqlalchemy.sql.sqltypes import DateTime, Integer, String, Uuid

from app.infrastructure.type_decorators import EmailType, PasswordType

metadata = MetaData()

users_table = Table(
    "users",
    metadata,
    Column("id", Uuid(), primary_key=True, default=lambda: uuid.uuid4()),
    Column("email", EmailType(), nullable=False, unique=True),
    Column("password", PasswordType(), nullable=False),
)

projects_table = Table(
    "projects",
    metadata,
    Column("id", Integer(), primary_key=True, autoincrement=True),
    Column("user_id", Uuid(), ForeignKey(users_table.c.id), nullable=False),
    Column("name", String(255), nullable=False),
    Column("last_task_number", Integer(), nullable=False, default=0),
    Column("maximum_number_of_incomplete_tasks", Integer(), nullable=True, default=None),
    Column("archived_at", DateTime(), nullable=True, default=None),
    Column("deleted_at", DateTime(), nullable=True, default=None),
)

tasks_table = Table(
    "tasks",
    metadata,
    Column("id", Integer(), primary_key=True, autoincrement=True),
    Column("project_id", Integer(), ForeignKey(projects_table.c.id), nullable=False),
    Column("number", Integer(), nullable=False),
    Column("name", String(255), nullable=False),
    Column("created_by", Uuid(), ForeignKey(users_table.c.id), nullable=True),
    Column("completed_at", DateTime(), nullable=True, default=None),
    UniqueConstraint("project_id", "number"),
)


def create_tables(engine):
    metadata.create_all(bind=engine)


def drop_tables(engine):
    metadata.drop_all(bind=engine)
