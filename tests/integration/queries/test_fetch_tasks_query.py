from sqlalchemy.orm import Session

from app.command.projects.infrastructure.queries.task_queries import FetchTasksQuery


def test_fetch_tasks(session: Session, create_project):
    # Given
    fetch_tasks = FetchTasksQuery(connection=session.connection())

    project = create_project()
    project.add_task(name="Task One")
    project.add_task(name="Task Two")
    session.commit()

    # When
    tasks = fetch_tasks(project_id=project.id)

    # Then
    assert len(tasks) == 2
    assert tasks[0].name == "Task One"
    assert tasks[0].number == 1
    assert tasks[1].name == "Task Two"
    assert tasks[1].number == 2
