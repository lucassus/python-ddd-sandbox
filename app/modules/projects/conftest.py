import pytest
from sqlalchemy.orm import Session, registry

from app.modules.projects.adapters.mappers import start_mappers

mapper_registry = registry()
start_mappers(mapper_registry)


@pytest.fixture
def db_connection(db_engine):
    connection = db_engine.connect()
    yield connection
    connection.close()


@pytest.fixture
def session(request, db_connection, prepare_db):
    session = Session(bind=db_connection)
    yield session
    session.close()
