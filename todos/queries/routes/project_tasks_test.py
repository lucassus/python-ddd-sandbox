def test_tasks_endpoint(client):
    # Given
    project = build_project(id=1)
    project.tasks.extend(
        [
            build_task(id=1, name="Test task"),
            build_task(id=2, name="The other task", completed_at=date(2021, 1, 6)),
            build_task(id=3, name="Testing 123"),
        ]
    )

    fake_uow = FakeUnitOfWork(
        projects=[
            project,
            build_project(id=2, name="Other Project"),
        ]
    )
    client.app.dependency_overrides[get_uow] = lambda: fake_uow

    # When
    response = client.get(f"/projects/{project.id}/tasks")

    # Then
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Test task", "completedAt": None},
        {"id": 2, "name": "The other task", "completedAt": "2021-01-06"},
        {"id": 3, "name": "Testing 123", "completedAt": None},
    ]


def test_tasks_endpoint_integration(session, client):
    # Given
    project = build_project()
    project.add_task(name="Test task")
    task = project.add_task(name="The other task")
    task.completed_at = date(2021, 1, 6)

    session.add(project)
    session.commit()

    # When
    response = client.get(f"/projects/{project.id}/tasks")

    # Then
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Test task", "completedAt": None},
        {"id": 2, "name": "The other task", "completedAt": "2021-01-06"},
    ]


def test_task_endpoint_returns_task(session, client):
    # Given
    project = build_project()
    task = project.add_task(name="Test name")
    session.add(project)
    session.commit()

    # When
    response = client.get(f"/projects/{project.id}/tasks/{task.id}")

    # Then
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Test name", "completedAt": None}


def test_task_endpoint_returns_404(client):
    response = client.get("/tasks/1")
    assert response.status_code == 404
