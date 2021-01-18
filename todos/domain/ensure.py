from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from todos.domain.models import Project


def allowed_number_of_unfinished_tasks_is_not_reached(project: "Project") -> None:
    pass
