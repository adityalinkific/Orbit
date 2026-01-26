from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependency import get_db
from app.modules.health.health_controller import Health

router = APIRouter(prefix= '/auth', tags= ['Health'])

@router.get("/health-check")
async def users(db: AsyncSession = Depends(get_db)):
    return await Health.health_check(db)