import pytest
from sqlalchemy.orm import clear_mappers

from app.infrastructure.db import AppSession, engine
from app.infrastructure.tables import create_tables, drop_tables
from app.modules import mapper_registry
from app.modules.accounts.infrastructure.mappers import start_mappers as start_account_mappers
from app.modules.projects.infrastructure.mappers import start_mappers as start_project_mappers


@pytest.fixture(autouse=True)
def _prepare_db():
    create_tables(engine)

    clear_mappers()
    start_account_mappers(mapper_registry)
    start_project_mappers(mapper_registry)

    yield

    clear_mappers()
    drop_tables(engine)


@pytest.fixture()
def session():
    session = AppSession(bind=engine)
    yield session
    session.close()
