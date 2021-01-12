from fastapi import Depends
from sqlalchemy.orm import Session

from todos.interfaces.abstract_repository import AbstractRepository
from todos.interfaces.db.repository import Repository
from todos.interfaces.db.session import SessionLocal


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
