import pytest
from httpx import AsyncClient

from todos.queries.app import create_app


@pytest.fixture
def client():
    app = create_app()
    return AsyncClient(app=app, base_url="http://test")
