import pytest

from app.command.projects.entities import ensure
from app.command.projects.entities.errors import MaxIncompleteTasksNumberIsReached
from app.command.projects.entities.factories import build_project


class TestEnsureProjectHasAllowedNumberOfIncompleteTasks:
    def test_passes_if_maximum_number_of_incomplete_tasks_is_none(self):
        project = build_project(name="Test Project", maximum_number_of_incomplete_tasks=None)

        try:
            ensure.project_has_allowed_number_of_incomplete_tasks(project)
        except MaxIncompleteTasksNumberIsReached:
            pytest.fail()

    def test_passes_if_maximum_number_of_incomplete_tasks_is_not_reached(self):
        project = build_project(name="Test Project", maximum_number_of_incomplete_tasks=2)
        project.add_task(name="First")

        try:
            ensure.project_has_allowed_number_of_incomplete_tasks(project)
        except MaxIncompleteTasksNumberIsReached:
            pytest.fail()

    def test_fails_if_maximum_number_of_incomplete_tasks_is_reached(self):
        project = build_project(name="Test Project", maximum_number_of_incomplete_tasks=2)
        project.add_task(name="First")
        project.add_task(name="Second")

        with pytest.raises(MaxIncompleteTasksNumberIsReached):
            ensure.project_has_allowed_number_of_incomplete_tasks(project)