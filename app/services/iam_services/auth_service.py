import sqlite3

from app.config.log_config import logger
from app.exceptions import InternalError, UnauthorizedError

from app.utils.iam_utils import JWT_utils, auth_utils
from app.repository.sql_repository.user_repository import UserRepository
from app.repository.sql_repository.role_repository import RoleRepository



class AuthService:
    """Authentication business logic."""

    def __init__(self, db: sqlite3.Connection) -> None:
        """Initialize AuthService with database connection.

        Args:
            db: Active SQLite connection.
        """
        self.db = db
        self.user_repo = UserRepository(db)
        self.role_repo = RoleRepository(db)
        

    def login(self, username: str, password: str) -> str:
        """Authenticate user and return JWT access token.

        Args:
            username: User's username.
            password: Plain text password.

        Returns:
            JWT access token string.

        Raises:
            UnauthorizedError: If credentials are invalid.
            InternalError: If database operations fail.
        """
        try:
            user = self.user_repo.get_user_by_username(username)
        except sqlite3.Error as e:
            logger.exception("Database error during login: %s", e)
            raise InternalError("Authentication failed") from e

        if not user or not auth_utils.verify_password(password, user.hashed_password):
            raise UnauthorizedError("Invalid credentials")

        try:
            roles = self.user_repo.get_roles_for_user(user.id)
            role_names = []
            for role in roles:
                role_names.append(role.name)

            return JWT_utils.create_access_token(user_id=user.id, roles=role_names)
        except sqlite3.Error as e:
            logger.exception("Database error during login: %s", e)
            raise InternalError("Authentication failed") from e
