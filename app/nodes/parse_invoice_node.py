from app.services.core_services import InvoiceService
from app.constants import INVOICE_STATUS
from app.schemas.core_schemas import GraphState, InvoiceDataSchema
from typing import Dict, Any
from app.services.core_services.parse_invoice_service import parse_invoice_service
from app.config import logger
import json
from datetime import date, datetime

def parse_invoice_node(state: GraphState) -> Dict[str, Any]:
    """Node: Converts raw PDF text into structured JSON via LLM and updates SQLite."""

    if state.actual_content is None:
        return {"status": INVOICE_STATUS.FAILED, "error_message": "No actual content available."}
        
    logger.info(f"Parsing invoice content: {state.actual_content}")
    parsed_result: InvoiceDataSchema = parse_invoice_service.parse(state.actual_content)
    content = (
            parsed_result.model_dump()
            if hasattr(parsed_result, "model_dump")
            else parsed_result.dict()
        )

    logger.info(f"Parsed invoice content: {content}")
    status = INVOICE_STATUS.PARSED

    InvoiceService.object().update_invoice(
        invoice_id=state.invoice_id,
        extracted_data=json.dumps(content),
        status=status
    )

    return {
        "parsed_content": content, 
        "invoice_id": state.invoice_id, 
        "status":status
    }


