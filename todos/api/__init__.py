from fastapi import APIRouter

from todos.api.endpoints import health, todos

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(todos.router, prefix="/todos", tags=["todos"])
