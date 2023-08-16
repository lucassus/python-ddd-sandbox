import pytest
from sqlalchemy import Connection
from sqlalchemy.orm import Session

from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.task import TaskNumber
from app.modules.projects.infrastructure.queries.task_queries import GetTaskSQLQuery


def test_get_task_query(
    connection: Connection,
    session: Session,
    create_user,
    create_project,
):
    # Given
    list_tasks = GetTaskSQLQuery(connection=connection)

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


def test_get_taskq_query_raises_error(connection: Connection):
    # Given
    list_tasks = GetTaskSQLQuery(connection=connection)

    # When
    with pytest.raises(GetTaskSQLQuery.NotFoundError):
        list_tasks(project_id=ProjectID(1), number=TaskNumber(1))
