from fastapi import Depends
from sqlalchemy.orm import Session

from todos.db.abstract_repository import AbstractRepository
from todos.db.repository import Repository
from todos.db.session import SessionLocal


def get_session():
    session = SessionLocal()

    try:
        yield session
    except Exception:
        session.rollback()
    finally:
        session.close()


def get_repository(session: Session = Depends(get_session)) -> AbstractRepository:
    return Repository(session=session)
