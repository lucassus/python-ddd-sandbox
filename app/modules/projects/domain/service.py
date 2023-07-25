from datetime import date, datetime

from app.modules.projects.domain.entities import Project
from app.modules.projects.domain.ports import AbstractUnitOfWork


class Service:
    def __init__(self, *, uow: AbstractUnitOfWork):
        self._uow = uow

    def create_example_project(self, *, user_id: int) -> int:
        with self._uow as uow:
            project = Project(name="My first project")
            project.user_id = user_id

            task = project.add_task(name="Sign up!")
            task.complete(datetime.utcnow())

            project.add_task(name="Watch the tutorial")
            project.add_task(name="Start using our awesome app")

            uow.repository.create(project)
            uow.commit()

            return project.id

    def create_task(self, *, project_id, name: str) -> int:
        with self._uow as uow:
            project = uow.repository.get(project_id)
            task = project.add_task(name=name)

            uow.commit()
            return task.id

    def complete_task(self, id: int, *, project_id: int, now: date) -> None:
        with self._uow as uow:
            project = uow.repository.get(project_id)
            project.complete_task(id, now)

            uow.commit()

    def incomplete_task(self, id: int, *, project_id: int) -> None:
        with self._uow as uow:
            project = uow.repository.get(project_id)
            project.incomplete_task(id)

            uow.commit()
