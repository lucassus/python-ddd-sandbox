from typing import Self

from app.command.projects.entities.project import Project, ProjectName
from app.command.shared_kernel.entities.user_id import UserID


class ProjectBuilder:
    _user_id = UserID(1)
    _name = ProjectName("Test project")
    _maximum_number_of_incomplete_tasks: int | None = None

    def with_maximum_number_of_incomplete_tasks(self, value: int | None) -> Self:
        self._maximum_number_of_incomplete_tasks = value
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
