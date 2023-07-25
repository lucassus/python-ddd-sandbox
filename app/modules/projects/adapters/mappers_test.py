from app.modules.projects.domain.entities import Project, Task


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
    assert task
