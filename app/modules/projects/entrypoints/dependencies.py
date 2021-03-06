from datetime import date, datetime

from fastapi import Depends

from app.infrastructure.session import session_factory
from app.modules.projects.adapters.unit_of_work import UnitOfWork
from app.modules.projects.domain.service import Service


def get_current_time() -> date:
    return datetime.utcnow()


def get_uow():
    return UnitOfWork(session_factory=session_factory)


def get_service(uow=Depends(get_uow)) -> Service:
    return Service(uow=uow)
