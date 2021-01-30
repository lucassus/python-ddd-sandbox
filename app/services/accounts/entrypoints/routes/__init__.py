from fastapi import APIRouter

from app.services.accounts.entrypoints.routes import users

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
