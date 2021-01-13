from fastapi import FastAPI

from todos.entrypoints.api import api_router
from todos.interfaces.db.session import engine
from todos.interfaces.db.tables import metadata, start_mappers

metadata.create_all(bind=engine)
start_mappers()


# TODO: Move it to the better place
def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)

    return app


app = create_app()
