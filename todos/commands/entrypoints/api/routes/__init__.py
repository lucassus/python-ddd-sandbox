from fastapi import APIRouter, Depends

from todos.commands.entrypoints.api.dependencies import get_project
from todos.commands.entrypoints.api.routes import project_tasks

api_router = APIRouter()

api_router.include_router(
    project_tasks.router,
    prefix="/projects/{project_id}/tasks",
    tags=["tasks"],
    dependencies=[Depends(get_project)],
)
