from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from todos.config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    echo=False,
)

session_factory = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
