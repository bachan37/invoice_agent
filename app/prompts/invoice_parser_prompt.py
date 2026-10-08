from langchain_core.prompts import ChatPromptTemplate

INVOICE_EXTRACTION_PROMPT = ChatPromptTemplate(
    messages=[
        (
            "system",
            "You are an expert financial document processing assistant specializing in invoice analysis. "
            "Your task is to accurately extract key metadata, vendor details, itemized line items, subtotal, tax, "
            "and final amounts from the provided raw invoice text."
            "And if you find any date, please keep it in string yyyy-mm-dd format"
        ),
        (
            "user",
            "Extract all structured invoice details from the text below:\n\n"
            "--- START INVOICE TEXT ---\n"
            "{invoice_text}\n"
            "--- END INVOICE TEXT ---"
        ),
    ],
    input_variables=["invoice_text"]
)