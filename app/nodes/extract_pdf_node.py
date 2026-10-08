from app.schemas.core_schemas import GraphState
from typing import Any, Dict
from app.constants import INVOICE_STATUS
from app.tools.extract_invoice_pdf_tool import extract_invoice_pdf_tool
from app.services.core_services import InvoiceService
from app.config import logger

def extract_pdf_node(state: GraphState) -> Dict[str, Any]:
    """Node to extract raw text content using pypdf tool."""
    if not state.file_path:
        return {"error_message": "No file path provided for PDF extraction."}

    
    raw_text = extract_invoice_pdf_tool.invoke({"file_path": state.file_path})

    if(raw_text is None):
        logger.error(f"Node2: Failed to extract the raw content for file_name:{state.filename}")
        return {"status": INVOICE_STATUS.FAILED, "error_message": "Extraction failed: No raw text extracted"}
        
    logger.info(f"Node2: Extract the raw content: {raw_text}")

    # update extracted content in database
    InvoiceService.object().update_invoice(
        invoice_id=state.invoice_id,
        raw_data=raw_text,
        status=INVOICE_STATUS.EXTRACTED
    )

    return {
        "actual_content": raw_text,
        "status": INVOICE_STATUS.EXTRACTED,
    }
    