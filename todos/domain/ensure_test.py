import pytest

from todos.domain import ensure
from todos.domain.errors import MaxUnfinishedTasksNumberIfReached
from todos.test_utils.factories import build_project, build_task


class TestEnsureAllowedNumberOfUnfinishedTasksIsNotReached:
    def test_passes_if_max_unfinished_tasks_number_is_none(self):
        project = build_project(max_unfinished_tasks_number=None)

        try:
            ensure.max_unfinished_tasks_number_is_not_reached(project)
        except MaxUnfinishedTasksNumberIfReached:
            pytest.fail()

    def test_passes_if_max_unfinished_tasks_number_is_not_reached(self):
        project = build_project(max_unfinished_tasks_number=2)
        project.tasks.append(build_task())

        try:
            ensure.max_unfinished_tasks_number_is_not_reached(project)
        except MaxUnfinishedTasksNumberIfReached:
            pytest.fail()

    def test_fails_if_max_unfinished_tasks_number_is_reached(self):
        project = build_project(max_unfinished_tasks_number=2)
        project.tasks.append(build_task())
        project.tasks.append(build_task())

        with pytest.raises(MaxUnfinishedTasksNumberIfReached):
            ensure.max_unfinished_tasks_number_is_not_reached(project)
