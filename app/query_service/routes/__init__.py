from fastapi import APIRouter

from app.query_service.routes import health, project_tasks, projects, users

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(
    project_tasks.router,
    prefix="/projects/{project_id}/tasks",
    tags=["tasks"],
)
