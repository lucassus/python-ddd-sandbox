import pytest
from fastapi import FastAPI
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app.modules.projects.adapters.unit_of_work import UnitOfWork
from app.modules.projects.entrypoints.dependencies import get_uow
from app.modules.projects.entrypoints.routes import router


@pytest.fixture
def client(db_connection):
    app = FastAPI()
    app.include_router(router)

    def session_factory():
        return Session(bind=db_connection)

    uow = UnitOfWork(session_factory=session_factory)

    app.dependency_overrides[get_uow] = lambda: uow

    with uow:
        yield TestClient(app)
