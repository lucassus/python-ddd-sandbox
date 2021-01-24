from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from todos.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

session_factory = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
