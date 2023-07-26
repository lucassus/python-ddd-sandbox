from sqlalchemy.orm import Session

from app.infrastructure.factories import create_project
from app.modules.projects.domain.entities import Project, Task


def test_tables(session: Session):
    project_id = create_project(session.connection()).id
    project = session.get(Project, project_id)
    assert project is not None

    assert len(project.tasks) == 0

    project.tasks.extend(
        [
            Task(name="Learn python"),
            Task(name="Learn DSS"),
            Task(name="Clean the house"),
        ]
    )
    session.commit()

    assert len(project.tasks) == 3

    task = session.get(Task, 1)
    assert task
