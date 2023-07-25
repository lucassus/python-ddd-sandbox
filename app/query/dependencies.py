from typing import Annotated

from fastapi import Depends

from app.query.errors import EntityNotFoundError
from app.query.queries.projects import FindProjectQuery


def get_project(
    project_id: int,
    find_project: Annotated[FindProjectQuery, Depends()],
):
    project = find_project(id=project_id)

    if project is None:
        raise EntityNotFoundError(detail=f"Unable to find a project with ID={project_id}")

    return project
