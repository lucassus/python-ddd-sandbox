from fastapi import APIRouter, Depends

from app.modules.projects.entrypoints.routes import project_tasks, projects
from app.shared.dependencies import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

router.include_router(projects.router, tags=["projects"])
router.include_router(project_tasks.router, tags=["tasks"])
