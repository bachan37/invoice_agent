from typing import Optional
from app.models.base_model import Base

class User(Base):
    """User domain model for IAM."""
    username: str
    email: Optional[str]
    hashed_password: str
    created_by: Optional[int]
    updated_by: Optional[int]