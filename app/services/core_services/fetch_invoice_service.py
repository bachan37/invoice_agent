# app/services/fetch_invoice_service.py
from app.utils.core_utils import utc_now_iso, email_utility
import os
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union

from app.config import logger, settings



class FetchInvoiceService:
    """Service to coordinate fetching email attachments and saving PDF invoices."""

    def __init__(self):
        self.email_utility = email_utility

    def execute(
        self,
        subject_keyword: Optional[str] = "invoice",
        sender_email: Optional[str] = settings.SENDER_EMAIL,
        since_date: Optional[Union[date, datetime]] = None,
        until_date: Optional[Union[date, datetime]] = None,
    ) -> List[Dict[str, Any]]:
        """Fetch emails matching criteria, filter for PDF attachments, and save to disk.

        Args:
            subject_keyword: Optional filter for email subject.
            sender_email: Optional filter for sender address.
            since_date: Optional start date filter.
            until_date: Optional end date filter.

        Returns:
            List[Dict[str, Any]]: List of metadata dicts for saved PDF files.
        """
        saved_invoices: List[Dict[str, Any]] = []

        # 1. Fetch raw messages via utility
        messages = self.email_utility.fetch_emails(
            subject_keyword=subject_keyword,
            sender_email=sender_email,
            since_date=since_date,
            until_date=until_date,
        )

        if not messages:
            logger.info("No matching emails found.")
            return saved_invoices

        # 2. Extract and store PDF attachments
        for item in messages:
            msg = item["raw_msg"]
            email_id = item["id"]

            for part in msg.walk():
                if part.get_content_maintype() == "multipart":
                    continue
                if part.get("Content-Disposition") is None:
                    continue

                filename = part.get_filename()
                if filename and filename.lower().endswith(".pdf"):
                    safe_filename = f"{subject_keyword}_{utc_now_iso()}_{filename}"
                    file_path = os.path.join(settings.INVOICES_DIR, safe_filename)

                    try:
                        payload = part.get_payload(decode=True)
                        if payload:
                            with open(file_path, "wb") as f:
                                f.write(payload)

                            logger.info("Saved invoice PDF to %s", file_path)
                            saved_invoices.append({
                                "filename": safe_filename,
                                "file_path": file_path
                            })
                    except Exception as e:
                        logger.exception("Failed to save attachment %s: %s", filename, e)

        return saved_invoices


# Module-level singleton instance for application/tool usage
fetch_invoice_service = FetchInvoiceService()