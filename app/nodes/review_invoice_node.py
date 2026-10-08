from langgraph.types import interrupt
from app.schemas.core_schemas import GraphState
from app.constants import INVOICE_STATUS
from app.services.core_services import InvoiceService
from app.config import logger

def review_invoice_node(state: GraphState) -> dict:
    """Node: Validates invoice arithmetic. Pauses graph via interrupt()"""

    InvoiceService.object().update_invoice(
        invoice_id=state.invoice_id,
        status=INVOICE_STATUS.PENDING_REVIEW
    )

    logger.info("Interrupting graph execution for manual review. Invoice ID: %s", state.invoice_id)

    human_response = interrupt({
        "invoice_id": state.invoice_id,
        "parsed_content": state.parsed_content,
        "status": INVOICE_STATUS.PENDING_REVIEW
    })

    # Resumes here after FastAPI receives resume POST request with Command(resume=...)
    # Payload format expected from API: {"approved": True/False, "corrected_content": {...}, "reviewer_note": "..."}
    breakpoint()
    is_approved = human_response.get("approved", True)
    #corrected_data = human_response.get("corrected_content", state.parsed_content)
    note = human_response.get("reviewer_note", "")
    status = INVOICE_STATUS.APPROVED if is_approved else INVOICE_STATUS.REJECTED
    
    # Update SQLite with human input
    if is_approved:
        status = INVOICE_STATUS.APPROVED
    else:
        status = INVOICE_STATUS.REJECTED

    InvoiceService.object().update_invoice(
        invoice_id=state.invoice_id,
        status=status,
        #extracted_data=corrected_data,  # Save human-corrected JSON
        reviewer_notes=note
    )

    return {
        #"parsed_content": corrected_data,
        "status": status,
        "review_note": note,
        "review_approved": is_approved,
    }
    
