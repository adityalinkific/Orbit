from fastapi import HTTPException, status
from app.modules.user.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.user.user_schema import ChangePassword
from app.core.security import PasswordService
from app.modules.auth.auth_model import User

class UserServices:
    
    @staticmethod
    async def _all_users(db: AsyncSession):
        result = await UserRepository._all_data(db)
        return result
    
    @staticmethod
    async def _change_password(data: ChangePassword, db: AsyncSession, current_user: User):
        if not PasswordService._verify(data.current_password, current_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid current password"
            )
            
        hashed_password = PasswordService._hash(data.new_password)
        try:
            await UserRepository._update({"password": hashed_password}, current_user)
            await db.commit()
            return
        except Exception:
            await db.rollback()
            raise