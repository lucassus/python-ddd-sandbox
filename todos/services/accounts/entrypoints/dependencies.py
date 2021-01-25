from fastapi import Depends

from todos.infrastructure.session import session_factory
from todos.services.accounts.adapters.unit_of_work import UnitOfWork
from todos.services.accounts.domain.service import Service


def get_uow():
    return UnitOfWork(session_factory=session_factory)


def get_service(uow=Depends(get_uow)) -> Service:
    return Service(uow=uow)
