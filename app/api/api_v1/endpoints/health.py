from fastapi import APIRouter

from app.core.config import get_settings
from app.db.session import check_database_connection
from app.models.auth import DetailedHealthResponse, HealthResponse

router = APIRouter()
settings = get_settings()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Basic health check endpoint for load balancer and monitoring",
)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        environment=settings.environment,
    )


@router.get(
    "/health/detailed",
    response_model=DetailedHealthResponse,
    summary="Detailed Health Check",
    description="Detailed health check with configuration and connectivity status",
)
async def detailed_health_check() -> DetailedHealthResponse:
    db_connected = await check_database_connection()

    return DetailedHealthResponse(
        status="healthy" if db_connected or not settings.database_url else "degraded",
        version=settings.app_version,
        environment=settings.environment,
        cognito_configured=bool(
            settings.cognito_user_pool_id and settings.cognito_app_client_id
        ),
        api_keys_configured=bool(settings.api_keys),
        database_configured=bool(settings.database_url),
        database_connected=db_connected,
    )
