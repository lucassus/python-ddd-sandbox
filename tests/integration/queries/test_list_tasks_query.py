from typing import assert_type

from sqlalchemy.orm import Session

from app.infrastructure.db import engine
from app.modules.projects.application.queries import ListTasks
from app.modules.projects.infrastructure.queries.task_query_handlers import ListTasksQueryHandler


def test_list_tasks_query(session: Session, create_project):
    # Given
    handle = ListTasksQueryHandler(engine=engine)

    project = create_project()
    project.add_task(name="Task One")
    project.add_task(name="Task Two")
    session.commit()

    # When
    result = handle(ListTasks(project_id=project.id))
    assert_type(result, ListTasks.Result)
    tasks = result.tasks

    # Then
    assert len(tasks) == 2
    assert tasks[0].name == "Task One"
    assert tasks[0].number == 1
    assert tasks[1].name == "Task Two"
    assert tasks[1].number == 2
