from todos.entrypoints.api.app import create_app as create_commands_app
from todos.queries.app import create_app

app = create_app()


# TODO: Bring back tests:


# TODO: Move /health to queries


commands_app = create_commands_app()
app.mount("/commands", commands_app)
