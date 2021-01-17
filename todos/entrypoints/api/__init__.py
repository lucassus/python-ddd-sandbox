from fastapi import APIRouter

from todos.entrypoints.api.endpoints import health, tasks, projects

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
