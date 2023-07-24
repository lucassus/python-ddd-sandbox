import os

import pytest
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.base import Engine

from app.infrastructure.tables import create_tables, drop_tables


@pytest.fixture(scope="session")
def db_url():
    database_path = os.path.join(os.path.dirname(__file__), "../db/test.db")
    return f"sqlite:///{database_path}"


@pytest.fixture(scope="session")
def db_engine(db_url) -> Engine:
    return create_engine(db_url, connect_args={"check_same_thread": False})


@pytest.fixture
def prepare_db(db_engine):
    create_tables(db_engine)
    yield
    drop_tables(db_engine)
