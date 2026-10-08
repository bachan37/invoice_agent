from app.schemas.core_schemas import GraphState
from typing import Any, Dict
from app.constants import INVOICE_STATUS

def revert_to_sender_node(state: GraphState) -> Dict[str, Any]:
    from app.services.core_services.email_service import EmailService
    from app.services.core_services.invoice_service import InvoiceService
    # call email service to revert
    
    InvoiceService.object().update_invoice(
        invoice_id=state.invoice_id,
        status=INVOICE_STATUS.REVERTED
    )

    EmailService().send_rejection_email(
        reason=state.review_note
    )

    return {
        "status": INVOICE_STATUS.REVERTED
    }