from datetime import date, datetime

from fastapi import Depends, HTTPException, status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from todos.commands.adapters.unit_of_work import UnitOfWork
from todos.commands.domain.service import Service
from todos.infrastructure.database import database
from todos.infrastructure.session import session_factory


def get_current_time() -> date:
    return datetime.utcnow()


# TODO: Bring back the old idea with true context manager
def get_uow():
    return UnitOfWork(session_factory=session_factory)


# TODO: Rename this dependency
async def get_project(project_id: int) -> None:
    pass
    # TODO: Do not use database here, since it belongs to queries app
    project = await database.fetch_one(
        "SELECT id FROM projects WHERE id = :id",
        values={"id": project_id},
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unable to find a project with ID={project_id}",
        )


def get_service(uow=Depends(get_uow)) -> Service:
    return Service(uow=uow)


class SeeOtherRedirect:
    def __init__(self, request: Request):
        self._request = request

    def __call__(self, name: str, **path_params):
        url = self._request.url_for(name, **path_params)
        return RedirectResponse(url, status_code=status.HTTP_303_SEE_OTHER)
