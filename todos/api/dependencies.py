from fastapi import Depends
from sqlalchemy.orm import Session

from todos.db.repository import Repository
from todos.db.session import SessionLocal


# TODO: It couples api with the db, consider unit of work design pattern
def get_session():
    session = SessionLocal()

    try:
        yield session
    except Exception:
        session.rollback()
    finally:
        session.close()


def get_repository(session: Session = Depends(get_session)):
    return Repository(session=session)
