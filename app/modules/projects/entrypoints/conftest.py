import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.modules.authentication_contract import AuthenticationContract
from app.modules.projects.entrypoints import routes
from app.modules.projects.entrypoints.containers import Container
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID


@pytest.fixture(autouse=True)
def container():
    container = Container()
    container.wire()

    return container


@pytest.fixture()
def app():
    app = FastAPI()
    app.include_router(routes.router)

    app.dependency_overrides[routes.get_current_user] = lambda: AuthenticationContract.CurrentUserDTO(
        id=UserID.generate(),
        email=EmailAddress("test@email.com"),
    )

    return app


@pytest.fixture()
def client(app):
    return TestClient(app)
