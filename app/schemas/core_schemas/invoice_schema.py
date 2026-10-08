from app.config import settings
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional, Type, Union
from pydantic import BaseModel, Field, model_validator
from app.utils.core_utils import utc_now

class FetchInvoicesInput(BaseModel):
    """Input schema for FetchEmailInvoicesTool."""

    subject_keyword: Optional[str] = Field(
        default="invoice", description="Keyword to search in email subject lines."
    )
    sender_email: Optional[str] = Field(
        default=settings.SENDER_EMAIL, description="Optional sender email address to filter by."
    )
    since_date: Optional[Union[date, datetime]] = Field(
        default=utc_now().date(), description="Optional start date filter (inclusive)."
    )
    until_date: Optional[Union[date, datetime]] = Field(
        default=utc_now().date() + timedelta(days=1), description="Optional end date filter (inclusive)."
    )

class ExtractPDFInput(BaseModel):
    """Input schema for ExtractPDFContentTool."""
    file_path: str = Field(description="Local disk path to the downloaded invoice PDF file.")

class LineItemSchema(BaseModel):
    """Schema representing an individual line item on an invoice."""

    description: str = Field(description="Description of the item or service provided.")
    quantity: float = Field(default=1.0, description="Quantity of items purchased.")
    unit_price: float = Field(description="Price per unit of the item.")
    amount: float = Field(description="Total price for this line item (quantity * unit_price).")

class InvoiceDataSchema(BaseModel):
    """Schema representing structured data extracted from an invoice PDF."""

    invoice_number: Optional[str] = Field(
        default=None, description="Unique invoice or bill identifier."
    )
    vendor_name: Optional[str] = Field(
        default=None, description="Name of the vendor or issuing company."
    )
    vendor_address: Optional[str] = Field(
        default=None, description="Address of the vendor, if present."
    )
    invoice_date: Optional[str] = Field(
        default=None, description="Date the invoice was issued (YYYY-MM-DD)."
    )
    due_date: Optional[str] = Field(
        default=None, description="Payment due date (YYYY-MM-DD)."
    )
    
    line_items: List[LineItemSchema] = Field(
        default_factory=list, description="List of individual line items listed on the invoice."
    )

    subtotal: float = Field(default=0.0, description="Subtotal amount before taxes and fees.")
    tax: float = Field(default=0.0, description="Tax or VAT amount.")
    total_amount: float = Field(default=0.0, description="Final total amount payable.")
    currency: str = Field(default="USD", description="Currency code (e.g., USD, EUR, INR).")