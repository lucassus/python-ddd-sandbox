from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import RedirectResponse, Response
from starlette.status import HTTP_200_OK

from app.modules.authentication_contract import AuthenticationContract
from app.modules.projects.application.archivization_service import ArchivizationService
from app.modules.projects.application.create_project import CreateProject
from app.modules.projects.application.queries.project_queries import GetProjectQuery, ListProjectsQuery
from app.modules.projects.application.update_project import UpdateProject
from app.modules.projects.domain.project import ProjectID, ProjectName
from app.modules.projects.entrypoints import schemas
from app.modules.projects.entrypoints.containers import Container
from app.modules.projects.entrypoints.dependencies import get_current_user

router = APIRouter(prefix="/projects")


@router.post("")
@inject
def project_create_endpoint(
    current_user: Annotated[AuthenticationContract.CurrentUserDTO, Depends(get_current_user)],
    data: schemas.CreateProject,
    create_project: CreateProject = Depends(Provide[Container.create_project]),
):
    project_id = create_project(
        user_id=current_user.id,
        name=ProjectName(data.name),
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
    list_projects: ListProjectsQuery = Depends(Provide[Container.list_projects_query]),
):
    return list_projects(current_user.id)


@router.get(
    "/{project_id}",
    response_model=GetProjectQuery.Result,
)
@inject
def get_project_endpoint(
    project_id: ProjectID,
    get_project: GetProjectQuery = Depends(Provide[Container.get_project_query]),
):
    try:
        return get_project(project_id)
    except GetProjectQuery.NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.put("/{project_id}")
@inject
def update_project_endpoint(
    project_id: int,
    data: schemas.UpdateProject,
    update_project: UpdateProject = Depends(Provide[Container.update_project]),
):
    update_project(ProjectID(project_id), ProjectName(data.name))

    return RedirectResponse(
        f"/api/projects/{project_id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.put("/{project_id}/archive")
@inject
def archive_project_endpoint(
    project_id: int,
    archivization_service: ArchivizationService = Depends(Provide[Container.archivization_service]),
):
    archivization_service.archive(ProjectID(project_id))
    return Response(status_code=HTTP_200_OK)


@router.put("/{project_id}/unarchive")
@inject
def unarchive_project_endpoint(
    project_id: int,
    archivization_service: ArchivizationService = Depends(Provide[Container.archivization_service]),
):
    archivization_service.unarchive(ProjectID(project_id))
    return Response(status_code=HTTP_200_OK)


@router.delete("/{project_id}")
@inject
def delete_project_endpoint(
    project_id: int,
    archivization_service: ArchivizationService = Depends(Provide[Container.archivization_service]),
):
    archivization_service.delete(ProjectID(project_id))
    return Response(status_code=HTTP_200_OK)
