from fastapi import Depends

from app.infrastructure.db import session_factory
from app.modules.accounts.adapters.unit_of_work import UnitOfWork
from app.modules.accounts.domain.service import Service
from app.modules.message_bus import bus


def get_uow():
    return UnitOfWork(session_factory=session_factory)


def get_service(uow=Depends(get_uow)) -> Service:
    return Service(uow=uow, bus=bus)
