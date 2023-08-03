from typing import Annotated

from fastapi import APIRouter, Depends, status
from starlette.responses import RedirectResponse, Response
from starlette.status import HTTP_200_OK

from app.command.projects.application.archivization_service import ArchivizationService
from app.command.projects.application.create_project import CreateProject
from app.command.projects.entities.project import ProjectID
from app.command.projects.entrypoints import schemas
from app.command.projects.entrypoints.dependencies import get_archivization_service, get_create_project
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


@router.put("/{project_id}/archive")
def archive_project_endpoint(
    project_id: int,
    archivization_service: Annotated[ArchivizationService, Depends(get_archivization_service)],
):
    archivization_service.archive(ProjectID(project_id))
    return Response(status_code=HTTP_200_OK)


@router.put("/{project_id}/unarchive")
def unarchive_project_endpoint(
    project_id: int,
    archivization_service: Annotated[ArchivizationService, Depends(get_archivization_service)],
):
    archivization_service.unarchive(ProjectID(project_id))
    return Response(status_code=HTTP_200_OK)


@router.delete("/{project_id}")
def delete_project_endpoint(
    project_id: int,
    archivization_service: Annotated[ArchivizationService, Depends(get_archivization_service)],
):
    archivization_service.delete(ProjectID(project_id))
    return Response(status_code=HTTP_200_OK)
