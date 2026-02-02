from fastapi import APIRouter

from app.api.api_v1.endpoints import auth_local, health

api_router = APIRouter()

api_router.include_router(
    health.router,
    tags=["Health"],
)

api_router.include_router(
    auth_local.router,
    prefix="/auth",
    tags=["Authentication"],
)
