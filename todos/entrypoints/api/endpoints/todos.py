from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status

from todos.domain.models.todo import Todo
from todos.entrypoints.api import schemas
from todos.entrypoints.api.dependencies import (
    CompleteTodoHandler,
    CreateTodoHandler,
    IncompleteTodoHandler,
    get_repository,
)
from todos.interfaces.abstract_repository import AbstractRepository

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
    todo = repository.get(id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unable to find a todo with ID={id}",
        )

    return todo


@router.get("/{id}", response_model=schemas.Todo)
def todo_endpoint(todo: Todo = Depends(get_todo)):
    return todo


@router.put("/{id}/complete", response_model=schemas.Todo)
def todo_complete_endpoint(
    todo: Todo = Depends(get_todo),
    complete_todo: CompleteTodoHandler = Depends(),
):
    return complete_todo(todo)


@router.put("/{id}/incomplete", response_model=schemas.Todo)
def todo_incomplete_endpoint(
    todo: Todo = Depends(get_todo),
    incomplete_todo: IncompleteTodoHandler = Depends(),
):
    return incomplete_todo(todo)
