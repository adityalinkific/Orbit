from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists, select
from app.modules.department.department_model import Department


class DepartmentRepository:

    @staticmethod
    async def _create(db: AsyncSession, data):
        db.add(data)
        return data
    
    
    @staticmethod
    async def _update(update_data: dict, instance: any):
        for field, value in update_data.items():
            setattr(instance, field, value)
        
        return instance
    
    @staticmethod
    async def _delete(db: AsyncSession, instance):
        return await db.delete(instance)
    

class RecordExists():

    @staticmethod
    async def _check(db: AsyncSession, *conditions) -> bool:
        stmt = select(exists().where(*conditions))
        result = await db.execute(stmt)
        return result.scalar()


class GetDetail:
    @staticmethod
    async def _get_all(db: AsyncSession, model, *conditions):
        stmt = select(model).order_by(model.id.desc())
        if conditions:
            stmt = stmt.where(*conditions)
        result = await db.execute(stmt)
        return result.scalars().all()
    
    @staticmethod
    async def _get_one(db: AsyncSession, model, *conditions):
        stmt = select(model).where(*conditions)
        result = await db.execute(stmt)
        return result.scalars().first()