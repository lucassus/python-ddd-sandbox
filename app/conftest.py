from pathlib import Path

import pytest
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.base import Engine

from app.infrastructure.tables import create_tables, drop_tables


@pytest.fixture(scope="session")
def db_url():
    database_path = (Path(__file__).parent / "infrastructure/databases/test.db").resolve()
    return f"sqlite:///{database_path}"


@pytest.fixture(scope="session")
def db_engine(db_url) -> Engine:
    return create_engine(db_url, connect_args={"check_same_thread": False})


@pytest.fixture
def prepare_db(db_engine):
    create_tables(db_engine)
    yield
    drop_tables(db_engine)


@pytest.fixture
def connection(db_engine, prepare_db):
    with db_engine.begin() as connection:
        yield connection
