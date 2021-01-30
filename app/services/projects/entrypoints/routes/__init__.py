from fastapi import APIRouter

from app.services.projects.entrypoints.routes import project_tasks

api_router = APIRouter()

api_router.include_router(
    project_tasks.router, prefix="/projects/{project_id}/tasks", tags=["tasks"]
)
