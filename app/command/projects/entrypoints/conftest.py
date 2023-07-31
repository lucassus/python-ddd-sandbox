import pytest
from fastapi import FastAPI
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app.command.projects.entrypoints.dependencies import get_uow
from app.command.projects.entrypoints.routes.projects import router
from app.command.projects.infrastructure.adapters.sqla_unit_of_work import SQLAUnitOfWork


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(connection, app: FastAPI):
    def session_factory():
        return Session(bind=connection)

    uow = SQLAUnitOfWork(session_factory=session_factory)

    app.dependency_overrides[get_uow] = lambda: uow

    with uow:
        yield TestClient(app)
