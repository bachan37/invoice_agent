from app.schemas.api_schemas.invoice_api_schema import InvoiceReivewResponse
from app.schemas.api_schemas.invoice_api_schema import InvoiceReviewRequest
from app.utils.core_utils import get_db
from app.services.core_services import InvoiceService, WorkflowService
from app.schemas.api_schemas import InvoiceResponse
import sqlite3
from app.exceptions import NotFoundError
from fastapi import APIRouter, Body, Depends, Path, status

# it should starts from invoices/:invoice_id/review
router = APIRouter(prefix="/invoices/{invoice_id}/review", tags=["invoice_review"])

def _invoice_service(db: sqlite3.Connection = Depends(get_db)) -> InvoiceService:
    """Returns the invoice service."""
    return InvoiceService(db)

def _workflow_service() -> WorkflowService:
    """Returns the workflow service."""
    return WorkflowService()

# it should take the review as put request
# action: APPROVED/REJECTED
# body payload: note: str

@router.put("", status_code=status.HTTP_200_OK, response_model=InvoiceReivewResponse)
def update_invoice_review(
    invoice_id: int = Path(..., description="Invoice ID"),
    payload: InvoiceReviewRequest = Body(..., description="Review payload"),
    invoice_service: InvoiceService = Depends(_invoice_service),
    workflow_service: WorkflowService = Depends(_workflow_service),
):
    invoice = invoice_service.get_invoice(invoice_id)

    if not invoice:
        raise NotFoundError(message="Invoice not found")
        
    final_state = workflow_service.resume_processing(invoice.thread_id, payload.action, payload.note)

    return InvoiceReivewResponse(
        id=invoice.id,
        thread_id=invoice.thread_id,
        status=final_state.get("status"),
        reviewer_note=payload.note
    )
    
