from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from todos.adapters.db.config import DB_URL

engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False},
    echo=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
