from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.modules.auth.auth_model import User

class UserRepository:
    @staticmethod
    async def _update(update_data: dict, instance: any):
        for field, value in update_data.items():
            setattr(instance, field, value)
        
        return instance
    
class GetDetail:
    @staticmethod
    async def _all_data(db):
        stmt = (select(User)
            .order_by(User.id.desc())
            .options(
                selectinload(User.role),
                selectinload(User.department)
            )
        )
        result = await db.execute(stmt)
        users = result.scalars().all()
        return users
    
    @staticmethod
    async def _get_one(db: AsyncSession, model, *conditions):
        stmt = select(model).where(*conditions)
        result = await db.execute(stmt)
        return result.scalars().first()