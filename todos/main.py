from todos.entrypoints.api.app import app as commands_api
from todos.queries.app import create_app

app = create_app()


# TODO: Bring back tests:
# def test_hello_endpoint(client):
#     response = client.get("/health")
#
#     assert response.status_code == 200
#     assert response.json() == {"message": "I'm fine!"}


@app.get("/health")
def health_endpoint():
    return {"message": "I'm fine!"}


app.mount("/commands", commands_api)
