from app.config import logger
from app.utils.core_utils import log_node
from app.schemas.core_schemas import GraphState
from typing import Any, Dict
from app.services.core_services import InvoiceService
from app.constants import INVOICE_STATUS

@log_node
def make_invoice_completed_node(state: GraphState) -> Dict[str, Any]:
    InvoiceService.object().update_invoice(
        invoice_id=state.invoice_id,
        reviewer_notes=state.review_note,
        status=INVOICE_STATUS.COMPLETED
    )

    logger.info("Update invoice data: %s", {
        "invoice_id": state.invoice_id,
        "status": INVOICE_STATUS.COMPLETED,
        "reviewer_notes": state.review_note
    })

    return {
        "status": INVOICE_STATUS.COMPLETED
    }    
