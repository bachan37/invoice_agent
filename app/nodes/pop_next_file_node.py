from app.schemas.core_schemas import GraphState
from typing import Any, Dict
from app.constants import INVOICE_STATUS

def pop_next_file_node(state: GraphState) -> Dict[str, Any]:
    """Pops the next pending file path from file_queue and sets it as current_file_path."""
    queue = list(state.file_queue)
    active_item = queue.pop(0)

    return {
        "file_queue": queue,
        "invoice_id": active_item["invoice_id"],
        "current_file_path": active_item["file_path"],
        "actual_content": None,
        "parsed_content": None,
        "status": INVOICE_STATUS.FETCHED
    }