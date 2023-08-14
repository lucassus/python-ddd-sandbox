from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from app.modules.projects.application.queries.project_queries import GetProjectQuery
from app.modules.projects.domain.project import ProjectID
from app.modules.projects.entrypoints.containers import Container
from app.modules.projects.entrypoints.errors import EntityNotFoundError


# TODO: Drop it?
@inject
def get_project(
    project_id: int,
    get_project: GetProjectQuery = Depends(Provide[Container.get_project_query]),
):
    project = get_project(id=ProjectID(project_id))

    # TODO: Move this error to the query
    if project is None:
        raise EntityNotFoundError(detail=f"Unable to find a project with ID={project_id}")

    return project
