import pytest
from fastapi import FastAPI
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from todos.services.project_management.adapters.unit_of_work import UnitOfWork
from todos.services.project_management.entrypoints.dependencies import get_uow
from todos.services.project_management.entrypoints.routes import api_router
from todos.services.project_management.test_utils.fake_unit_of_work import (
    FakeUnitOfWork,
)


@pytest.fixture
def client(request):
    app = FastAPI()
    app.include_router(api_router)

    if "integration" in request.keywords:
        # For tests marked as "integration" create Unit Of Work
        # instance that uses the database...
        db_connection = request.getfixturevalue("db_connection")
        uow = UnitOfWork(session_factory=lambda: Session(bind=db_connection))
    else:
        # ...otherwise go with the fake implementation.
        uow = FakeUnitOfWork(projects=[])

    app.dependency_overrides[get_uow] = lambda: uow

    with uow:
        yield TestClient(app)
