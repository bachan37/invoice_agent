from app.config import logger
class EmailService:
    def send_rejection_email(self, reason: str):
        """ For now mocking it
        Sends the rejection email"""
        logger.info(f"Sends the rejection email with following details: reason={reason}")

email_service = EmailService()
        

