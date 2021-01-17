from todos.domain.models import Project


def test_add_task():
    project = Project(name="Test Project")
    assert len(project.tasks) == 0

    task = project.add_task(name="Testing")

    assert len(project.tasks) == 1
    assert project.tasks == [task]
