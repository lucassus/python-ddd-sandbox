from typing import assert_type

import pytest
from sqlalchemy.orm import Session

from app.infrastructure.db import async_engine
from app.modules.projects.application.queries import ListTasks
from app.modules.projects.infrastructure.queries.task_query_handlers import ListTasksQueryHandler


@pytest.mark.asyncio()
async def test_list_tasks_query(session: Session, create_project):
    # Given
    handle = ListTasksQueryHandler(engine=async_engine)

    project = create_project()
    project.add_task(name="Task One")
    project.add_task(name="Task Two")
    session.commit()

    # When
    result = await handle(ListTasks(project_id=project.id))
    assert_type(result, ListTasks.Result)
    tasks = result.tasks

    # Then
    assert len(tasks) == 2
    assert tasks[0].name == "Task One"
    assert tasks[0].number == 1
    assert tasks[1].name == "Task Two"
    assert tasks[1].number == 2
