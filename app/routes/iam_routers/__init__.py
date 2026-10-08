from fastapi import APIRouter
from app.routes.iam_routers.auth_route import router as auth_router


router = APIRouter()
router.include_router(auth_router)