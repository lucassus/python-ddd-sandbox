from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from todos.api import schemas
from todos.api.dependencies import get_session
from todos.db.repositories import Repository
from todos.domain.services import Service

# TODO: Nest routes
router = APIRouter()


@router.get("/")
def helo_endpoint():
    return {"message": "Hello World"}


@router.get("/todos", response_model=List[schemas.Todo])
def todos_endpoint(session: Session = Depends(get_session)):
    repository = Repository(session=session)
    return repository.list()


@router.get(
    "/todos/{id}",
    response_model=schemas.Todo,
    responses={404: {"description": "Todo not found"}},
)
def todo_endpoint(id: int, session: Session = Depends(get_session)):
    repository = Repository(session=session)
    todo = repository.get(id)

    if todo is None:
        return JSONResponse(status_code=404)

    return todo


@router.post("/todos", response_model=schemas.Todo)
def todo_create_endpoint(
    todo: schemas.CreateTodo, session: Session = Depends(get_session)
):
    repository = Repository(session=session)
    return repository.create(todo.name)


@router.put("/todos/{id}/complete", response_model=schemas.Todo)
def todo_complete_endpoint(id: int, session: Session = Depends(get_session)):
    service = Service(repository=Repository(session))
    return service.complete(id)


@router.put("/todos/{id}/incomplete", response_model=schemas.Todo)
def todo_incomplete_endpoint(id: int, session: Session = Depends(get_session)):
    service = Service(repository=Repository(session))
    return service.incomplete(id)
