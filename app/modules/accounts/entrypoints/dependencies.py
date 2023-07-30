from typing import Annotated

from fastapi import Depends

from app.infrastructure.db import AppSession
from app.modules.accounts.adapters.unit_of_work import UnitOfWork
from app.modules.accounts.use_cases import ChangeUserEmailAddress, RegisterUser
from app.modules.message_bus import bus


def get_uow():
    return UnitOfWork(session_factory=AppSession)


def get_register_user(uow: Annotated[UnitOfWork, Depends(get_uow)]) -> RegisterUser:
    return RegisterUser(uow=uow, bus=bus)


def get_change_user_email_address(uow: Annotated[UnitOfWork, Depends(get_uow)]) -> ChangeUserEmailAddress:
    return ChangeUserEmailAddress(uow=uow)
