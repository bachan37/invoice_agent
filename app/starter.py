from app.constants import ROUTE_CONSTANTS
import os
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.exceptions import AppError
from fastapi import APIRouter, FastAPI
from app.config.env_config import settings
from app.config.log_config import logger
from app.utils.core_utils import init_db
from app.exceptions.handlers import (
    app_error_handler,
    global_exception_handler,
    http_exception_handler,
    request_validation_handler,
)
from app.routes.core_routers import router as core_router

def start_application():
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI app instance with middleware, routers, and DB init.
    """

    # PATH HANDLING
    if settings.USE_SQL:
        os.makedirs(os.path.dirname(settings.DB_PATH), exist_ok=True)
    os.makedirs(settings.LOG_DIR, exist_ok=True)
    os.makedirs(settings.INVOICES_DIR, exist_ok=True)

    # DATABASE INITIALIZATION
    if settings.USE_SQL:
        try:
            init_db()
        except Exception as e:
            logger.exception("Database initialization failed: %s", e)
            raise
    else:
        logger.info(
            "SQL disabled. Skipping database initialization and admin bootstrap."
        )

    print(f"DEBUG: LOG_DIR resolves to: '{settings.LOG_DIR}'")
    logger.info("Starting application...")
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description=settings.PROJECT_DESCRIPTION,
        root_path=settings.BASE_PATH,
    )

    # EXCEPTION HANDLERS
    app.add_exception_handler(RequestValidationError, request_validation_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(Exception, global_exception_handler)

    # CORS MIDDLEWARE
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    #Routes
    api_v1 = APIRouter(prefix=ROUTE_CONSTANTS.API_V1_PREFIX.value)
    api_v1.include_router(core_router)
    app.include_router(api_v1)

    logger.info("Application started successfully")
    return app

