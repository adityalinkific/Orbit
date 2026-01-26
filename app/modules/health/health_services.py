from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

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
                content={
                    "status": False,
                    "message": "Service unavailable",
                    "errors": errors
                }
            )
            
        return {
            "status": True,
            "message": "Database connected"
        }