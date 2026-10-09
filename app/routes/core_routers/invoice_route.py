from app.exceptions import ForbiddenError
from app.policies.core.types import Action
from app.policies.core.types import ResourceContext
from app.models import User
from app.policies.invoice_policy import InvoicePolicy
from app.utils.iam_utils.auth_deps import get_current_user_payload
from app.utils.iam_utils.auth_deps import TokenPayload
from app.utils.core_utils import get_db
from app.services.core_services import InvoiceService
from app.schemas.api_schemas import InvoiceResponse
import sqlite3
from typing import List, Optional
from app.constants import INVOICE_STATUS
from app.exceptions import NotFoundError
from app.config import logger
from typing import Optional
from app.models import Invoice

from fastapi import APIRouter, Depends, status, Query

router = APIRouter(prefix="/invoices", tags=["invoices"])

def _invoice_service(db: sqlite3.Connection = Depends(get_db)) -> InvoiceService:
    """Returns the invoice service."""
    return InvoiceService(db)

def _invoice_policy(db: sqlite3.Connection = Depends(get_db), payload: TokenPayload = Depends(get_current_user_payload), invoice: Optional[Invoice] = None) -> InvoicePolicy:
    resource_context = ResourceContext(
        resource=invoice,
        owner_id=invoice.created_by,
        attributes={
            "status":invoice.status,
        }
    )
    return InvoicePolicy(db, payload, resource_context)

def can_perform(payload: TokenPayload, invoice: Invoice, action: Action) -> bool:
    policy = _invoice_policy(payload=payload, invoice=invoice)
    return policy.can_perform(action)
    
# for index action
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[InvoiceResponse],
    summary="Get list of all invoices",
    description="Returns list of all invoices from the database.",
)
def list_invoices(
    invoice_service: InvoiceService = Depends(_invoice_service),
    status_filter: Optional[INVOICE_STATUS] = Query(
        None, alias="status", description="Filter by status, e.g. PENDING_REVIEW, APPROVED, REJECTED"
    ),
):
    invoices = invoice_service.list_invoices(status_filter=status_filter)
    return [InvoiceResponse(**invoice.model_dump()) for invoice in invoices]

# for show action "invoices/id"
@router.get(
    "/{invoice_id}",
    status_code=status.HTTP_200_OK,
    response_model=InvoiceResponse,
    summary="Get invoice by id",
    description="Returns invoice by id.",
)
def show_invoice(
    invoice_id: int,
    payload: TokenPayload = Depends(get_current_user_payload),
    invoice_service: InvoiceService = Depends(_invoice_service),
):
    
    invoice = invoice_service.get_invoice(invoice_id)
    if not invoice:
        raise NotFoundError(message="Invoice not found")

    if not can_perform(payload=payload, invoice=invoice, action=Action.READ):
        raise ForbiddenError(message="You don't have permission to perform this action.")
    
    return InvoiceResponse(**invoice.model_dump())
    


#for show action by thread_id i.e. "invoices/thread/{thread_id}"
@router.get(
    "/thread/{thread_id}",
    status_code=status.HTTP_200_OK,
    response_model=InvoiceResponse,
    summary="Get invoice by thread id",
    description="Returns invoice by thread id.",
)
def show_invoice_by_thread_id(
    thread_id: str,
    payload: TokenPayload = Depends(get_current_user_payload),
    invoice_service: InvoiceService = Depends(_invoice_service),
):
    invoice = invoice_service.get_invoice_by_thread_id(thread_id)
    if not invoice:
        raise NotFoundError(message="Invoice not found")

    if not can_perform(payload=payload, invoice=invoice, action=Action.READ):
        raise ForbiddenError(message="You don't have permission to perform this action.")

    return InvoiceResponse(**invoice.model_dump())
    









