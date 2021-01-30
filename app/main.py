from app.infrastructure.session import engine
from app.infrastructure.tables import create_tables
from app.modules.app import create_app as create_commands_app
from app.query.app import create_app

create_tables(engine)

app = create_app()

commands_app = create_commands_app()
app.mount("/commands", commands_app)
