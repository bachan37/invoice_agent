from pydantic import BaseModel
class CreateRoleInputSchema(BaseModel):
    """Request schema for creating a role."""
    name: str
    description: str