from pydantic import ConfigDict
from pydantic import BaseModel, Field
from datetime import datetime
from app.utils.core_utils import utc_now

class Base(BaseModel):
    """Base domain abstract model."""
    model_config = ConfigDict(frozen=True)

    id: int
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

