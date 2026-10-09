from enum import Enum
from typing import Any, Dict, Optional, Set
from pydantic import BaseModel
from app.models import Base as BaseModelClass

class Action(str, Enum):
    # Standard CRUD
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    
    # Domain Actions
    REVIEW = "review"

class ResourceContext(BaseModel):
    resource: BaseModelClass
    owner_id: Optional[int] = None
    attributes: Dict[str, Any] = {} # extra attributes like status