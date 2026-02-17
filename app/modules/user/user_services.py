from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.user.user_repository import UserRepository, GetDetail
from app.modules.user.user_schema import ChangePassword, UpdateUserDetailsRequest
from app.core.security import PasswordService
from app.modules.auth.auth_model import User, Role
from app.modules.auth.auth_services import RecordChecking, GetDetails
from app.modules.department.department_model import Department

class UserServices:
    
    @staticmethod
    async def _all_users(db: AsyncSession):
        result = await GetDetail._all_data(db)
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
        
    async def _update_user(user_id: int, data: UpdateUserDetailsRequest, db: AsyncSession):
        user_detail = GetDetails._get_details(db, User, user_id, "user")
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field is required for updating the task."
            )
        
        RecordChecking._check(db, Department.id, data.department_id, "department")
        RecordChecking._check(db, Role.id, data.role_id, 'role')
        if data.reporting_manager_id:
            RecordChecking._check(db, User.id, data.reporting_manager_id, 'reporting manager')
        print(update_data)
        print('password is :', update_data.password)
        update_data.password = PasswordService._hash(data.password)
        print('hashing password : ', update_data.password)
            
        try:
            result = await UserRepository._update(update_data, user_detail)
            await db.commit()
            await db.refresh(result)
            return result
        except Exception:
            await db.rollback()
            raise