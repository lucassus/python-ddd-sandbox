from typing import Annotated

from fastapi import Depends

from app.command.accounts.adapters.unit_of_work import UnitOfWork
from app.command.accounts.use_cases import ChangeUserEmailAddress, RegisterUser
from app.command.event_handlers import bus
from app.infrastructure.db import AppSession


def get_uow():
    return UnitOfWork(session_factory=AppSession)


def get_register_user(uow: Annotated[UnitOfWork, Depends(get_uow)]) -> RegisterUser:
    return RegisterUser(uow=uow, bus=bus)


def get_change_user_email_address(uow: Annotated[UnitOfWork, Depends(get_uow)]) -> ChangeUserEmailAddress:
    return ChangeUserEmailAddress(uow=uow)
