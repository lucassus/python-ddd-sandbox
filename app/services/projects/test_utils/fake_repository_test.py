from app.services.projects.test_utils.factories import build_project
from app.services.projects.test_utils.fake_repository import FakeRepository


def test_fake_repository():
    repository = FakeRepository(
        projects=[
            build_project(id=1, name="First"),
        ]
    )

    repository.create(build_project(name="Foo"))
    repository.create(build_project(name="Bar"))

    assert len(repository.list()) == 3

    project = repository.get(1)
    assert project is not None
    assert project.id == 1
