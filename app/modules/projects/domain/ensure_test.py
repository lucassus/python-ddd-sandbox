import pytest

from app.modules.projects.domain import ensure
from app.modules.projects.domain.errors import MaxIncompleteTasksNumberIsReached
from app.modules.projects.test_utils.factories import build_project, build_task


class TestEnsureProjectHasAllowedNumberOfIncompleteTasks:
    def test_passes_if_maximum_number_of_incomplete_tasks_is_none(self):
        project = build_project(maximum_number_of_incomplete_tasks=None)

        try:
            ensure.project_has_allowed_number_of_incomplete_tasks(project)
        except MaxIncompleteTasksNumberIsReached:
            pytest.fail()

    def test_passes_if_maximum_number_of_incomplete_tasks_is_not_reached(self):
        project = build_project(maximum_number_of_incomplete_tasks=2)
        project.tasks.append(build_task())

        try:
            ensure.project_has_allowed_number_of_incomplete_tasks(project)
        except MaxIncompleteTasksNumberIsReached:
            pytest.fail()

    def test_fails_if_maximum_number_of_incomplete_tasks_is_reached(self):
        project = build_project(maximum_number_of_incomplete_tasks=2)
        project.tasks.append(build_task())
        project.tasks.append(build_task())

        with pytest.raises(MaxIncompleteTasksNumberIsReached):
            ensure.project_has_allowed_number_of_incomplete_tasks(project)
