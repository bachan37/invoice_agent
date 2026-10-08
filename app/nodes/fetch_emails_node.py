from app.schemas.core_schemas import GraphState
from typing import Any, Dict
from app.tools import fetch_email_invoices_tool
from app.constants import INVOICE_STATUS
from app.services.core_services import InvoiceService

def fetch_emails_node(state: GraphState) -> Dict[str, Any]:
    """Fetches emails and pushes all PDF paths into file_queue."""
    files = fetch_email_invoices_tool.invoke({})
    if not files:
        return {"status": INVOICE_STATUS.COMPLETED}
    
    queue_items = []

    # Create initial records in SQLite
    for file_info in files:
        path = file_info["file_path"]
        name = file_info["filename"]

        # create a new invoice record
        created_invoice = InvoiceService.object().create_record(
            file_path=path,
            filename=name,
            status=INVOICE_STATUS.FETCHED
        )
        if created_invoice:
            queue_items.append({
                "invoice_id": created_invoice.id,
                "file_path": created_invoice.file_path
            })

    return {
        "file_queue": queue_items,
        "status": INVOICE_STATUS.FETCHED
    }
