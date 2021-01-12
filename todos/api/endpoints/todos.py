from typing import List

from fastapi import APIRouter, Depends, Path
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from todos.api import schemas
from todos.api.dependencies import CreateTodoService, get_repository, get_session
from todos.interfaces.abstract_repository import AbstractRepository
from todos.service_layer.errors import TodoNotFoundError
from todos.service_layer.services import complete_todo, incomplete_todo

router = APIRouter()


@router.get("", response_model=List[schemas.Todo])
def todos_endpoint(
    repository: AbstractRepository = Depends(get_repository),
):
    return repository.list()


@router.post("", response_model=schemas.Todo)
def todo_create_endpoint(
    data: schemas.CreateTodo,
    create_todo: CreateTodoService = Depends(),
):
    return create_todo(name=data.name)


@router.get(
    "/{id}",
    response_model=schemas.Todo,
    responses={404: {"description": "Todo not found"}},
)
def todo_endpoint(
    id: int = Path(..., description="The ID of the todo to get", ge=1),
    repository: AbstractRepository = Depends(get_repository),
):
    todo = repository.get(id)

    if todo is None:
        return JSONResponse(status_code=404)

    return todo


@router.put("/{id}/complete", response_model=schemas.Todo)
def todo_complete_endpoint(
    id: int,
    repository: AbstractRepository = Depends(get_repository),
    session: Session = Depends(get_session),
):
    try:
        todo = complete_todo(id, repository=repository, session=session)
    except TodoNotFoundError:
        return JSONResponse(status_code=404)

    return todo


@router.put("/{id}/incomplete", response_model=schemas.Todo)
def todo_incomplete_endpoint(
    id: int,
    repository: AbstractRepository = Depends(get_repository),
    session: Session = Depends(get_session),
):
    try:
        todo = incomplete_todo(id, repository=repository, session=session)
    except TodoNotFoundError:
        return JSONResponse(status_code=404)

    return todo
