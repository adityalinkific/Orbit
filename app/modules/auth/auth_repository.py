from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from sqlalchemy.orm import selectinload
from app.modules.auth.auth_model import User


class AuthRepository:

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str):
        stmt = (
            select(User)
            .options(
                selectinload(User.role),
                selectinload(User.department)
            )
            .where(User.email == email)
        )
        result = await db.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def create_user(db: AsyncSession, user: User):
        db.add(user)
        return user
    
    
class DetailsExist():

    @staticmethod
    async def exists(db: AsyncSession, field, value) -> bool:
        stmt = select(exists().where(field == value))
        result = await db.execute(stmt)
        return result.scalar()

class GetDetails():
    @staticmethod
    async def get_by_id(db: AsyncSession, model, field_name, value):
        stmt = select(model).where(field_name == value)
        result = await db.execute(stmt)
        return result.scalars().first()
