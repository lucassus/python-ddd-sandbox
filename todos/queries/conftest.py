import pytest
from starlette.testclient import TestClient

from todos.queries.app import create_app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)
