from typing import Annotated

from fastapi import Depends

from app.command.accounts.application.change_user_email_address import ChangeUserEmailAddress
from app.command.accounts.application.register_user import RegisterUser
from app.command.accounts.infrastructure.adapters.sqla_unit_of_work import SQLAUnitOfWork
from app.command.event_handlers import bus
from app.infrastructure.db import AppSession


def get_uow() -> SQLAUnitOfWork:
    return SQLAUnitOfWork(session_factory=AppSession)


def get_register_user(uow: Annotated[SQLAUnitOfWork, Depends(get_uow)]) -> RegisterUser:
    return RegisterUser(uow=uow, bus=bus)


def get_change_user_email_address(uow: Annotated[SQLAUnitOfWork, Depends(get_uow)]) -> ChangeUserEmailAddress:
    return ChangeUserEmailAddress(uow=uow)
