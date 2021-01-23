from datetime import date, datetime

from fastapi import Depends, HTTPException, status

from todos.adapters.sqlalchemy.session import get_session
from todos.adapters.sqlalchemy.unit_of_work import UnitOfWork
from todos.domain.service import Service
from todos.queries.databases import database


def get_current_time() -> date:
    return datetime.utcnow()


# TODO: Bring back the old idea with true context manager
def get_uow():
    return UnitOfWork(session_factory=get_session)


# TODO: Rename this dependency
async def get_project(project_id: int) -> None:
    pass
    # TODO: Create a dependency for database?
    project = await database.fetch_one(
        "SELECT id FROM projects WHERE id = :id",
        values={"id": project_id},
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unable to find a project with ID={project_id}",
        )


def get_service(
    project_id: int,
    uow=Depends(get_uow),
) -> Service:
    return Service(project_id=project_id, uow=uow)
