from fastapi import APIRouter, Depends

from app.modules.projects.entrypoints.dependencies import get_current_user
from app.modules.projects.entrypoints.routes import project_tasks, projects

router = APIRouter(
    dependencies=[Depends(get_current_user)],
)

router.include_router(projects.router, tags=["projects"])
router.include_router(project_tasks.router, tags=["tasks"])
