from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status

from todos.domain.models.task import Task
from todos.entrypoints.api import schemas
from todos.entrypoints.api.dependencies import (
    CompleteTaskHandler,
    CreateTaskHandler,
    IncompleteTaskHandler,
    get_repository,
)
from todos.interfaces.abstract_repository import AbstractRepository

router = APIRouter()


@router.get("", response_model=List[schemas.Task])
def todos_endpoint(
    repository: AbstractRepository = Depends(get_repository),
):
    return repository.list()


@router.post("", response_model=schemas.Task)
def todo_create_endpoint(
    data: schemas.CreateTask,
    create_todo: CreateTaskHandler = Depends(),
):
    return create_todo(name=data.name)


def get_todo(
    id: int = Path(..., description="The ID of the todo", ge=1),
    repository: AbstractRepository = Depends(get_repository),
) -> Task:
    todo = repository.get(id)

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unable to find a todo with ID={id}",
        )

    return todo


@router.get("/{id}", response_model=schemas.Task)
def todo_endpoint(todo: Task = Depends(get_todo)):
    return todo


@router.put("/{id}/complete", response_model=schemas.Task)
def todo_complete_endpoint(
    todo: Task = Depends(get_todo),
    complete_todo: CompleteTaskHandler = Depends(),
):
    return complete_todo(todo)


@router.put("/{id}/incomplete", response_model=schemas.Task)
def todo_incomplete_endpoint(
    todo: Task = Depends(get_todo),
    incomplete_todo: IncompleteTaskHandler = Depends(),
):
    return incomplete_todo(todo)
