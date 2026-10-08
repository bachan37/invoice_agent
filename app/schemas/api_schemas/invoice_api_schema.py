from datetime import datetime
from app.constants import INVOICE_STATUS
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Literal

class InvoiceResponse(BaseModel):
    id: int
    thread_id: str
    status: INVOICE_STATUS
    file_path: Optional[str] = None
    extracted_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    
class InvoiceListResponse(BaseModel):
    total: int
    invoices: List[InvoiceResponse]

class InvoiceReviewRequest(BaseModel):
    action: Literal[INVOICE_STATUS.APPROVED, INVOICE_STATUS.REJECTED] = Field(
        ..., description="Action: APPROVED/REJECTED"
    ),
    note: str = Field(..., description="Note"),

class InvoiceReivewResponse(BaseModel):
    id: int
    thread_id: str
    status: INVOICE_STATUS
    reviewer_note: Optional[str] = None
    