from todos.commands.entrypoints.api.app import create_app as create_commands_app
from todos.queries.app import create_app

app = create_app()

commands_app = create_commands_app()
app.mount("/commands", commands_app)
