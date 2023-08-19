import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.modules.authentication_contract import AuthenticationContract
from app.modules.projects.entrypoints import routes
from app.modules.projects.entrypoints.containers import Container
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID

_container = Container()


@pytest.fixture(scope="session", autouse=True)
def _wire_container():
    _container.wire()


@pytest.fixture()
def container():
    return _container


@pytest.fixture()
def app():
    app = FastAPI()
    app.include_router(routes.router)

    app.dependency_overrides[routes.get_current_user] = lambda: AuthenticationContract.CurrentUserDTO(
        id=UserID(1),
        email=EmailAddress("test@email.com"),
    )

    return app


@pytest.fixture()
def client(app):
    return TestClient(app)
