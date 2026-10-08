from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.utils.core_utils import utc_now

class User(BaseModel):
    """User domain model for IAM."""
    model_config = ConfigDict(frozen=True)

    id: int
    username: str
    email: Optional[str]
    hashed_password: str
    created_at: datetime = Field(default_factory=utc_now)
    created_by: Optional[int]
    updated_at: datetime = Field(default_factory=utc_now)
    updated_by: Optional[int]