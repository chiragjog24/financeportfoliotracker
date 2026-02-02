from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.api.api_v1.api import api_router
from app.core.config import get_settings
from app.core.exceptions import (
    BaseAPIException,
    base_api_exception_handler,
    generic_exception_handler,
    http_exception_handler,
)
from app.core.logging import setup_logging, get_logger
from app.db.session import init_db, close_db
from app.middleware.cors import setup_cors
from app.middleware.logging import setup_logging_middleware

settings = get_settings()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("application_starting", version=settings.app_version)

    await init_db()
    logger.info("database_initialized")

    yield

    await close_db()
    logger.info("database_connections_closed")
    logger.info("application_shutdown")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API for managing investment portfolios and tracking financial performance",
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    docs_url=f"{settings.api_v1_prefix}/docs",
    redoc_url=f"{settings.api_v1_prefix}/redoc",
    lifespan=lifespan,
)

setup_cors(app)
setup_logging_middleware(app)

app.add_exception_handler(BaseAPIException, base_api_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/", include_in_schema=False)
async def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": f"{settings.api_v1_prefix}/docs",
    }
