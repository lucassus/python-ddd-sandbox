import pytest
from sqlalchemy.orm import Session

from app.command.accounts.domain.email_address import EmailAddress
from app.command.accounts.domain.password import Password
from app.command.accounts.domain.user import User
from app.command.accounts.infrastructure.adapters.user_repository import UserRepository
from app.command.projects.domain.project import Project, ProjectName
from app.command.projects.infrastructure.adapters.project_repository import ProjectRepository


@pytest.fixture()
def create_user(session: Session):
    repository = UserRepository(session=session)

    def _create_user(email: EmailAddress | None = None):
        user = User(
            email=email or EmailAddress("test@email.com"),
            password=Password("password"),
        )

        repository.create(user)
        session.commit()

        return user

    return _create_user


@pytest.fixture()
def create_project(session: Session, create_user):
    repository = ProjectRepository(session=session)

    def _create_project(
        user: User | None = None,
        name: ProjectName | None = None,
    ):
        if user is None:
            user = create_user()

        project = Project(
            user_id=user.id,
            name=name or ProjectName("Test project"),
        )

        repository.create(project)
        session.commit()

        return project

    return _create_project
