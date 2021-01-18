import pytest

from todos.domain import ensure
from todos.domain.errors import MaximumNumberOfUnfinishedTasksIfReached
from todos.test_utils.factories import build_project, build_task


class TestEnsureAllowedNumberOfUnfinishedTasksIsNotReached:
    def test_passes_if_allowed_number_of_unfinished_tasks_is_none(self):
        project = build_project(allowed_number_of_unfinished_tasks=None)

        try:
            ensure.allowed_number_of_unfinished_tasks_is_not_reached(project)
        except MaximumNumberOfUnfinishedTasksIfReached:
            pytest.fail()

    def test_passes_if_allowed_number_of_tasks_is_not_reached(self):
        project = build_project(allowed_number_of_unfinished_tasks=2)
        project.tasks.append(build_task())

        try:
            ensure.allowed_number_of_unfinished_tasks_is_not_reached(project)
        except MaximumNumberOfUnfinishedTasksIfReached:
            pytest.fail()

    def test_fails_if_allowed_number_of_tasks_is_reached(self):
        project = build_project(allowed_number_of_unfinished_tasks=2)
        project.tasks.append(build_task())
        project.tasks.append(build_task())

        with pytest.raises(MaximumNumberOfUnfinishedTasksIfReached):
            ensure.allowed_number_of_unfinished_tasks_is_not_reached(project)
