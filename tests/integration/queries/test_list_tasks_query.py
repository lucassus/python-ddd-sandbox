from sqlalchemy.orm import Session

from app.modules.projects.infrastructure.queries.task_queries import ListTasksSQLQuery


def test_list_tasks_query(session: Session, create_project):
    # Given
    fetch_tasks = ListTasksSQLQuery(connection=session.connection())

    project = create_project()
    project.add_task(name="Task One")
    project.add_task(name="Task Two")
    session.commit()

    # When
    tasks = fetch_tasks(project_id=project.id).tasks

    # Then
    assert len(tasks) == 2
    assert tasks[0].name == "Task One"
    assert tasks[0].number == 1
    assert tasks[1].name == "Task Two"
    assert tasks[1].number == 2
