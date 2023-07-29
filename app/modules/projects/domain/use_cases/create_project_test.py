from app.modules.projects.domain.ports import AbstractRepository
from app.modules.projects.domain.use_cases.create_project import CreateProject
from app.shared_kernel.user_id import UserID


def test_create_project_use_case(fake_uow, repository: AbstractRepository):
    create_project = CreateProject(uow=fake_uow)
    project_id = create_project(user_id=UserID(1), project_name="Project X")

    assert fake_uow.committed

    project = repository.get(project_id)
    assert project.name == "Project X"
    assert project.user_id == UserID(1)
    assert len(project.tasks) == 0
