from pydantic import BaseModel, Field
from datetime import datetime


class CreateDepartmentRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: str = Field(None, max_length=255)
    department_head_id: int = Field(None)
    
    
class DepartmentCreateResponse(BaseModel):
    id: int
    name: str
    description: str | None
    department_head_id: int | None
    created_at: datetime
    updated_at: datetime


class DepartmentResponse(BaseModel):
    id: int
    name: str
    description: str | None
    department_head_id: int | None
    department_head_name: str | None
    total_members: int
    total_associated_projects: int
    created_at: datetime
    updated_at: datetime
    
class UpdateDepartmentRequest(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=50)
    description: str = Field(None, max_length=255)
    department_head_id: int | None = Field(None)