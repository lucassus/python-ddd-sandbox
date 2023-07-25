from fastapi import FastAPI

from app.infrastructure.db import engine
from app.infrastructure.tables import create_tables
from app.modules.app import create_app as create_commands_app
from app.query.app import create_app as create_queries_app

create_tables(engine)

app = FastAPI()

app.mount("/", create_queries_app())
app.mount("/commands", create_commands_app())
