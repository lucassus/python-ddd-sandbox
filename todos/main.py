from todos.query_service.app import create_app
from todos.services.project_management.entrypoints.app import (
    create_app as create_commands_app,
)

app = create_app()

commands_app = create_commands_app()
app.mount("/commands", commands_app)
