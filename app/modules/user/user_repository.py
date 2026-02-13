from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.modules.auth.auth_model import User

class UserRepository:
    @staticmethod
    async def _all_data(db):
        stmt = (select(User)
            .options(
                selectinload(User.role),
                selectinload(User.department)
            )
        )
        result = await db.execute(stmt)
        users = result.scalars().all()
        return users
    
    @staticmethod
    async def _update(update_data: dict, instance: any):
        for field, value in update_data.items():
            setattr(instance, field, value)
        
        return instance