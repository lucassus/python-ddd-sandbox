from starlette.testclient import TestClient


def test_heath_check_endpoint(anonymous_client: TestClient):
    response = anonymous_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"message": "I'm fine!"}
