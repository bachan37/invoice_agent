from xml.dom import NotFoundErr
from typing import Any, Dict, Optional, List
import sqlite3
from app.config import logger, settings
from app.models import Invoice
from app.repository.sql_repository.invoice_repository import InvoiceRepository
from app.utils.core_utils import sqlite_db
from app.constants import INVOICE_STATUS
from app.exceptions import NotFoundError, InternalError


class InvoiceService:
    def __init__(self, db: sqlite3.Connection) -> None:
        """Initialize AuthService with database connection.
        Args:
            db: Active SQLite connection.
        """
        self.db = db
        self.invoice_repository = InvoiceRepository(db)

    def create_record(self, thread_id: str, file_path: str, filename: str, status: str, created_by: Optional[int], **kwargs) -> Optional[Invoice]:
        """ uses repository to create records """
        invoice = self.invoice_repository.create_invoice(
            file_path=file_path,
            filename=filename,
            status=status,
            thread_id=thread_id,
            created_by=created_by,
        )
        if invoice:
            logger.info(f"Created invoice record: {invoice.id}")
            return invoice
        else:
            logger.error(f"Failed to create invoice record")
            return None

    def update_invoice(self, invoice_id: int, **kwargs: Any) -> Optional[Invoice]:
        """Generic update method that forwards all keyword arguments to the repository."""
        invoice = self.invoice_repository.update_invoice(invoice_id=invoice_id, **kwargs)
        if invoice:
            logger.info(f"Updated invoice record: {invoice.id}")
            return invoice
        else:
            logger.error(f"Failed to update invoice record")
            return None

    def list_invoices(self, status_filter: Optional[INVOICE_STATUS] = None) -> List[Invoice]:
        """List all invoices from the database."""
        if (status_filter is not None):
            return self.invoice_repository.list_invoices_with_filters(status_filter)

        return self.invoice_repository.list_invoices()

    def get_invoice(self, invoice_id: int) -> Optional[Invoice]:
        """Get an invoice by ID."""
        return self.invoice_repository.get_invoice_by_id(invoice_id)

    def get_invoice_by_thread_id(self, thread_id: str) -> Optional[Invoice]:
        """Get an invoice by thread ID."""
        return self.invoice_repository.get_invoice_by_thread_id(thread_id)

    def object() -> InvoiceService:
        """Singleton instance."""
        return InvoiceService(sqlite_db.connect())