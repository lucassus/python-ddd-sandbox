from datetime import date

import pytest

from app.command.projects.entities.errors import (
    ArchiveProjectError,
    MaxIncompleteTasksNumberIsReached,
    TaskNotFoundError,
)
from app.command.projects.entities.factories import build_project
from app.command.projects.entities.project import ProjectID
from app.command.projects.entities.task import TaskNumber


def test_add_task():
    project = build_project(name="Test Project")
    assert len(project.tasks) == 0

    task = project.add_task(name="First")

    assert task.number == TaskNumber(1)
    assert task.name == "First"
    assert len(project.tasks) == 1
    assert project.tasks == [task]

    second = project.add_task(name="Second")

    assert second.number == TaskNumber(2)
    assert second.name == "Second"
    assert len(project.tasks) == 2


def test_add_task_fails_when_allowed_number_of_incomplete_tasks_is_reached():
    project = build_project(name="Test Project", maximum_number_of_incomplete_tasks=1)
    project.add_task(name="First")

    with pytest.raises(MaxIncompleteTasksNumberIsReached):
        project.add_task(name="Second")


def test_complete_task():
    project = build_project(name="Test Project")
    task = project.add_task(name="One")

    task = project.complete_task(number=task.number, now=date(2021, 1, 17))

    assert task.completed_at is not None
    assert task.completed_at == date(2021, 1, 17)


def test_complete_task_raises_error_when_task_not_found():
    project = build_project(name="Test Project")

    with pytest.raises(
        TaskNotFoundError,
        match="Unable to find Task with number=1",
    ):
        project.complete_task(number=TaskNumber(1), now=date(2021, 1, 17))


def test_incomplete_task():
    project = build_project(name="Test Project")
    task = project.add_task(name="One")
    project.complete_task(task.number, now=date(2021, 1, 17))

    task = project.incomplete_task(number=task.number)

    assert task.completed_at is None


def test_incomplete_task_raises_error_when_task_not_found():
    project = build_project(name="Test Project")

    with pytest.raises(
        TaskNotFoundError,
        match="Unable to find Task with number=1",
    ):
        project.incomplete_task(number=TaskNumber(1))


def test_complete_all_tasks():
    # Given
    project = build_project(name="Test Project")
    project.add_task(name="Foo")
    task = project.add_task(name="Foo")
    project.complete_task(task.number, now=date(2020, 12, 31))
    project.add_task(name="Foo")

    # When
    project.complete_all_tasks(now=date(2021, 1, 12))

    # Then
    for task in project.tasks:
        assert task.is_completed


def test_incomplete_tasks_count():
    project = build_project(name="Test Project")
    assert project.incomplete_tasks_count == 0

    project.add_task(name="Foo")
    task = project.add_task(name="Foo")
    project.complete_task(task.number, now=date(2020, 12, 31))
    project.add_task(name="Foo")
    assert project.incomplete_tasks_count == 2


def test_archive_project_raises_error_when_not_all_tasks_are_completed():
    # Given
    project = build_project(name="Test Project")
    project.id = ProjectID(1)
    project.add_task(name="Foo")

    # When
    with pytest.raises(
        ArchiveProjectError,
        match="Unable to archive project id=1, because it has 1 incomplete tasks",
    ):
        project.archive(now=date(2021, 1, 12))


def test_archive_project_set_archived_at():
    # Given
    project = build_project(name="Test Project")
    task = project.add_task(name="Foo")
    project.complete_task(task.number, now=date(2020, 12, 31))

    now = date(2021, 1, 12)

    # When
    project.archive(now=now)

    # Then
    assert project.archived_at == now
    assert project.archived is True


def test_unarchive_project():
    # Given
    project = build_project(name="Test Project")
    task = project.add_task(name="Foo")
    project.complete_task(task.number, now=date(2020, 12, 31))
    project.archive(now=date(2021, 1, 12))

    # When
    project.unarchive()

    # Then
    assert project.archived_at is None
    assert project.archived is False
