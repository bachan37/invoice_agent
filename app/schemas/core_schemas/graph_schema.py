from app.constants import INVOICE_STATUS
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class GraphState(BaseModel):
    """graph's state"""
    thread_id: Optional[str] = Field(None, description="Thread id of the graph")
    file_path: Optional[str] = Field(None, description="Active file path being processed")
    filename: Optional[str] = Field(None, description="Active file name being processed")
    invoice_id: Optional[int] = Field(None, description="Database primary key of active invoice")
    
    # Per-file processing fields
    actual_content: Optional[str] = None
    parsed_content: Optional[dict] = None
    status: INVOICE_STATUS = Field(default=INVOICE_STATUS.FETCHED)
    review_approved: Optional[bool] = None
    review_note: Optional[str] = None
    
    # Completed results accumulator
    processed_invoices: List[Dict[str, Any]] = Field(default_factory=list)

    # Error tracking
    error_message: Optional[str] = None
    retry_count: int = 0

    