import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.modules.authentication_contract import AuthenticationContract
from app.modules.projects.entrypoints import routes
from app.modules.projects.entrypoints.dependencies import get_current_user
from app.modules.projects.infrastructure.containers import Container
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID


@pytest.fixture(autouse=True)
def container():
    container = Container()
    container.wire(
        modules=[".dependencies"],
        packages=[".routes"],
    )

    return container


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(routes.router)

    app.dependency_overrides[get_current_user] = lambda: AuthenticationContract.Identity(
        id=UserID.generate(),
        email=EmailAddress("test@email.com"),
    )

    return app


@pytest.fixture
def client(app):
    return AsyncClient(app=app, base_url="http://test")
