from pypdf import PdfReader
from app.config import logger

class PDFService:
    """Service to extract raw text from PDF files using pypdf."""

    def __init__(self):
        """Initialize PDFService."""
        pass

    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract raw text from a PDF file.

        Args:
            file_path: Path to the PDF file.

        Returns:
            str: Extracted text from the PDF file.
        """

        extracted_text = []

        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                text = page.extract_text()

                if text:
                    extracted_text.append(text)

            logger.info("Successfully extracted text from PDF: %s", file_path)
            return "\n".join(extracted_text).strip()
        except Exception as e:
            logger.exception("Failed to extract text from PDF: %s", file_path)
            raise RuntimeError(f"Error reading PDF file: {str(e)}") from e

# Singleton service instance
pdf_service = PDFService()