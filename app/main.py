"""FastAPI application entry point."""
import argparse
from app.config import settings
from app.starter import start_application
from app.config import setup_logging
import uvicorn


def run_api():
    logger = setup_logging(service_name="api")
    logger.info("Initializing API application...")
    app = start_application()

    # Run uvicorn server programmatically
    uvicorn.run(app, host=settings.HOST_IP, port=settings.HOST_PORT)

def run_ingestion():
    """Starts the background Ingestion Worker process."""
    logger = setup_logging(service_name="ingestion")
    logger.info("Initializing Ingestion Worker...")

    from app.workers.ingestion import IngestionWorker
    worker = IngestionWorker()
    worker.run()

def main():
    parser = argparse.ArgumentParser(description="Invoice Agent Application Runner")
    parser.add_argument(
        "--mode",
        type=str,
        choices=["api", "ingestion"],
        default="api",
        help="Mode to run the application in: 'api' (FastAPI web server), 'ingestion' (background worker). Default is 'api'.",
    )

    args = parser.parse_args()

    if args.mode == "api":
        run_api()
    elif args.mode == "ingestion":
        run_ingestion()

if __name__ == "__main__":
    main()