import email
import imaplib
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union

from app.config import logger, settings


class EmailUtility:
    """Low-level IMAP wrapper to query emails and extract raw attachments."""

    def __init__(self):
        self.host = getattr(settings, "IMAP_HOST", "imap.gmail.com")
        self.port = getattr(settings, "IMAP_PORT", 993)
        self.username = getattr(settings, "IMAP_USERNAME", "")
        self.password = getattr(settings, "IMAP_PASSWORD", "")

    def fetch_emails(
        self,
        subject_keyword: Optional[str] = None,
        sender_email: Optional[str] = None,
        since_date: Optional[Union[date, datetime]] = None,
        until_date: Optional[Union[date, datetime]] = None,
    ) -> List[Dict[str, Any]]:
        """Fetch emails matching optional subject, sender, and date criteria.

        Args:
            subject_keyword: Optional string to filter subject lines.
            sender_email: Optional email address to filter senders.
            since_date: Optional start date filter (inclusive).
            until_date: Optional end date filter (inclusive).

        Returns:
            List[Dict[str, Any]]: List of dicts containing message metadata and raw message.
        """
        fetched_messages = []
        try:
            mail = imaplib.IMAP4_SSL(self.host, self.port)
            mail.login(self.username, self.password)
            mail.select("inbox")

            # Build dynamic search criteria list
            criteria = []

            if subject_keyword:
                criteria.append(f'SUBJECT "{subject_keyword}"')

            if sender_email:
                criteria.append(f'FROM "{sender_email}"')

            if since_date:
                formatted_since = since_date.strftime("%d-%b-%Y")
                criteria.append(f'SINCE "{formatted_since}"')

            if until_date:
                formatted_until = until_date.strftime("%d-%b-%Y")
                criteria.append(f'BEFORE "{formatted_until}"')

            # Default to "ALL" if no criteria specified
            search_query = " ".join(criteria) if criteria else "ALL"

            status, response = mail.search(None, search_query)
            if status != "OK":
                logger.warning("IMAP search failed with criteria: %s", search_query)
                return fetched_messages

            email_ids = response[0].split()
            for e_id in email_ids:
                res, msg_data = mail.fetch(e_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        fetched_messages.append({
                            "id": e_id.decode(),
                            "raw_msg": msg
                        })

            mail.logout()
            logger.info("Successfully fetched %d emails matching query.", len(fetched_messages))

        except Exception as e:
            logger.exception("Failed to fetch emails via IMAP: %s", e)

        return fetched_messages

email_utility = EmailUtility()