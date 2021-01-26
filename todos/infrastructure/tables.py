from sqlalchemy.sql.schema import Column, ForeignKey, MetaData, Table
from sqlalchemy.sql.sqltypes import Date, Integer, String

metadata = MetaData()


class PrimaryIdColumn(Column):
    def __init__(self):
        super().__init__("id", Integer, primary_key=True, autoincrement=True)


users_table = Table(
    "users",
    metadata,
    PrimaryIdColumn(),
    Column("email", String(255)),
    Column("password", String(255)),
)

projects_table = Table(
    "projects",
    metadata,
    PrimaryIdColumn(),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("name", String(255)),
    Column("max_incomplete_tasks_number", Integer),
)

tasks_table = Table(
    "tasks",
    metadata,
    PrimaryIdColumn(),
    Column("project_id", Integer, ForeignKey("projects.id")),
    Column("name", String(255)),
    Column("completed_at", Date, nullable=True),
)


def create_tables(engine):
    metadata.create_all(bind=engine)


def drop_tables(engine):
    metadata.drop_all(bind=engine)
