from datetime import datetime
from typing import Optional

from app.modules.projects.domain.entities import Project
from app.shared_kernel.user_id import UserID


def build_project(
    name: str,
    user_id: Optional[UserID] = None,
    maximum_number_of_incomplete_tasks: Optional[int] = None,
) -> Project:
    project = Project(name=name)

    if user_id is not None:
        project.user_id = user_id

    if maximum_number_of_incomplete_tasks is not None:
        project.maximum_number_of_incomplete_tasks = maximum_number_of_incomplete_tasks

    return project


def build_example_project(
    user_id: UserID,
    completed_at: Optional[datetime] = None,
) -> Project:
    if completed_at is None:
        completed_at = datetime.utcnow()  # TODO: Do not use naive dates

    project = build_project(user_id=user_id, name="My first project")

    task = project.add_task(name="Sign up!")
    task.complete(completed_at)

    project.add_task(name="Watch the tutorial")
    project.add_task(name="Start using our awesome app")

    return project