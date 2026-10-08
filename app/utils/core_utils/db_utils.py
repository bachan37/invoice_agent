import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Generator, Iterator, Optional

from app.config import settings, logger
from app.exceptions import InternalError

def utc_now() -> datetime:
    """Return the current UTC time.
    
    Returns:
        datetime: Current UTC time.
    """
    return datetime.now(timezone.utc)

def utc_now_iso() -> str:
    """Return the current UTC time as an ISO 8601 string.

    Returns:
        str: Timestamp in ISO format (e.g. ``2024-01-15T12:00:00+00:00``).
    """
    return utc_now().isoformat()

class SQLiteDatabase:
    """SQLite database manager with connection pooling and schema initialization."""

    def __init__(self, db_path: Optional[str] = None):
        """Initialize the database manager.

        Args:
            db_path: Optional path to the database file. Defaults to settings.DB_PATH.
        """
        self.db_path = db_path or settings.DB_PATH
        self._connection: Optional[sqlite3.Connection] = None

    def connect(self) -> sqlite3.Connection:
        """Create and return a new SQLite connection.

        Returns:
            sqlite3.Connection: Connection with ``row_factory`` set to ``sqlite3.Row``
            and foreign keys enabled.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys=ON;")
        return conn

    @contextmanager
    def get_connection(self) -> Iterator[sqlite3.Connection]:
        """Provide a database connection that closes when the context ends.

        Intended for ``with self.get_connection() as db:``; HTTP handlers typically
        depend on ``get_db`` instead.

        Yields:
            sqlite3.Connection: Open connection; closed in ``finally`` after the
                block completes or raises.
        """
        db = self.connect()
        try:
            yield db
        finally:
            db.close()

    def initialize_schema(self) -> None:
        """Create the application schema if tables are missing.

        Raises:
            InternalError: If connecting or creating tables fails.
        """
        try:
            db = self.connect()
        except sqlite3.Error as e:
            logger.exception("Database connection failed: %s", e)
            raise InternalError("Database initialization failed") from e

        try:
            self._create_users_table(db)
            self._create_roles_table(db)
            self._create_invoices_table(db)
            self._create_user_role_mapping_table(db)

            db.commit()
            logger.info("Database schema initialized successfully")

        except sqlite3.Error as e:
            logger.exception("Database schema creation failed: %s", e)
            raise InternalError("Database initialization failed") from e
        finally:
            db.close()

    def get_checkpointer_connection(self) -> sqlite3.Connection:
        """Create and return a thread-safe connection for LangGraph SqliteSaver.

        Sets check_same_thread=False to allow FastAPI request threads and 
        worker threads to query and checkpoint state across threads.

        Returns:
            sqlite3.Connection: Open SQLite connection configured for checkpointer.
        """
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys=ON;")
        return conn

    def _create_users_table(self, db: sqlite3.Connection) -> None:
        """Create the users table.

        Args:
            db: Active database connection.
        """
        query = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE,
                hashed_password TEXT NOT NULL,
                created_at DATETIME NOT NULL,
                created_by INTEGER,
                updated_at DATETIME,
                updated_by INTEGER
            )
        """
        db.execute(query)

    def _create_roles_table(self, db: sqlite3.Connection) -> None:
        """Create the roles table.

        Args:
            db: Active database connection.
        """
        query = """
            CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at DATETIME NOT NULL,
                created_by INTEGER,
                updated_at DATETIME,
                updated_by INTEGER
            )
        """
        db.execute(query)

    def _create_invoices_table(self, db: sqlite3.Connection) -> None:
        """Create the invoices table.

        Args:
            db: Active database connection.
        """
        query = """
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id TEXT UNIQUE NOT NULL,
                filename TEXT NOT NULL,
                file_path TEXT,
                status TEXT NOT NULL DEFAULT 'FETCHED',
                raw_data str,
                extracted_data TEXT,
                reviewer_notes TEXT,
                reviewer_id INTEGER,
                created_at DATETIME NOT NULL,
                created_by INTEGER,
                updated_at DATETIME,
                updated_by INTEGER,
                FOREIGN KEY (reviewer_id) REFERENCES users(id) ON DELETE SET NULL
            )
        """
        db.execute(query)

    def _create_user_role_mapping_table(self, db: sqlite3.Connection) -> None:
        """Create the user_role_mapping table.

        Args:
            db: Active database connection.
        """
        query = """
            CREATE TABLE IF NOT EXISTS user_role_mapping (
                user_id INTEGER NOT NULL,
                role_id INTEGER NOT NULL,
                PRIMARY KEY (user_id, role_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
            )
        """
        db.execute(query)


    def execute_query(
        self,
        query: str,
        params: tuple = (),
        fetch_one: bool = False,
        fetch_all: bool = False,
    ):
        """Run SQL on a short-lived connection (commit for writes).

        Args:
            query: SQL statement.
            params: Optional tuple of parameters bound to the query.
            fetch_one: If True, return one row (or None).
            fetch_all: If True, return all rows.

        Returns:
            sqlite3.Cursor: If neither ``fetch_one`` nor ``fetch_all`` is True,
                the cursor after ``commit()`` (for statements that do not fetch).
            sqlite3.Row or None: If ``fetch_one`` is True.
            list: If ``fetch_all`` is True.
        """
        with self.get_connection() as db:
            cursor = db.execute(query, params)
            if fetch_one:
                return cursor.fetchone()
            if fetch_all:
                return cursor.fetchall()
            db.commit()
            return cursor


sqlite_db = SQLiteDatabase()


def get_db() -> Generator[sqlite3.Connection, None, None]:
    """FastAPI dependency that yields one SQLite connection per HTTP request.

    The connection is closed after the response is sent.

    Yields:
        sqlite3.Connection: Request-scoped connection from ``sqlite_db``.
    """
    with sqlite_db.get_connection() as db:
        yield db


def init_db() -> None:
    """Ensure all application tables exist (compatibility wrapper).

    Delegates to ``SQLiteDatabase.initialize_schema``.
    """
    sqlite_db.initialize_schema()

def checkpointer_conn() -> sqlite3.Connection:
    return sqlite_db.get_checkpointer_connection()