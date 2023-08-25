from typing import Self

from app.modules.projects.domain.project import MaximumNumberOfIncompleteTasks, Project, ProjectName
from app.modules.shared_kernel.entities.user_id import UserID


class ProjectBuilder:
    # Provide some sane defaults
    _name = ProjectName("Test project")
    _maximum_number_of_incomplete_tasks: None | MaximumNumberOfIncompleteTasks = None

    def __init__(self):
        self._user_id = UserID.generate()

    def with_maximum_number_of_incomplete_tasks(self, value: None | int | MaximumNumberOfIncompleteTasks) -> Self:
        self._maximum_number_of_incomplete_tasks = MaximumNumberOfIncompleteTasks(int(value)) if value else None
        return self

    def with_name(self, name: str | ProjectName) -> Self:
        self._name = ProjectName(str(name))
        return self

    def build(self) -> Project:
        return Project(
            user_id=self._user_id,
            name=self._name,
            maximum_number_of_incomplete_tasks=self._maximum_number_of_incomplete_tasks,
        )
