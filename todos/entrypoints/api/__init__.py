from fastapi import APIRouter

# TODO: Rename endpoints to routes
from todos.entrypoints.api.endpoints import health, projects, tasks

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(
    tasks.router, prefix="/projects/{project_id}/tasks", tags=["tasks"]
)
