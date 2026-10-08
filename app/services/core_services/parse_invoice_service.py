from app.llms.open_ai_client import open_ai_client
from app.schemas.core_schemas import InvoiceDataSchema
from app.prompts import INVOICE_EXTRACTION_PROMPT

class ParseInvoiceService:
    def __init__(self):
        self.llm = open_ai_client.create_structured_output_parser_client(InvoiceDataSchema)
        self.chain = INVOICE_EXTRACTION_PROMPT | self.llm

    def parse(self, invoice_text: str):
        return self.chain.invoke({"invoice_text": invoice_text})

# singleton
parse_invoice_service = ParseInvoiceService()
