from fastapi import FastAPI

from app.query.routes import api_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)

    return app
