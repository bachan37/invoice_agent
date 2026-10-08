from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.utils.core_utils import utc_now


class Role(BaseModel):
    """Role domain model for IAM."""
    model_config = ConfigDict(frozen=True)

    id: int
    name: str
    description: Optional[str]
    created_at: datetime = Field(default_factory=utc_now)
    created_by: Optional[int]
    updated_at: datetime = Field(default_factory=utc_now)
    updated_by: Optional[int]