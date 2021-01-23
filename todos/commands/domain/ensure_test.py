import pytest

from todos.commands.domain import ensure
from todos.commands.domain.errors import MaxIncompleteTasksNumberIsReached
from todos.test_utils.factories import build_project, build_task


class TestEnsureProjectHasAllowedNumberOfIncompleteTasks:
    def test_passes_if_max_incomplete_tasks_number_is_none(self):
        project = build_project(max_incomplete_tasks_number=None)

        try:
            ensure.project_has_allowed_number_of_incomplete_tasks(project)
        except MaxIncompleteTasksNumberIsReached:
            pytest.fail()

    def test_passes_if_max_incomplete_tasks_number_is_not_reached(self):
        project = build_project(max_incomplete_tasks_number=2)
        project.tasks.append(build_task())

        try:
            ensure.project_has_allowed_number_of_incomplete_tasks(project)
        except MaxIncompleteTasksNumberIsReached:
            pytest.fail()

    def test_fails_if_max_incomplete_tasks_number_is_reached(self):
        project = build_project(max_incomplete_tasks_number=2)
        project.tasks.append(build_task())
        project.tasks.append(build_task())

        with pytest.raises(MaxIncompleteTasksNumberIsReached):
            ensure.project_has_allowed_number_of_incomplete_tasks(project)
