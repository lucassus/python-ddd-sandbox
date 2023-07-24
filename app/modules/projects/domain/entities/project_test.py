from datetime import date

import pytest

from app.modules.projects.domain.errors import MaxIncompleteTasksNumberIsReached, TaskNotFoundError
from app.modules.projects.test_utils.factories import build_project, build_task


def test_add_task():
    project = build_project(name="Test Project")
    assert len(project.tasks) == 0

    task = project.add_task(name="Testing")

    assert len(project.tasks) == 1
    assert project.tasks == [task]


def test_add_task_fails_when_allowed_number_of_incomplete_tasks_is_reached():
    project = build_project(max_incomplete_tasks_number=1)
    project.add_task(name="First")

    with pytest.raises(MaxIncompleteTasksNumberIsReached):
        project.add_task(name="Second")


def test_complete_task():
    project = build_project(name="Test Project")
    task = build_task(id=1, name="One")
    project.tasks = [task]

    task = project.complete_task(id=1, now=date(2021, 1, 17))

    assert task.completed_at is not None
    assert task.completed_at == date(2021, 1, 17)


def test_incomplete_task():
    project = build_project(name="Test Project")
    task = build_task(id=1, name="One", completed_at=date(2021, 1, 17))
    project.tasks = [task]

    task = project.incomplete_task(id=1)

    assert task.completed_at is None


def test_get_task_returns_task():
    project = build_project(name="Test Project")
    task = build_task(id=1, name="One")
    project.tasks = [task, build_task(id=2, name="Two")]

    assert project.get_task(1) == task


def test_get_task_raises_error():
    project = build_project(name="Test Project")
    task = build_task(id=1, name="One")
    project.tasks = [task, build_task(id=2, name="Two")]

    with pytest.raises(TaskNotFoundError):
        project.get_task(3)


def test_complete_tasks_completes_all_tasks():
    # Given
    tasks = [
        build_task(name="Foo", completed_at=None),
        build_task(name="Foo", completed_at=date(2020, 12, 31)),
        build_task(name="Foo", completed_at=None),
    ]
    project = build_project()
    project.tasks = tasks

    # When
    project.complete_tasks(now=date(2021, 1, 12))

    # Then
    for task in tasks:
        assert task.is_completed
