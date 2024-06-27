import pytest
from sqlalchemy.orm import Session

from app.infrastructure.db import async_engine
from app.modules.projects.application.queries import GetTask
from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.task import TaskNumber
from app.modules.projects.infrastructure.queries.task_query_handlers import GetTaskQueryHandler


@pytest.mark.asyncio
async def test_get_task_query(
    session: Session,
    create_user,
    create_project,
):
    # Given
    handle = GetTaskQueryHandler(engine=async_engine)

    user = create_user()

    project = create_project(user=user)
    project.add_task(name="Task One")
    session.commit()

    second_project = create_project(user=user)
    second_project.add_task(name="Task Two")
    second_project.add_task(name="Task Three")
    session.commit()

    # When
    task = await handle(GetTask(project_id=second_project.id, number=TaskNumber(1)))

    # Then
    assert task.name == "Task Two"
    assert task.number == TaskNumber(1)


@pytest.mark.asyncio
async def test_get_task_query_raises_error():
    # Given
    handle = GetTaskQueryHandler(engine=async_engine)

    # When
    with pytest.raises(GetTask.NotFoundError):
        await handle(GetTask(project_id=ProjectID(1), number=TaskNumber(1)))
