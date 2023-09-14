from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from starlette.responses import RedirectResponse, Response
from starlette.status import HTTP_200_OK

from app.modules.authentication_contract import AuthenticationContract
from app.modules.projects.application.commands import (
    ArchiveProject,
    CreateProject,
    DeleteProject,
    UnarchiveProject,
    UpdateProject,
)
from app.modules.projects.application.queries import GetProject, ListProjects
from app.modules.projects.domain.project import ProjectID, ProjectName
from app.modules.projects.entrypoints import schemas
from app.modules.projects.entrypoints.dependencies import get_current_user
from app.modules.projects.infrastructure.containers import Container
from app.modules.projects.infrastructure.queries.project_query_handlers import (
    GetProjectQueryHandler,
    ListProjectsQueryHandler,
)
from app.shared.message_bus import MessageBus
from app.utc_datetime import utc_now

router = APIRouter(prefix="/projects")


@router.post("")
@inject
def project_create_endpoint(
    current_user: Annotated[AuthenticationContract.Identity, Depends(get_current_user)],
    data: schemas.CreateProject,
    bus: MessageBus = Depends(Provide[Container.bus]),
):
    project_id = bus.execute(CreateProject(current_user.id, ProjectName(data.name)))

    return RedirectResponse(
        f"/api/projects/{project_id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get(
    "",
    response_model=ListProjects.Result,
    name="Returns the list of projects",
)
@inject
async def list_projects_endpoint(
    current_user: Annotated[AuthenticationContract.Identity, Depends(get_current_user)],
    handle: ListProjectsQueryHandler = Depends(Provide[Container.queries.list_projects_handler]),
):
    return await handle(ListProjects(current_user.id))


@router.get(
    "/{project_id}",
    response_model=GetProject.Result,
)
@inject
async def get_project_endpoint(
    project_id: ProjectID,
    handle: GetProjectQueryHandler = Depends(Provide[Container.queries.get_project_handler]),
):
    return await handle(GetProject(project_id))


@router.put("/{project_id}")
@inject
def update_project_endpoint(
    project_id: int,
    data: schemas.UpdateProject,
    bus: MessageBus = Depends(Provide[Container.bus]),
):
    bus.execute(UpdateProject(ProjectID(project_id), ProjectName(data.name)))

    return RedirectResponse(
        f"/api/projects/{project_id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.put("/{project_id}/archive")
@inject
def archive_project_endpoint(
    project_id: int,
    bus: MessageBus = Depends(Provide[Container.bus]),
):
    bus.execute(ArchiveProject(ProjectID(project_id), now=utc_now()))
    return Response(status_code=HTTP_200_OK)


@router.put("/{project_id}/unarchive")
@inject
def unarchive_project_endpoint(
    project_id: int,
    bus: MessageBus = Depends(Provide[Container.bus]),
):
    bus.execute(UnarchiveProject(ProjectID(project_id)))
    return Response(status_code=HTTP_200_OK)


@router.delete("/{project_id}")
@inject
def delete_project_endpoint(
    project_id: int,
    bus: MessageBus = Depends(Provide[Container.bus]),
):
    bus.execute(DeleteProject(ProjectID(project_id), now=utc_now()))
    return Response(status_code=HTTP_200_OK)
