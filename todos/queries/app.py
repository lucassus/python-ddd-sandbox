from databases import Database
from fastapi import FastAPI, Request

from todos.config import DATABASE_URL
from todos.queries.routes import api_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)

    database = Database(DATABASE_URL)

    @app.middleware("http")
    async def db_session_middleware(request: Request, call_next):
        request.state.database = database
        response = await call_next(request)
        return response

    @app.on_event("startup")
    async def startup():
        await database.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()

    return app
