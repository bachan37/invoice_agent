import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Load and expose environment settings for the application."""

    def __init__(self) -> None:
        """Initialize settings from environment variables."""
        # 1. Project information
        self.ENV: str = os.getenv("ENV", "dev")
        self.PROJECT_NAME: str = os.getenv("PROJECT_NAME", "invoice_agent")
        self.PROJECT_VERSION: str = os.getenv("PROJECT_VERSION", "0.1.0")
        self.PROJECT_DESCRIPTION: str = os.getenv(
            "PROJECT_DESCRIPTION",
            "An agentic invoice processing application.",
        )

        # 2. API configuration
        self.ALLOWED_ORIGINS: list[str] = os.getenv("ALLOWED_ORIGINS", "").split(",")
        self.BASE_PATH: str = os.getenv("BASE_PATH", "")
        self.OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY", None)

        # 3. Authentication configuration
        self.JWT_SECRET_KEY: str = os.getenv(
            "JWT_SECRET_KEY", "invoice_agent_secret_key"
        )
        self.JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
        self.JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
            os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")
        )

        # Email Configuration
        self.IMAP_HOST: str = os.getenv("IMAP_HOST", "imap.gmail.com")
        self.IMAP_PORT: int = int(os.getenv("IMAP_PORT", "993"))
        self.IMAP_USERNAME: str = os.getenv("IMAP_USERNAME", "")
        self.IMAP_PASSWORD: str = os.getenv("IMAP_PASSWORD", "")

        # sender email configuration
        self.SENDER_EMAIL: str= os.getenv("SENDER_EMAIL", "")
        
        # System AI user configuration
        self.SYSTEM_AI_USERNAME: str | None = (
            os.getenv("SYSTEM_AI_USERNAME", "").strip() or None
        )
        self.SYSTEM_AI_EMAIL: str | None = os.getenv("SYSTEM_AI_EMAIL", "").strip() or None
        self.SYSTEM_AI_PASSWORD: str | None = (
            os.getenv("SYSTEM_AI_PASSWORD", "").strip() or None
        )

        # 5. Working directory
        working_dir = os.path.abspath(os.getenv("WORKING_DIR", ".").strip() or ".")

        self.WORKING_PROJECT_DIR: str = working_dir #os.path.join(working_dir, self.PROJECT_NAME)
        self.DB_PATH: str = os.path.join(working_dir, "sqlite_data", "app.db")
        self.LOG_DIR: str = os.path.join(self.WORKING_PROJECT_DIR, "logs")
        self.INVOICES_DIR: str = os.path.join(self.WORKING_PROJECT_DIR, "invoices")

        # DB Configuration
        self.USE_SQL: bool = os.getenv("USE_SQL", "false").lower() in ("1", "true", "yes")


        # Ensure required directories exist on app startup
        os.makedirs(os.path.dirname(self.DB_PATH), exist_ok=True)
        os.makedirs(self.LOG_DIR, exist_ok=True)
        os.makedirs(self.INVOICES_DIR, exist_ok=True)

# singleton pattern
settings = Settings()