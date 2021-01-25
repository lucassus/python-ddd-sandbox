from todos.infrastructure.session import engine
from todos.infrastructure.tables import create_tables
from todos.query_service.app import create_app
from todos.services.app import create_app as create_commands_app

create_tables(engine)

app = create_app()

commands_app = create_commands_app()
app.mount("/commands", commands_app)
