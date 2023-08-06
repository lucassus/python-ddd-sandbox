from fastapi import APIRouter

from app.command.projects.entrypoints.endpoints import project_tasks, projects

router = APIRouter()

router.include_router(projects.router, tags=["projects"])
router.include_router(project_tasks.router, tags=["tasks"])
