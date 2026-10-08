from typing import Literal
from app.agents.graph import invoice_graph
from app.constants import INVOICE_STATUS
from typing import Any, Dict
from app.config import logger
from langgraph.types import Command

class WorkflowService:
    def resume_processing(self, thread_id: str, action: Literal[INVOICE_STATUS.APPROVED, INVOICE_STATUS.REJECTED], note: str) -> Dict[str, Any]:
        config = {"configurable": {"thread_id": thread_id}}
        is_approved = action == INVOICE_STATUS.APPROVED

        resume_payload = {
            "approved": is_approved,
            "reviewer_note": note
        }

        logger.info(f"Resuming graph thread {thread_id} with payload: {resume_payload}")
        final_state = invoice_graph.invoke(
            Command(resume=resume_payload),
            config=config,
        )
        return final_state