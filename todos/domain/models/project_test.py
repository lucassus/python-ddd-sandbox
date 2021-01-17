from datetime import date

import pytest

from todos.domain.errors import TaskNotFoundError
from todos.test_utils.factories import build_project, build_task


def test_add_task():
    project = build_project(name="Test Project")
    assert len(project.tasks) == 0

    task = project.add_task(name="Testing")

    assert len(project.tasks) == 1
    assert project.tasks == [task]


def test_complete_task():
    project = build_project(name="Test Project")
    task = build_task(id=1, name="One")
    project.tasks = [task]

    task = project.complete_task(id=1, now=lambda: date(2021, 1, 17))

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