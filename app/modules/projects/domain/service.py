from datetime import date, datetime

from app.modules.projects.domain.entities import Project, ProjectID, TaskID
from app.modules.projects.domain.ports import AbstractUnitOfWork
from app.shared_kernel.user_id import UserID


# TODO: Split it into smaller services / use cases
class Service:
    def __init__(self, *, uow: AbstractUnitOfWork):
        self._uow = uow

    def create_example_project(self, *, user_id: UserID) -> ProjectID:
        with self._uow as uow:
            entity = Project(name="My first project")
            entity.user_id = user_id

            task = entity.add_task(name="Sign up!")
            task.complete(datetime.utcnow())  # TODO: Inject datetime and write tests

            entity.add_task(name="Watch the tutorial")
            entity.add_task(name="Start using our awesome app")

            uow.project.create(entity)
            uow.commit()

            return entity.id

    def create_task(self, *, project_id: ProjectID, name: str) -> TaskID:
        with self._uow as uow:
            project = uow.project.get(project_id)
            task = project.add_task(name=name)

            uow.commit()
            return task.id

    def complete_task(self, id: TaskID, *, project_id: ProjectID, now: date) -> None:
        with self._uow as uow:
            project = uow.project.get(project_id)
            project.complete_task(id, now)

            uow.commit()

    def incomplete_task(self, id: TaskID, *, project_id: ProjectID) -> None:
        with self._uow as uow:
            project = uow.project.get(project_id)
            project.incomplete_task(id)

            uow.commit()
