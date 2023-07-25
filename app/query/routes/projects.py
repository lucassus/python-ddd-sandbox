from fastapi import APIRouter, Depends

from app.query import schemas
from app.query.dependencies import get_project
from app.query.queries.projects import FetchProjectsQuery

router = APIRouter()


@router.get(
    "",
    response_model=list[schemas.Project],
    name="Returns the list of projects",
)
def projects_endpoint(fetch_projects: FetchProjectsQuery = Depends()):
    return fetch_projects()


@router.get("/{project_id}", response_model=schemas.Project)
def project_endpoint(project=Depends(get_project)):
    return project
