from datetime import date

from todos.domain.models.todo import Todo


# TODO: Find a way to write proper integration tests
# TODO: How to organize tests by type: unit/integration/e2e
def test_integration(session, client):
    response = client.get("/todos")

    assert response.status_code == 200
    assert response.json() == []

    response = client.post("/todos", json={"name": "Test todo"})
    assert response.status_code == 200

    response = client.post("/todos", json={"name": "The other todo"})
    assert response.status_code == 200

    response = client.get("/todos")

    assert response.status_code == 200
    todos = response.json()
    assert len(todos) == 2
    assert todos == [
        {"id": 1, "name": "Test todo", "completed_at": None},
        {"id": 2, "name": "The other todo", "completed_at": None},
    ]

    response = client.put("/todos/1/complete")
    assert response.status_code == 200
    # TODO: Does not work
    assert session.query(Todo).get(1).completed_at is not None


def test_todos_endpoint(session, client):
    # Given
    session.add(Todo(name="Test todo"))
    session.add(Todo(name="The other todo", completed_at=date(2021, 1, 6)))
    session.commit()

    # When
    response = client.get("/todos")

    # Then
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Test todo", "completed_at": None},
        {"id": 2, "name": "The other todo", "completed_at": "2021-01-06"},
    ]


def test_todo_endpoint_returns_todo(session, client):
    session.add(Todo(id=1, name="Test name"))
    response = client.get("/todos/1")

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Test name", "completed_at": None}


def test_todo_endpoint_returns_404(client):
    response = client.get("/todos/1")
    assert response.status_code == 404


def test_todo_complete_endpoint(session, client):
    todo = Todo(name="Test")
    session.add(todo)
    session.commit()

    response = client.put(f"/todos/{todo.id}/complete")

    assert response.status_code == 200
    assert todo.completed_at is not None


def test_todo_complete_endpoint_returns_404(client):
    response = client.put(f"/todos/{123}/complete")
    assert response.status_code == 404
