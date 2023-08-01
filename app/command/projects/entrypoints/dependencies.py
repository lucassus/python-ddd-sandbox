from typing import Annotated

from fastapi import Depends

from app.command.projects.application.create_project import CreateProject
from app.command.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.command.projects.application.tasks_service import TasksService
from app.command.projects.infrastructure.adapters.unit_of_work import UnitOfWork
from app.infrastructure.db import AppSession


def get_uow() -> UnitOfWork:
    return UnitOfWork(session_factory=AppSession)


def get_tasks_service(uow: Annotated[AbstractUnitOfWork, Depends(get_uow)]) -> TasksService:
    return TasksService(uow=uow)


def get_create_project(uow: Annotated[AbstractUnitOfWork, Depends(get_uow)]) -> CreateProject:
    return CreateProject(uow=uow)
