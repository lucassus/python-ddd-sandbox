from fastapi import FastAPI, Request

from app.query.routes import api_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)

    # TODO: Setup database connection
    # engine = create_engine(settings.database_url, echo=True)

    @app.middleware("http")
    async def db_session_middleware(request: Request, call_next):
        # request.state.engine = engine
        response = await call_next(request)
        return response

    # @app.on_event("startup")
    # async def startup():
    #     await database.connect()

    # @app.on_event("shutdown")
    # async def shutdown():
    #     await engine.dispose()

    return app
