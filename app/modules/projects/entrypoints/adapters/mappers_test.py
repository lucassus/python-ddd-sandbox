from sqlalchemy.orm import Session

from app.infrastructure.factories import create_project
from app.modules.projects.entities.project import Project
from app.modules.projects.entities.task import Task, TaskNumber


def test_tables(session: Session):
    project_id = create_project(session.connection()).id
    project = session.get(Project, project_id)
    assert project is not None

    assert len(project.tasks) == 0

    project.add_task(name="Learn python")
    project.add_task(name="Learn DDD")
    project.add_task(name="Clean the house")
    session.commit()

    session.refresh(project)
    assert len(project.tasks) == 3
    assert project.last_task_number == TaskNumber(3)

    task = session.get(Task, 1)
    assert task
