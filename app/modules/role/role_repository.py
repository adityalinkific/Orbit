from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.auth.auth_model import Role


class RoleRepository:

    @staticmethod
    async def get_by_role_name(db: AsyncSession, role: str):
        result = await db.execute(
            select(Role).where(Role.role == role)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, role: str, description: str):
        new_role = Role(role=role, description=description)
        db.add(new_role)
        return new_role
    
    
    async def fetch_all(db: AsyncSession):
        result = await db.execute(
            select(Role).order_by(Role.id.asc())
        )
        return result.scalars().all()
