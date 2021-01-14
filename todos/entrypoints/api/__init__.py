from fastapi import APIRouter

from todos.entrypoints.api.endpoints import health, tasks

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
