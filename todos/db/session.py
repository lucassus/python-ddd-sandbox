import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_file = os.path.join(os.path.dirname(__file__), "../../todos.db")
engine = create_engine(
    f"sqlite:///{db_file}", connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
