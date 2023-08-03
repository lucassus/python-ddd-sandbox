from typing import Annotated

from fastapi import APIRouter, Depends, status
from starlette.responses import RedirectResponse

from app.command.projects.application.create_project import CreateProject
from app.command.projects.entrypoints import schemas
from app.command.projects.entrypoints.dependencies import get_create_project
from app.command.shared_kernel.user_id import UserID

router = APIRouter(prefix="/projects")


@router.post("")
def project_create_endpoint(
    data: schemas.CreateProject,
    create_project: Annotated[CreateProject, Depends(get_create_project)],
):
    project_id = create_project(
        user_id=UserID(data.user_id),
        name=data.name,
    )

    return RedirectResponse(
        f"/queries/projects/{project_id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
