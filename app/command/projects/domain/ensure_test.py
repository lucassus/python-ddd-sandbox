import pytest

from app.command.projects.domain import ensure
from app.command.projects.domain.errors import MaxIncompleteTasksNumberIsReachedError
from app.command.projects.domain.project_builder import ProjectBuilder


class TestEnsureProjectHasAllowedNumberOfIncompleteTasks:
    def test_passes_if_maximum_number_of_incomplete_tasks_is_none(self):
        project = ProjectBuilder().with_maximum_number_of_incomplete_tasks(None).build()

        try:
            ensure.project_has_allowed_number_of_incomplete_tasks(project)
        except MaxIncompleteTasksNumberIsReachedError:
            pytest.fail()

    def test_passes_if_maximum_number_of_incomplete_tasks_is_not_reached(self):
        project = ProjectBuilder().with_maximum_number_of_incomplete_tasks(2).build()
        project.add_task(name="First")

        try:
            ensure.project_has_allowed_number_of_incomplete_tasks(project)
        except MaxIncompleteTasksNumberIsReachedError:
            pytest.fail()

    def test_fails_if_maximum_number_of_incomplete_tasks_is_reached(self):
        project = ProjectBuilder().with_maximum_number_of_incomplete_tasks(2).build()
        project.add_task(name="First")
        project.add_task(name="Second")

        with pytest.raises(MaxIncompleteTasksNumberIsReachedError):
            ensure.project_has_allowed_number_of_incomplete_tasks(project)
