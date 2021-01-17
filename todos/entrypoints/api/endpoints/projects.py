from typing import List

from fastapi import APIRouter, Depends

from todos.domain.models import Project
from todos.entrypoints.api import schemas
from todos.entrypoints.api.dependencies import get_project, get_uow
from todos.interfaces.abstract_unit_of_work import AbstractUnitOfWork

router = APIRouter()


@router.get("", response_model=List[schemas.Project], name="Returns list of projects")
def projects_endpoint(uow: AbstractUnitOfWork = Depends(get_uow)):
    return uow.repository.list()


@router.get("/{project_id}", response_model=schemas.Project)
def project_endpoint(project: Project = Depends(get_project)):
    return project
