import pytest
from sqlalchemy.orm import Session

from app.infrastructure.db import engine
from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.task import TaskNumber
from app.modules.projects.queries.task_queries import GetTaskQuery


def test_get_task_query(
    session: Session,
    create_user,
    create_project,
):
    # Given
    list_tasks = GetTaskQuery(engine=engine)

    user = create_user()

    project = create_project(user=user)
    project.add_task(name="Task One")
    session.commit()

    second_project = create_project(user=user)
    second_project.add_task(name="Task Two")
    second_project.add_task(name="Task Three")
    session.commit()

    # When
    task = list_tasks(project_id=second_project.id, number=TaskNumber(1))

    # Then
    assert task.name == "Task Two"
    assert task.number == TaskNumber(1)


def test_get_taskq_query_raises_error():
    # Given
    list_tasks = GetTaskQuery(engine=engine)

    # When
    with pytest.raises(GetTaskQuery.NotFoundError):
        list_tasks(project_id=ProjectID(1), number=TaskNumber(1))
