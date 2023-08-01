import pytest
from sqlalchemy.orm import clear_mappers

from app.command import mapper_registry
from app.command.accounts.infrastructure.mappers import start_mappers as start_account_mappers
from app.command.projects.infrastructure.mappers import start_mappers as start_project_mappers
from app.infrastructure.db import AppSession, engine
from app.infrastructure.tables import create_tables, drop_tables


@pytest.fixture
def prepare_db():
    create_tables(engine)

    clear_mappers()
    start_account_mappers(mapper_registry)
    start_project_mappers(mapper_registry)

    yield

    clear_mappers()
    drop_tables(engine)


@pytest.fixture
def connection(prepare_db):
    with engine.begin() as connection:
        yield connection


@pytest.fixture
def session(connection):
    session = AppSession(bind=connection)
    yield session
    session.close()
