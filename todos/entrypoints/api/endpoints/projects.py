from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from todos.domain.models import Project
from todos.entrypoints.api import schemas
from todos.entrypoints.api.dependencies import get_uow
from todos.interfaces.abstract_unit_of_work import AbstractUnitOfWork

router = APIRouter()


@router.get("", response_model=List[schemas.Project], name="Returns list of projects")
def projects_endpoint(uow: AbstractUnitOfWork = Depends(get_uow)):
    return uow.repository.list()


def get_project(
    id: int,
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> Project:
    project = uow.repository.get(id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unable to find a project with ID={id}",
        )

    return project


@router.get("/{id}", response_model=schemas.Project)
def project_endpoint(project: Project = Depends(get_project)):
    return project
