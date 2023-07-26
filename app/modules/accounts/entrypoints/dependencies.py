from typing import Annotated

from fastapi import Depends

from app.infrastructure.db import AppSession
from app.modules.accounts.adapters.unit_of_work import UnitOfWork
from app.modules.accounts.domain.register_user_use_case import RegisterUserUseCase
from app.modules.message_bus import bus


def get_uow():
    return UnitOfWork(session_factory=AppSession)


def get_register_user_use_case(uow: Annotated[UnitOfWork, Depends(get_uow)]) -> RegisterUserUseCase:
    return RegisterUserUseCase(uow=uow, bus=bus)
