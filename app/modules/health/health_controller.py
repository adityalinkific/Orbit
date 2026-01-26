from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.health.health_services import HealthServices

class Health():

    @staticmethod
    async def health_check(db: AsyncSession):
        return await HealthServices.health_check(db)
        
