from typing import List

from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import JSONResponse

from todos.domain.models.todo import Todo
from todos.entrypoints.api import schemas
from todos.entrypoints.api.dependencies import (
    CompleteTodoHandler,
    CreateTodoHandler,
    IncompleteTodoHandler,
    get_repository,
)
from todos.interfaces.abstract_repository import AbstractRepository
from todos.service_layer.errors import TodoNotFoundError

router = APIRouter()


@router.get("", response_model=List[schemas.Todo])
def todos_endpoint(
    repository: AbstractRepository = Depends(get_repository),
):
    return repository.list()


@router.post("", response_model=schemas.Todo)
def todo_create_endpoint(
    data: schemas.CreateTodo,
    create_todo: CreateTodoHandler = Depends(),
):
    return create_todo(name=data.name)


def get_todo(
    id: int = Path(..., description="The ID of the todo to get", ge=1),
    repository: AbstractRepository = Depends(get_repository),
) -> Todo:
    # TODO: Raise 404 error here
    return repository.get(id)


@router.get(
    "/{id}",
    response_model=schemas.Todo,
)
def todo_endpoint(todo: Todo = Depends(get_todo)):
    if todo is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)

    return todo


@router.put("/{id}/complete", response_model=schemas.Todo)
def todo_complete_endpoint(
    id: int,
    complete_todo: CompleteTodoHandler = Depends(),
):
    try:
        todo = complete_todo(id)
    except TodoNotFoundError:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)

    return todo


@router.put("/{id}/incomplete", response_model=schemas.Todo)
def todo_incomplete_endpoint(
    id: int,
    incomplete_todo: IncompleteTodoHandler = Depends(),
):
    try:
        todo = incomplete_todo(id)
    except TodoNotFoundError:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)

    return todo
