from app.exceptions import ConflictError
from app.services.iam_services.user_service import UserService
from app.services.iam_services import user_service
from app.schemas.core_schemas.role_schema import CreateRoleInputSchema
from app.constants import ROUTE_CONSTANTS
import os
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.exceptions import AppError
from fastapi import APIRouter, FastAPI
from app.config.env_config import settings
from app.config.log_config import logging
logger = logging.getLogger("app")

from app.utils.core_utils import init_db, sqlite_db
from app.models import Role
from app.services.iam_services import RoleService
from app.exceptions.handlers import (
    app_error_handler,
    global_exception_handler,
    http_exception_handler,
    request_validation_handler,
)
from app.routes.core_routers import router as core_router
from app.routes.iam_routers import router as iam_router
from app.schemas.core_schemas.user_schema import CreateUserInputSchema
from typing import Optional


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

    # CREATE predefined roles
    _seed_roles()
    _seed_users()

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
    api_v1.include_router(iam_router)
    app.include_router(api_v1)

    logger.info("Application started successfully")
    return app

def _seed_roles():
    """Seed predefined roles in the database."""
    role_names = [{
        "name": "admin",
        "description": "Administrator with full access to the system."
    }, {
        "name": "reviewer",
        "description": "Review invoice and approve and disapprove tra"
    }, {
        "name": "viewer",
        "description": "Viewer with read-only access to view transactions."
    }]
    db = sqlite_db.connect()
    role_service = RoleService(db)

    for role in role_names:
        """find or create role by its name"""
        role_service.get_or_create_role(CreateRoleInputSchema(**role))

def _seed_system_user():
    db = sqlite_db.connect()
    user_service = UserService(db)
    role_service = RoleService(db)

    role_names = ["admin", "reviewer"]
    role_ids = []

    for role_name in role_names:
        role: Optional[Role] = role_service.get_role_by_name(role_name)
        if role is None:
            raise Exception(f"Role {role_name} not found")
        role_ids.append(role.id)
    
    try:
        # create system user
        user_service.create_user(
            CreateUserInputSchema(
                first_name="System",
                last_name="AI",
                username=settings.SYSTEM_AI_USERNAME,
                email=settings.SYSTEM_AI_EMAIL,
                password=settings.SYSTEM_AI_PASSWORD,
                role_ids=role_ids
            )
        )
    except ConflictError:
        logger.info("System user exists.")


def _seed_users():
    # seed system user
    _seed_system_user()
    
    db = sqlite_db.connect()
    user_service = UserService(db)
    role_service = RoleService(db)

    admin_role = role_service.get_role_by_name("admin")
    reviewer_role = role_service.get_role_by_name("reviewer")

    user_data = [
        {
            "first_name": "Admin",
            "last_name": "User",
            "username": "admin",
            "email": "admin@invoiceexample.abc",
            "password": "admin",
            "role_ids": [admin_role.id]
        },
        {
            "first_name": "Reviewer",
            "last_name": "User",
            "username": "reviewer",
            "email": "reviewer@invoiceexample.abc",
            "password": "reviewer",
            "role_ids": [reviewer_role.id]
        },
        {
            "first_name": "Viewer",
            "last_name": "User",
            "username": "viewer",
            "email": "viewer@invoiceexample.abc",
            "password": "viewer",
            "role_ids": []
        }
    ]

    for user_datum in user_data:
        try:
            user_service.create_user(CreateUserInputSchema(**user_datum))
        except ConflictError:
            logger.info("User exists.")  


        

