import asyncio
from unittest.mock import Mock

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status

from app.modules.accounts.application.commands import RegisterUser
from app.modules.accounts.application.queries import GetUser
from app.modules.accounts.domain.errors import EmailAlreadyExistsException
from app.modules.accounts.domain.password import Password
from app.modules.accounts.entrypoints.dependencies import get_current_user
from app.modules.accounts.application.containers import AppContainer
from app.modules.authentication_contract import AuthenticationContract
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID
from app.shared.message_bus import MessageBus


@pytest.mark.asyncio()
async def test_register_user_endpoint(container: AppContainer, client: AsyncClient):
    # Given
    bus_mock = Mock(MessageBus)

    # When
    with container.bus.override(bus_mock):
        response = await client.post(
            "/users",
            json={
                "email": "test@email.com",
                "password": "password",
            },
            follow_redirects=False,
        )

    # Then
    bus_mock.execute.assert_called_with(
        RegisterUser(
            email=EmailAddress("test@email.com"),
            password=Password("password"),
        )
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    ("email", "password"),
    [
        ("invalid", "password"),
        ("a@b.c", "password"),
        ("test@email.com", "short"),
        ("test@email.com", ""),
        ("", ""),
    ],
)
async def test_register_user_endpoint_returns_422(client: AsyncClient, email, password):
    # When
    response = await client.post(
        "/users",
        json={"email": email, "password": password},
    )

    # Then
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_register_user_endpoint_errors_handling(container: AppContainer, client: AsyncClient):
    # Given
    bus_mock = Mock(MessageBus)
    bus_mock.execute.side_effect = EmailAlreadyExistsException(EmailAddress("taken@email.com"))

    # When
    with container.bus.override(bus_mock):
        response = await client.post(
            "/users",
            json={"email": "taken@email.com", "password": "password"},
            follow_redirects=False,
        )

    # Then
    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio()
async def test_get_current_user_endpoint(
    container: AppContainer,
    app: FastAPI,
    client: AsyncClient,
):
    # Given
    user_id = UserID.generate()

    app.dependency_overrides[get_current_user] = lambda: AuthenticationContract.Identity(
        id=user_id,
        email=EmailAddress("test@email.com"),
    )

    future = asyncio.Future[GetUser.Result]()
    future.set_result(
        GetUser.Result(
            id=user_id,
            email="test@email.com",
            projects=[
                GetUser.Result.Project(id=1, name="Project One"),
                GetUser.Result.Project(id=2, name="Project Two"),
            ],
        )
    )
    get_user_mock = Mock(return_value=future)

    # When
    with container.queries.get_user.override(get_user_mock):
        response = await client.get("/users/me")

    # Then
    get_user_mock.assert_called_with(GetUser(user_id))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": str(user_id),
        "email": "test@email.com",
        "projects": [
            {"id": 1, "name": "Project One"},
            {"id": 2, "name": "Project Two"},
        ],
    }
