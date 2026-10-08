from app.schemas.core_schemas.invoice_schema import ExtractPDFInput
from app.services.core_services import pdf_service
from langchain_core.tools import StructuredTool

extract_invoice_pdf_tool = StructuredTool.from_function(
    func=pdf_service.extract_text_from_pdf,
    name="extract_invoice_pdf",
    description="Extracts text from an invoice PDF file. Use this tool to extract text from an invoice PDF file.",
    args_schema=ExtractPDFInput,
)