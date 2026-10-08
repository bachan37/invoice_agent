from langchain_core.tools import StructuredTool
from app.schemas.core_schemas.invoice_schema import FetchInvoicesInput
from app.services.core_services import fetch_invoice_service

fetch_email_invoices_tool = StructuredTool.from_function(
    func=fetch_invoice_service.execute,
    name="fetch_email_invoices",
    description="Fetches emails matching the given criteria and extracts attachments. "
    "Use this tool to get email invoices.",
    args_schema=FetchInvoicesInput,
)