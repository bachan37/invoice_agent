from fastapi import APIRouter
from app.routes.core_routers.invoice_route import router as invoice_router
from app.routes.core_routers.invoice_review_route import router as invoice_review_router


router = APIRouter()
router.include_router(invoice_router)
router.include_router(invoice_review_router)