from datetime import date, datetime
from typing import Annotated

from fastapi import Depends

from app.infrastructure.db import AppSession
from app.modules.projects.adapters.unit_of_work import UnitOfWork
from app.modules.projects.domain.ports import AbstractUnitOfWork
from app.modules.projects.domain.service import Service
from app.modules.projects.domain.use_cases import CreateProject


def get_current_time() -> date:
    return datetime.utcnow()


def get_uow():
    return UnitOfWork(session_factory=AppSession)


def get_service(uow: Annotated[AbstractUnitOfWork, Depends(get_uow)]) -> Service:
    return Service(uow=uow)


def get_create_project(uow: Annotated[AbstractUnitOfWork, Depends(get_uow)]) -> CreateProject:
    return CreateProject(uow=uow)
