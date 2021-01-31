import pytest
from sqlalchemy.orm import Session

from app.modules.projects.adapters.mappers import start_mappers

start_mappers()


@pytest.fixture
def db_connection(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()

    yield connection

    transaction.rollback()
    connection.close()


@pytest.fixture
def session(request, db_connection):
    session = Session(bind=db_connection)
    yield session
    session.close()
