from fastapi import Depends

from app.infrastructure.session import session_factory
from app.services.accounts.adapters.unit_of_work import UnitOfWork
from app.services.accounts.domain.service import Service
from app.services.message_bus import bus


def get_uow():
    return UnitOfWork(session_factory=session_factory)


def get_service(uow=Depends(get_uow)) -> Service:
    return Service(uow=uow, bus=bus)
