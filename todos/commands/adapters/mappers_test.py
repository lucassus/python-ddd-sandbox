import pytest

from todos.commands.domain.entities import Project, Task


@pytest.mark.integration
def test_tables(session):
    project = Project(name="Work")
    session.add(project)
    session.commit()

    assert len(session.query(Project).get(1).tasks_table) == 0

    project.tasks.extend(
        [
            Task(name="Learn python"),
            Task(name="Learn DSS"),
            Task(name="Clean the house"),
        ]
    )
    session.commit()

    assert len(session.query(Project).get(1).tasks_table) == 3

    task: Task = session.query(Task).get(1)
    assert task

    session.add(Task(name="Task without project"))
    session.commit()

    task: Task = session.query(Task).get(4)
    assert task
    assert task.name == "Task without project"
