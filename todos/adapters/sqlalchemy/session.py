from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from todos.adapters.sqlalchemy.config import DB_URL

engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

session_factory = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_session() -> Session:
    return session_factory()
