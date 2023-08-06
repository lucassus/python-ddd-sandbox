from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from starlette.responses import RedirectResponse, Response
from starlette.status import HTTP_200_OK

from app.command.projects.application.archivization_service import ArchivizationService
from app.command.projects.application.create_project import CreateProject
from app.command.projects.application.update_project import UpdateProject
from app.command.projects.entities.project import ProjectID, ProjectName
from app.command.projects.entrypoints import schemas
from app.command.projects.entrypoints.containers import Container
from app.command.shared_kernel.entities.user_id import UserID

router = APIRouter(prefix="/projects")


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
        f"/queries/projects/{project_id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.put("/{project_id}")
@inject
def update_project_endpoint(
    project_id: int,
    data: schemas.UpdateProject,
    update_project: UpdateProject = Depends(Provide[Container.update_project]),
):
    update_project(ProjectID(project_id), ProjectName(data.name))

    return RedirectResponse(
        f"/queries/projects/{project_id}",
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
