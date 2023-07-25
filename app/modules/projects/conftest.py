import pytest
from sqlalchemy.orm import Session, registry

from app.modules.projects.adapters.mappers import start_mappers

mapper_registry = registry()
start_mappers(mapper_registry)


@pytest.fixture
def session(connection, prepare_db):
    session = Session(bind=connection)
    yield session
    session.close()
