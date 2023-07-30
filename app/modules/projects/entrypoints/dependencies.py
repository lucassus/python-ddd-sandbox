from datetime import date, datetime
from typing import Annotated

from fastapi import Depends

from app.infrastructure.db import AppSession
from app.modules.projects.adapters.unit_of_work import UnitOfWork
from app.modules.projects.use_cases import CreateProject, TasksService
from app.modules.projects.use_cases.ports import AbstractUnitOfWork


def get_current_time() -> date:
    return datetime.utcnow()


def get_uow():
    return UnitOfWork(session_factory=AppSession)


def get_tasks_service(uow: Annotated[AbstractUnitOfWork, Depends(get_uow)]) -> TasksService:
    return TasksService(uow=uow)


def get_create_project(uow: Annotated[AbstractUnitOfWork, Depends(get_uow)]) -> CreateProject:
    return CreateProject(uow=uow)
