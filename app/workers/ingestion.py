from typing import Any
from app.config.log_config import logger
from app.tools import fetch_email_invoices_tool
import uuid
from app.services.core_services import invoice_service
from app.constants import INVOICE_STATUS
from app.agents.graph import invoice_graph
from app.schemas.core_schemas import GraphState
import atexit

class IngestionWorker:
    def __init__(self):
        self.in_progress_threads = set()
        atexit.register(self.shutdown)

    def shutdown(self):
        pass

    def _index_file(self, file_path: str):
        """Indexes a single PDF by running it through the invoice graph."""
        filename = file_path.split("/")[-1]
        thread_id = f"inv-{uuid.uuid4()}"
        logger.debug("thread_id = %s", thread_id)
        config = {"configurable": {"thread_id": thread_id}}

        result = invoice_graph.invoke({"file_path": file_path, "filename": filename, "thread_id": thread_id}, config=config)

        return {
            "thread_id": thread_id,
            "invoice_id": result["invoice_id"],
            "status": result["status"]
        }

    def _run_ingestion_job(self):
        """Fetches all new email attachments and processes each file into its own graph thread."""
        logger.info("Starting email ingestion worker...")

        fetched_files = fetch_email_invoices_tool.invoke({})

        if not fetched_files:
            logger.info("No new invoice attachments found.")
            return

        logger.info("Found %d file(s) to process.", len(fetched_files))

        results = []
        for file_info in fetched_files:
            saved_path = file_info["file_path"]
            logger.info("Processing file: %s", saved_path)

            result = self._index_file(file_path=saved_path)
            results.append(result)
            logger.info("Successfully ingested \n\tinvoice ID=%s\n\t(thread_id=%s)\n\t(status=%s)", result["invoice_id"], result["thread_id"], result["status"])

    def run(self):
        self._run_ingestion_job()

ingestion_worker = IngestionWorker()
ingestion_worker.run()
        