from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.modules.department.department_repository import DepartmentRepository


class DepartmentService:

    @staticmethod
    async def create_department(data, db: AsyncSession):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
        
        existing = await DepartmentRepository.get_by_name(db, data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Department already exists"
            )

        try:
            department = await DepartmentRepository.create(
                db=db,
                name=data.name,
                description=data.description
            )
            await db.commit()
            await db.refresh(department)
            return department

        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def get_departments(db: AsyncSession):
        return await DepartmentRepository.fetch_all(db)
