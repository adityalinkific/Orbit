from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.modules.auth.auth_model import User
from app.modules.department.department_schema import CreateDepartmentRequest, UpdateDepartmentRequest
from app.modules.department.department_model import Department
from app.modules.department.department_repository import DepartmentRepository, RecordExists, GetDetail


class DepartmentService:

    @staticmethod
    async def _create_department(data: CreateDepartmentRequest, db: AsyncSession):
        if await RecordExists._check(db, Department.name == data.name):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Department already exists"
            )
        if not await RecordExists._check(db, User.id == data.department_head_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Invalid department head selected."
            )
        new_department = Department(
            name = data.name,
            description = data.description,
            department_head_id = data.department_head_id
        )

        try:
            department = await DepartmentRepository._create(db, new_department)
            await db.commit()
            await db.refresh(department)
            return department

        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def _get_departments(db: AsyncSession):
        return await GetDetail._get_all(db, Department)
    
    
    @staticmethod
    async def _get_department(department_id, db):
        department_detail = await GetDetail._get_department_by_id(db, department_id)
        if not department_detail:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail= 'Department not found'
            )
        return department_detail
    
    
    
    @staticmethod
    async def _update_department(department_id: int, data: UpdateDepartmentRequest, db: AsyncSession):
        department_detail = await GetDetail._get_one(db, Department, Department.id == department_id)
        if not department_detail:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail= 'Department not found.'
            )
                
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field is required for updating the department."
            )
        
        try:
            result = await DepartmentRepository._update(update_data, department_detail)
            await db.commit()
            await db.refresh(result)
            return result
        except Exception:
            await db.rollback()
            raise
        
    
    @staticmethod
    async def _delete(department_id: int, db: AsyncSession):
        department_detail = await GetDetail._get_one(db, Department, Department.id == department_id)
        if not department_detail:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail= 'Department not found.'
            )
        
        try:
            await DepartmentRepository._delete(db, department_detail)
            await db.commit()
            return
        
        except Exception:
            await db.rollback()
            raise
        