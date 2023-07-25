import pytest

from app.infrastructure.db import engine
from app.infrastructure.tables import create_tables, drop_tables


@pytest.fixture
def prepare_db():
    create_tables(engine)
    yield
    drop_tables(engine)


@pytest.fixture
def connection(prepare_db):
    with engine.begin() as connection:
        yield connection
