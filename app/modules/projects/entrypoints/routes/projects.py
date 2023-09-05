from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from starlette.responses import RedirectResponse, Response
from starlette.status import HTTP_200_OK

from app.modules.authentication_contract import AuthenticationContract
from app.modules.projects.application.commands.archive_project import ArchiveProject
from app.modules.projects.application.commands.create_project import CreateProject
from app.modules.projects.application.commands.delete_project import DeleteProject
from app.modules.projects.application.commands.unarchive_project import UnarchiveProject
from app.modules.projects.application.commands.update_project import UpdateProject
from app.modules.projects.domain.project import ProjectID, ProjectName
from app.modules.projects.entrypoints import schemas
from app.modules.projects.entrypoints.containers import Container
from app.modules.projects.entrypoints.dependencies import get_current_user
from app.modules.projects.queries.project_queries import GetProjectQuery, ListProjectsQuery
from app.modules.shared_kernel.message_bus import MessageBus
from app.utc_datetime import utc_now

router = APIRouter(prefix="/projects")


@router.post("")
@inject
def project_create_endpoint(
    current_user: Annotated[AuthenticationContract.CurrentUserDTO, Depends(get_current_user)],
    data: schemas.CreateProject,
    bus: MessageBus = Depends(Provide[Container.bus]),
):
    project_id = bus.execute(
        CreateProject(
            user_id=current_user.id,
            name=ProjectName(data.name),
        ),
    )

    return RedirectResponse(
        f"/api/projects/{project_id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get(
    "",
    response_model=ListProjectsQuery.Result,
    name="Returns the list of projects",
)
@inject
def list_projects_endpoint(
    current_user: Annotated[AuthenticationContract.CurrentUserDTO, Depends(get_current_user)],
    list_projects: ListProjectsQuery = Depends(Provide[Container.queries.list_projects]),
):
    return list_projects(current_user.id)


@router.get(
    "/{project_id}",
    response_model=GetProjectQuery.Result,
)
@inject
def get_project_endpoint(
    project_id: ProjectID,
    get_project: GetProjectQuery = Depends(Provide[Container.queries.get_project]),
):
    return get_project(project_id)


@router.put("/{project_id}")
@inject
def update_project_endpoint(
    project_id: int,
    data: schemas.UpdateProject,
    bus: MessageBus = Depends(Provide[Container.bus]),
):
    bus.execute(
        UpdateProject(
            project_id=ProjectID(project_id),
            name=ProjectName(data.name),
        ),
    )

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
    bus.execute(
        ArchiveProject(
            project_id=ProjectID(project_id),
            now=utc_now(),
        )
    )

    return Response(status_code=HTTP_200_OK)


@router.put("/{project_id}/unarchive")
@inject
def unarchive_project_endpoint(
    project_id: int,
    bus: MessageBus = Depends(Provide[Container.bus]),
):
    bus.execute(UnarchiveProject(project_id=ProjectID(project_id)))
    return Response(status_code=HTTP_200_OK)


@router.delete("/{project_id}")
@inject
def delete_project_endpoint(
    project_id: int,
    bus: MessageBus = Depends(Provide[Container.bus]),
):
    bus.execute(DeleteProject(project_id=ProjectID(project_id), now=utc_now()))
    return Response(status_code=HTTP_200_OK)
