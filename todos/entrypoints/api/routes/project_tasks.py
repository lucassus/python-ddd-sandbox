from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Path, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy import and_, select

from todos.adapters.sqlalchemy.session import engine
from todos.adapters.sqlalchemy.tables import tasks_table
from todos.domain.entities import Project
from todos.domain.service import Service
from todos.entrypoints.api import schemas
from todos.entrypoints.api.dependencies import (
    get_current_time,
    get_project,
    get_service,
)

router = APIRouter()


@router.get("", response_model=List[schemas.Task], name="Returns list of tasks_table")
def tasks_endpoint(project: Project = Depends(get_project)):

    return project.tasks


@router.post("")
def task_create_endpoint(
    project_id: int,
    data: schemas.CreateTask,
    request: Request,
    service: Service = Depends(get_service),
):
    task = service.create_task(data.name)

    return RedirectResponse(
        url=request.url_for("task_endpoint", project_id=project_id, id=task.id),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/{id}", response_model=schemas.Task)
def task_endpoint(
    project_id: int,
    id: int = Path(..., description="The ID of the task", ge=1),
):
    with engine.connect() as connection:
        stmt = select([tasks_table]).where(
            and_(tasks_table.c.id == id, tasks_table.c.project_id == project_id)
        )
        return connection.execute(stmt).fetchone()


@router.put("/{id}/complete", response_model=schemas.Task)
def task_complete_endpoint(
    id: int = Path(..., description="The ID of the task", ge=1),
    service: Service = Depends(get_service),
    now: date = Depends(get_current_time),
):
    return service.complete_task(id, now=now)


@router.put("/{id}/incomplete", response_model=schemas.Task)
def task_incomplete_endpoint(
    id: int = Path(..., description="The ID of the task", ge=1),
    service: Service = Depends(get_service),
):
    return service.incomplete_task(id)
