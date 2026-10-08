from app.constants.app_constants import INVOICE_STATUS
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.utils.core_utils import utc_now
import json


class Invoice(BaseModel):
    """Invoice domain model."""
    model_config = ConfigDict(frozen=True)

    id: int
    thread_id: str
    filename: str
    file_path: Optional[str]
    status: INVOICE_STATUS = Field(default=INVOICE_STATUS.FETCHED)
    raw_data: Optional[str]
    extracted_data: Optional[Dict[str, Any]]
    reviewer_notes: Optional[str]
    reviewer_id: Optional[int]
    created_at: datetime = Field(default_factory=utc_now)
    created_by: Optional[int]
    updated_at: datetime = Field(default_factory=utc_now)
    updated_by: Optional[int]

    @field_validator("extracted_data", mode="before")
    @classmethod
    def parse_sqlite_json_str(cls, value: Any) -> Any:
        if isinstance(value, str):
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
        return value
