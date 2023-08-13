from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from starlette.responses import RedirectResponse, Response
from starlette.status import HTTP_200_OK

from app.modules.projects.application.archivization_service import ArchivizationService
from app.modules.projects.application.create_project import CreateProject
from app.modules.projects.application.queries.project_queries import GetProjectQuery, ListProjectsQuery
from app.modules.projects.application.update_project import UpdateProject
from app.modules.projects.domain.project import ProjectID, ProjectName
from app.modules.projects.entrypoints import schemas
from app.modules.projects.entrypoints.containers import Container
from app.modules.projects.entrypoints.errors import EntityNotFoundError
from app.modules.shared_kernel.entities.user_id import UserID

router = APIRouter(prefix="/projects")


# TODO: Drop it
@inject
def get_project(
    project_id: int,
    get_project: GetProjectQuery = Depends(Provide[Container.get_project_query]),
):
    project = get_project(id=ProjectID(project_id))

    if project is None:
        raise EntityNotFoundError(detail=f"Unable to find a project with ID={project_id}")

    return project


@router.post("")
@inject
def project_create_endpoint(
    data: schemas.CreateProject,
    create_project: CreateProject = Depends(Provide[Container.create_project]),
):
    project_id = create_project(
        user_id=UserID(data.user_id),
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
    list_projects: ListProjectsQuery = Depends(Provide[Container.list_projects_query]),
):
    return list_projects()


@router.get(
    "/{project_id}",
    response_model=GetProjectQuery.Result,
)
@inject
def project_endpoint(project=Depends(get_project)):
    return project


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
    project_id: int, archivization_service: ArchivizationService = Depends(Provide[Container.archivization_service])
):
    archivization_service.unarchive(ProjectID(project_id))
    return Response(status_code=HTTP_200_OK)


@router.delete("/{project_id}")
@inject
def delete_project_endpoint(
    project_id: int, archivization_service: ArchivizationService = Depends(Provide[Container.archivization_service])
):
    archivization_service.delete(ProjectID(project_id))
    return Response(status_code=HTTP_200_OK)
