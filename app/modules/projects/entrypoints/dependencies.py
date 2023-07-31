from datetime import date, datetime
from typing import Annotated

from fastapi import Depends

from app.infrastructure.db import AppSession
from app.modules.projects.application.create_project import CreateProject
from app.modules.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.projects.application.tasks_service import TasksService
from app.modules.projects.entrypoints.adapters.sqla_unit_of_work import SQLAUnitOfWork


def get_current_time() -> date:
    return datetime.utcnow()


def get_uow():
    return SQLAUnitOfWork(session_factory=AppSession)


def get_tasks_service(uow: Annotated[AbstractUnitOfWork, Depends(get_uow)]) -> TasksService:
    return TasksService(uow=uow)


def get_create_project(uow: Annotated[AbstractUnitOfWork, Depends(get_uow)]) -> CreateProject:
    return CreateProject(uow=uow)
