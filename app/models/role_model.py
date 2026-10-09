from typing import Optional
from app.models.base_model import Base

class Role(Base):
    """Role domain model for IAM."""
    name: str
    description: Optional[str]
    updated_by: Optional[int]