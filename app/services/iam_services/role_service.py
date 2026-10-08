from app.schemas.core_schemas.role_schema import CreateRoleInputSchema
import sqlite3
from typing import Dict, List

from app.models.role_model import Role
from app.repository.sql_repository.role_repository import RoleRepository

class RoleService:
    def __init__(self, db: sqlite3.Connection) -> None:
        """Initialize AuthService with database connection.
        Args:
            db: Active SQLite connection.
        """
        self.db = db
        self.role_repository = RoleRepository(db)

    def get_or_create_role(self, role_input: CreateRoleInputSchema) -> Role:
        """Get or create a role.
        Args:
            role: Role to create or get.
        Returns:
            Role: Created or existing role.
        """
        role = self.role_repository.get_role_by_name(role_input.name)

        if role:
            return role

        role = self.role_repository.create_role(**role_input.model_dump())
        
    def get_all_roles(self) -> List[Role]:
        """Get all roles.
        Returns:
            List[Role]: List of all roles.
        """
        return self.role_repository.get_all()

    def get_role_by_name(self, role_name: str) -> Role:
        return self.role_repository.get_role_by_name(role_name)
    