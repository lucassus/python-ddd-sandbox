from datetime import date, datetime

from fastapi import Depends, HTTPException
from starlette import status

from todos.adapters.sqlalchemy.session import get_session
from todos.adapters.sqlalchemy.unit_of_work import UnitOfWork
from todos.domain.entities import Project
from todos.service_layer.ports import AbstractUnitOfWork
from todos.service_layer.service import Service


def get_current_time() -> date:
    return datetime.utcnow()


def get_uow():
    session = get_session()

    try:
        yield UnitOfWork(session=session)
    except:  # noqa
        session.close()


def get_project(
    project_id: int,
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> Project:
    project = uow.repository.get(project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unable to find a project with ID={project_id}",
        )

    return project


def get_service(
    project_id: int,
    uow=Depends(get_uow),
) -> Service:
    return Service(project_id=project_id, uow=uow)
