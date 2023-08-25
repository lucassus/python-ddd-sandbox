import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from app.modules import register_error_handlers
from app.modules.accounts.queries.find_user_query import GetUserQuery
from app.modules.authentication_contract import AuthenticationError
from app.modules.shared_kernel.entities.user_id import UserID
from app.modules.shared_kernel.errors import EntityNotFoundError


@pytest.fixture()
def app():
    app = FastAPI()
    register_error_handlers(app)
    return app


@pytest.fixture()
def client(app):
    return TestClient(app)


def test_handle_page_not_found_error(client):
    response = client.get("/foo")

    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_handle_entity_not_found_error(app, client):
    @app.get("/foo")
    def raise_entity_not_found_error():
        raise EntityNotFoundError("Entity not found")  # noqa: TRY003

    response = client.get("/foo")

    assert response.status_code == 404
    assert response.json() == {"detail": "Entity not found"}


def test_handle_user_not_found_error(app, client):
    # Given
    user_id = UserID.generate()

    @app.get("/foo")
    def raise_user_not_found_error():
        raise GetUserQuery.NotFoundError(user_id)

    # When
    response = client.get("/foo")

    # Then
    assert response.status_code == 404
    assert response.json() == {"detail": f"User with id {user_id} not found"}


def test_handle_authentication_error(app, client):
    @app.get("/foo")
    def raise_authentication_error():
        raise AuthenticationError("Authentication error")  # noqa: TRY003

    response = client.get("/foo")

    assert response.status_code == 401
    assert response.json() == {"detail": "Authentication error"}
