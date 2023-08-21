from sqlalchemy.orm import Session

from app.infrastructure.db import engine
from app.modules.projects.queries.task_queries import ListTasksQuery


def test_list_tasks_query(session: Session, create_project):
    # Given
    list_tasks = ListTasksQuery(engine=engine)

    project = create_project()
    project.add_task(name="Task One")
    project.add_task(name="Task Two")
    session.commit()

    # When
    tasks = list_tasks(project_id=project.id).tasks

    # Then
    assert len(tasks) == 2
    assert tasks[0].name == "Task One"
    assert tasks[0].number == 1
    assert tasks[1].name == "Task Two"
    assert tasks[1].number == 2
