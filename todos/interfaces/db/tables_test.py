import pytest

from todos.domain.models import Project, Task


@pytest.mark.integration
def test_tables(session):
    project = Project(name="Work")
    session.add(project)
    session.commit()

    assert len(session.query(Project).get(1).tasks) == 0

    project.tasks.extend(
        [
            Task(name="Learn python"),
            Task(name="Learn DSS"),
            Task(name="Clean the house"),
        ]
    )
    session.commit()

    assert len(session.query(Project).get(1).tasks) == 3

    task: Task = session.query(Task).get(1)
    assert task.project == project
    assert task.project.name == "Work"

    session.add(Task(name="Task without project"))
    session.commit()

    task: Task = session.query(Task).get(4)
    assert task
    assert task.name == "Task without project"
    assert task.project is None
