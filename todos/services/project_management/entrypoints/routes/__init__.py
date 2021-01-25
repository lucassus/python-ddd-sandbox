from fastapi import APIRouter

from todos.services.project_management.entrypoints.routes import project_tasks

api_router = APIRouter()

api_router.include_router(
    project_tasks.router, prefix="/projects/{project_id}/tasks", tags=["tasks"]
)
