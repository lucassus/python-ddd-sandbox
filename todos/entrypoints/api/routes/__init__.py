from fastapi import APIRouter, Depends

from todos.entrypoints.api.dependencies import get_project
from todos.entrypoints.api.routes import health, project_tasks, projects

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(
    project_tasks.router,
    prefix="/projects/{project_id}/tasks",
    tags=["tasks"],
    dependencies=[Depends(get_project)],
)
