import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from todos.commands.adapters.unit_of_work import UnitOfWork
from todos.commands.entrypoints.api.dependencies import get_uow
from todos.commands.entrypoints.api.routes import api_router
from todos.commands.test_utils.fake_unit_of_work import FakeUnitOfWork


@pytest.fixture
def client(request):
    app = FastAPI()
    app.include_router(api_router)

    if "integration" in request.keywords:
        # For tests marked as "integration" create Unit Of Work
        # instance that uses the database...
        session = request.getfixturevalue("session")
        uow = UnitOfWork(session_factory=session)
    else:
        # ...otherwise go with the fake implementation.
        uow = FakeUnitOfWork(projects=[])

    app.dependency_overrides[get_uow] = lambda: uow

    with uow:
        yield TestClient(app)
