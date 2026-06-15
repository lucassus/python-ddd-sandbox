import pytest
from fastapi import FastAPI
from httpx2 import ASGITransport, AsyncClient

from app.modules.accounts.application.queries import GetUser
from app.modules.authentication_contract import AuthenticationError
from app.modules.errors_handling import register_error_handlers
from app.modules.shared_kernel.entities.user_id import UserID
from app.modules.shared_kernel.errors import EntityNotFoundError


@pytest.fixture
def app():
    app = FastAPI()
    register_error_handlers(app)
    return app


@pytest.fixture
def client(app):
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


@pytest.mark.asyncio
async def test_handle_page_not_found_error(client):
    response = await client.get("/foo")

    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


@pytest.mark.asyncio
async def test_handle_entity_not_found_error(app, client):
    @app.get("/foo")
    def raise_entity_not_found_error():
        raise EntityNotFoundError("Entity not found")  # noqa: TRY003

    response = await client.get("/foo")

    assert response.status_code == 404
    assert response.json() == {"detail": "Entity not found"}


@pytest.mark.asyncio
async def test_handle_user_not_found_error(app, client):
    # Given
    user_id = UserID.generate()

    @app.get("/foo")
    def raise_user_not_found_error():
        raise GetUser.NotFoundError(user_id)

    # When
    response = await client.get("/foo")

    # Then
    assert response.status_code == 404
    assert response.json() == {"detail": f"User with id {user_id} not found"}


@pytest.mark.asyncio
async def test_handle_authentication_error(app, client):
    @app.get("/foo")
    def raise_authentication_error():
        raise AuthenticationError("Authentication error")  # noqa: TRY003

    response = await client.get("/foo")

    assert response.status_code == 401
    assert response.json() == {"detail": "Authentication error"}
