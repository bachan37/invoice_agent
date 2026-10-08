from app.repository.sql_repository.user_repository import UserRepository
from app.repository.sql_repository.role_repository import RoleRepository
from app.schemas.core_schemas.user_schema import CreateUserInputSchema
from app.exceptions import ConflictError
from app.utils.iam_utils import auth_utils

import sqlite3
class UserService:
    def __init__(self, db: sqlite3.Connection) -> None:
        """Initialize UserService with database connection.
        Args:
            db: Active SQLite connection.
        """
        self.db = db
        self.user_repository = UserRepository(db)
        self.role_repository = RoleRepository(db)

    def get_user_by_username(self, username: str):
        """Get user by username.
        Args:
            username: Username to search for.
        Returns:
            User domain model.
        """
        return self.user_repository.get_user_by_username(username)

    def create_user(
        self,
        create_user_input:CreateUserInputSchema
    ):
        """Create a new user with roles.
        Args:
            create_user_input: CreateUserInputSchema instance.
        Returns:
            User domain model.
        """
        existing_user = self.user_repository.get_user_by_username(create_user_input.username)
        if existing_user:
            raise ConflictError("Username already exists")
        
        hashed_password = auth_utils.hash_password(create_user_input.password)
        user = self.user_repository.create_user(
                username=create_user_input.username,
                email=create_user_input.email,
                hashed_password=hashed_password
            )

        default_role = self.role_repository.get_role_by_name("viewer")
        self.user_repository.add_role_to_user(user.id, default_role.id)

        for role_id in create_user_input.role_ids:
            self.user_repository.add_role_to_user(user.id, role_id)
        
        return user