from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.department.department_model import Department


class DepartmentRepository:

    @staticmethod
    async def get_by_name(db: AsyncSession, name: str):
        result = await db.execute(
            select(Department).where(Department.name == name)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, name: str, description: str | None):
        department = Department(name=name, description=description)
        db.add(department)
        return department

    @staticmethod
    async def fetch_all(db: AsyncSession):
        result = await db.execute(
            select(Department).order_by(Department.id.asc())
        )
        return result.scalars().all()
