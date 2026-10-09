from app.schemas.core_schemas import GraphState
from app.constants import INVOICE_STATUS
from app.services.core_services import InvoiceService
from app.services.iam_services import UserService
from app.config import logger
from typing import Dict, Any
from app.utils.core_utils import get_db
from app.utils.core_utils import log_node

@log_node
def create_invoice_node(state: GraphState) -> Dict[str, Any]:
    """Creates the invoice database record."""
    filename = state.filename
    file_path = state.file_path
    thread_id = state.thread_id
    created_invoice = InvoiceService.object().create_record(
        thread_id=thread_id,
        file_path=file_path,
        filename=filename,
        status=INVOICE_STATUS.FETCHED,
        created_by=state.user_id,
    )
    logger.info(
        "create_invoice_node: Created invoice DB record ID=%s with thread_id=%s for file=%s",
        created_invoice.id,
        thread_id,
        filename,
    )
    return {"invoice_id": created_invoice.id, 
    "status": INVOICE_STATUS.FETCHED, 
    "created_by": state.user_id}

    