from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.schema import Response

class HealthServices():
    async def health_check(db: AsyncSession):
        errors = []

        try:
            await db.execute(text("SELECT 1"))
        except Exception as e:
            errors.append(f"Database error: {str(e)}")

        if errors:
            return JSONResponse(
                status_code=503,
                content= await Response._error_response("Service unavailable", errors)
            )
            
        return await Response._success_response("Database connected")