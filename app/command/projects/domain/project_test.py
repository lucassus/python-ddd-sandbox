import pytest

from app.command.projects.domain.errors import (
    MaxIncompleteTasksNumberIsReachedError,
    ProjectIsNotCompletedError,
    ProjectNotArchivedError,
    TaskNotFoundError,
)
from app.command.projects.domain.project import ProjectName
from app.command.projects.domain.project_builder import ProjectBuilder
from app.command.projects.domain.task import TaskNumber
from app.utc_datetime import utc_datetime


def test_set_name():
    project = ProjectBuilder().build()
    project.name = ProjectName("New name")
    assert project.name == ProjectName("New name")


def test_add_task():
    project = ProjectBuilder().build()
    assert len(project.tasks) == 0

    task = project.add_task(name="First")

    assert task.number == TaskNumber(1)
    assert task.name == "First"
    assert len(project.tasks) == 1
    assert project.tasks == (task,)

    second_task = project.add_task(name="Second")

    assert second_task.number == TaskNumber(2)
    assert second_task.name == "Second"
    assert len(project.tasks) == 2
    assert project.tasks == (task, second_task)


def test_add_task_fails_when_allowed_number_of_incomplete_tasks_is_reached():
    project = ProjectBuilder().with_maximum_number_of_incomplete_tasks(1).build()
    project.add_task(name="First")

    with pytest.raises(MaxIncompleteTasksNumberIsReachedError):
        project.add_task(name="Second")


def test_complete_task():
    project = ProjectBuilder().build()
    task = project.add_task(name="One")

    task = project.complete_task(number=task.number, now=utc_datetime(2021, 1, 17))

    assert task.completed_at is not None
    assert task.completed_at == utc_datetime(2021, 1, 17)


def test_complete_task_raises_error_when_task_not_found():
    project = ProjectBuilder().build()

    with pytest.raises(
        TaskNotFoundError,
        match="Unable to find Task with number=1",
    ):
        project.complete_task(number=TaskNumber(1), now=utc_datetime(2021, 1, 17))


def test_incomplete_task():
    project = ProjectBuilder().build()
    task = project.add_task(name="One")
    project.complete_task(task.number, now=utc_datetime(2021, 1, 17))

    task = project.incomplete_task(number=task.number)

    assert task.completed_at is None


def test_incomplete_task_raises_error_when_task_not_found():
    project = ProjectBuilder().build()

    with pytest.raises(
        TaskNotFoundError,
        match="Unable to find Task with number=1",
    ):
        project.incomplete_task(number=TaskNumber(1))


def test_complete_all_tasks():
    # Given
    project = ProjectBuilder().build()
    project.add_task(name="Foo")
    task = project.add_task(name="Foo")
    project.complete_task(task.number, now=utc_datetime(2020, 12, 31))
    project.add_task(name="Foo")

    # When
    project.complete_all_tasks(now=utc_datetime(2021, 1, 12))

    # Then
    for task in project.tasks:
        assert task.is_completed


def test_incomplete_tasks_count():
    project = ProjectBuilder().build()
    assert project.incomplete_tasks_count == 0

    project.add_task(name="Foo")
    task = project.add_task(name="Foo")
    project.complete_task(task.number, now=utc_datetime(2020, 12, 31))
    project.add_task(name="Foo")
    assert project.incomplete_tasks_count == 2


def test_archive_project_raises_error_when_not_all_tasks_are_completed():
    # Given
    project = ProjectBuilder().build()
    project.add_task(name="Foo")

    # When
    with pytest.raises(
        ProjectIsNotCompletedError,
        match="Project has 1 incomplete tasks",
    ):
        project.archive(now=utc_datetime(2021, 1, 12))


def test_archive_project_set_archived_at():
    # Given
    project = ProjectBuilder().build()
    task = project.add_task(name="Foo")
    project.complete_task(task.number, now=utc_datetime(2020, 12, 31))

    now = utc_datetime(2021, 1, 12)

    # When
    project.archive(now=now)

    # Then
    assert project.archived_at == now
    assert project.archived is True


def test_unarchive_project():
    # Given
    project = ProjectBuilder().build()
    task = project.add_task(name="Foo")
    project.complete_task(task.number, now=utc_datetime(2020, 12, 31))
    project.archive(now=utc_datetime(2021, 1, 12))

    # When
    project.unarchive()

    # Then
    assert project.archived_at is None
    assert project.archived is False


def test_delete_project():
    # Given
    project = ProjectBuilder().build()
    project.archive(now=utc_datetime(2021, 1, 12))

    # When
    project.delete(now=utc_datetime(2022, 1, 12))

    # Then
    assert project.deleted_at == utc_datetime(2022, 1, 12)


def test_delete_project_raises_error_whe_not_archived():
    # Given
    project = ProjectBuilder().build()

    # When
    with pytest.raises(ProjectNotArchivedError):
        project.delete(now=utc_datetime(2022, 1, 12))
