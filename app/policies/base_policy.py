from app.utils.iam_utils.auth_deps import TokenPayload
from app.policies.core.types import ResourceContext
from abc import ABC, abstractmethod
from app.models import User
from app.policies.core.types import Action
from typing import Optional
import sqlite3


class BasePolicy(ABC):
    """Abstract Base Class for all policies."""

    def __init__(self, db: sqlite3.Connection, payload: TokenPayload, resource_context: ResourceContext):
        self.db = db
        self.user_id = payload.user_id
        self.role_names = payload.roles
        self.resource_context = resource_context

    @abstractmethod
    def can_perform(self, action: Action) -> bool:
        """Check if the user has permission to perform the action.
        Args:
            action: The action to check permissions for.
        Returns:
            True if the user has permission to perform the action, False otherwise.
        """
        pass
