from todos.domain import ensure
from todos.test_utils.factories import build_project


# TODO: How to make shorted names?
def test_allowed_number_of_unfinished_tasks_is_not_reached():
    project = build_project()

    ensure.allowed_number_of_unfinished_tasks_is_not_reached(project)
