from app.modules.projects.domain.testing import build_test_task


def test_build_task():
    task = build_test_task(name="Test task")

    assert task.id is None  # TODO: But in fact task.id cannot be None
    assert task.name == "Test task"
    assert task.completed_at is None
