from app.modules.projects.domain.factories import build_example_project
from app.modules.projects.domain.project import ProjectID
from app.modules.projects.use_cases.ports import AbstractUnitOfWork
from app.shared_kernel.user_id import UserID


class CreateExampleProject:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def __call__(self, user_id: UserID) -> ProjectID:
        with self.uow:
            new_project = build_example_project(user_id)
            self.uow.project.create(new_project)
            self.uow.commit()

            return new_project.id
