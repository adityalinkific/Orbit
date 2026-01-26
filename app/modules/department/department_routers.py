from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependency import get_db, require_roles
from app.core.schema import ApiResponse
from app.modules.department.department_schema import CreateDepartmentRequest, DepartmentResponse
from app.modules.department.department_controller import DepartmentController

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.post("/", response_model= ApiResponse[DepartmentResponse], summary= "Create Department")
async def create_department(data: CreateDepartmentRequest, db: AsyncSession = Depends(get_db), _= Depends(require_roles("super_admin"))):
    return await DepartmentController.create_department(data, db)


@router.get("/", response_model= ApiResponse[list[DepartmentResponse]], summary= "Get All Departments")
async def get_departments(db: AsyncSession = Depends(get_db)):
    return await DepartmentController.get_departments(db)
