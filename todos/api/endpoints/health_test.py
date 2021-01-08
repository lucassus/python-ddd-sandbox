def test_hello_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"message": "I'm fine!"}
