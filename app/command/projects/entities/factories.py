from datetime import datetime
from typing import Optional

from app.command.projects.entities.project import Project
from app.command.shared_kernel.entities.user_id import UserID


def build_example_project(
    user_id: UserID,
    completed_at: Optional[datetime] = None,
) -> Project:
    if completed_at is None:
        completed_at = datetime.utcnow()

    project = Project(user_id=user_id, name="My first project")

    task = project.add_task(name="Sign up!")
    task.complete(completed_at)

    project.add_task(name="Watch the tutorial")
    project.add_task(name="Start using our awesome app")

    return project
