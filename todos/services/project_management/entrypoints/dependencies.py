from datetime import date, datetime

from fastapi import Depends

from todos.infrastructure.session import session_factory
from todos.services.project_management.adapters.unit_of_work import UnitOfWork
from todos.services.project_management.domain.service import Service


def get_current_time() -> date:
    return datetime.utcnow()


# TODO: Bring back the old idea with true context manager
def get_uow():
    return UnitOfWork(session_factory=session_factory)


def get_service(uow=Depends(get_uow)) -> Service:
    return Service(uow=uow)
