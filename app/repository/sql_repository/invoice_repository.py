from app.constants import INVOICE_STATUS
from app.utils.core_utils import utc_now
import sqlite3
from typing import List, Optional, Dict, Any
from app.models import Invoice
from app.repository.sql_repository.base_repository import BaseRepository

class InvoiceRepository(BaseRepository[Invoice]):
    """Data access for invoices."""

    def __init__(self, db: sqlite3.Connection) -> None:
        """Initialize with database connection and invoices table."""
        super().__init__(db, "invoices", Invoice)

    def create_invoice(
        self,
        thread_id: str,
        filename: str,
        file_path: str,
        status: INVOICE_STATUS = INVOICE_STATUS.FETCHED,
        raw_data: Optional[str] = None,
        extracted_data: Optional[Dict[str, Any]] = None,
        reviewer_notes: Optional[str] = None,
        reviewer_id: Optional[int] = None,
        created_by: Optional[int] = None,
    ) -> Invoice:
        """Create a new invoice.

        Args:
            thread_id: Unique identifier for the invoice thread.
            filename: Name of the invoice file.
            file_path: Path to the invoice file.
            status: Status of the invoice (default: FETCHED).
        Returns:
            Created Invoice instance.
        """
        return self.create(
            thread_id=thread_id,
            filename=filename,
            file_path=file_path,
            status=status
        )

    def get_invoice_by_id(self, invoice_id: int) -> Optional[Invoice]:
        """Get an invoice by ID.

        Args:
            invoice_id: Invoice identifier.

        Returns:
            Invoice instance or None.
        """
        return self.get_by_id(invoice_id)

    def get_invoice_by_thread_id(self, thread_id: str) -> Optional[Invoice]:
        """Get an invoice by thread ID.

        Args:
            thread_id: Invoice thread identifier.

        Returns:
            Invoice instance or None.
        """
        return self.get_by_field("thread_id", thread_id)

    def list_invoices(self) -> List[Invoice]:
        """List all invoices.

        Returns:
            List of Invoice instances.
        """
        return self.list_all()

    def list_invoices_with_filters(self, status_filter: Optional[INVOICE_STATUS] = None) -> List[Invoice]:
        """List invoices with optional status filter.
        
        Args:
            status_filter: Optional status to filter invoices by.
            
        Returns:
            List of Invoice instances.
        """
        query = "SELECT * FROM invoices WHERE true"
        params = []
        if status_filter:
            query += " AND status = ?"
            params.append(status_filter.value)
        
        rows = self.db.execute(query, params).fetchall()
        return self._rows_to_models(rows)

    def update_invoice(
        self,
        invoice_id: int,
        thread_id: Optional[str] = None,
        filename: Optional[str] = None,
        file_path: Optional[str] = None,
        status: Optional[INVOICE_STATUS] = None,
        raw_data: Optional[str] = None,
        extracted_data: Optional[Dict[str, Any]] = None,
        reviewer_notes: Optional[str] = None,
        reviewer_id: Optional[int] = None,
        updated_by: Optional[int] = None,
    ) -> Optional[Invoice]:
        """Update an invoice.

        Args:
            invoice_id: Invoice identifier.
            thread_id: Optional new thread ID.
            filename: Optional new filename.
            file_path: Optional new file path.
            status: Optional new status.
            raw_data: Optional new raw data.
            extracted_data: Optional new extracted data in stringify json.
            reviewer_notes: Optional new reviewer notes.
            reviewer_id: Optional new reviewer ID.
            updated_by: Optional user ID of updater.

        Returns:
            Updated Invoice instance or None if not found.
        """
        return self.update(
            invoice_id,
            updated_by=updated_by,
            thread_id=thread_id,
            filename=filename,
            file_path=file_path,
            status=status,
            raw_data=raw_data,
            extracted_data=extracted_data,
            reviewer_notes=reviewer_notes,
            reviewer_id=reviewer_id,
            updated_at=utc_now()
        )

    def delete_invoice(self, invoice_id: int) -> Optional[Invoice]:
        """Delete an invoice.

        Args:
            invoice_id: Invoice identifier.

        Returns:
            Deleted Invoice instance or None if not found.
        """
        return self.delete(invoice_id)