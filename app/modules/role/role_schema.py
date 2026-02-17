from pydantic import BaseModel, Field
from datetime import datetime


class CreateRoleRequest(BaseModel):
    role: str = Field(..., min_length=3, max_length=50)
    description: str | None = Field(None, max_length=255)


class RoleResponse(BaseModel):
    id: int
    role: str
    description: str | None
    created_at: datetime
    updated_at: datetime
    

class RoleUpdateSchema(BaseModel):
    role: str | None = Field(None, min_length=3, max_length=50)
    description: str | None = Field(None, max_length=255)
    

