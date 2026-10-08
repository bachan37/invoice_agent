from typing import Optional, List
from pydantic import BaseModel

class CreateUserInputSchema(BaseModel):
    username: str
    email: str
    password: str
    role_ids: List[int]
    created_by: Optional[int] = None