from fastapi import APIRouter

from app.api.endpoints import users, images

api_router = APIRouter()

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)

api_router.include_router(
    images.router,
    prefix="/images",
    tags=["Images"]
)