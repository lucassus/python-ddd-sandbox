import pytest
from starlette.testclient import TestClient

from app.infrastructure.db import engine
from app.infrastructure.tables import create_tables, drop_tables
from app.main import create_app


@pytest.fixture(scope="function", autouse=True)
def prepare_db():
    create_tables(engine)
    yield
    drop_tables(engine)


@pytest.fixture(scope="session")
def client():
    app = create_app()
    return TestClient(app)
