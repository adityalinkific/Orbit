from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.auth.auth_repository import AuthRepository, DetailsExist, GetDetails
from app.modules.auth.auth_model import User, Role
from app.modules.department.department_model import Department
from app.core.security import PasswordService, TokenService
from app.modules.auth.auth_schema import RegisterRequest, LoginRequest
import uuid


class AuthService:

    @staticmethod
    async def register_user(data: RegisterRequest, db: AsyncSession, current_user):
        
        if await DetailsExist.exists(db, User.email, data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )

        role = await GetDetails.get_by_id(db, Role, Role.id, data.role_id)

        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail= 'Invalid role selected'
            )
            
        if role.role.lower() == 'super_admin':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail= 'Cannot assign Super Admin role'
            )
            
        if not await DetailsExist.exists(db, Department.id, data.department_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail= 'Invalid department selected'
            )
        
        if data.reporting_manager_id:
            
            if data.reporting_manager_id == current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail= 'You cannot assign yourself as reporting manager'
                )

            reporting_manager = await GetDetails.get_by_id(db, User, User.id, data.reporting_manager_id)
            if not reporting_manager:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail= 'Invalid reporting manager selected'
                )
            if reporting_manager.is_active is False:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail= 'Reporting manager is blocked'
                )             

        hashed_password = PasswordService.hash(data.password)

        user = User(
            emp_id=f"LF-{uuid.uuid4().hex[:6].upper()}",
            name=data.name,
            email=data.email,
            password=hashed_password,
            role_id=data.role_id,
            reporting_manager_id=data.reporting_manager_id,
            department_id=data.department_id,
            is_active=data.is_active,
            joined_date=data.joined_date,
        )

        try:
            await AuthRepository.create_user(db, user)
            await db.commit()
            await db.refresh(user)
            return user

        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def login_user(data: LoginRequest, db: AsyncSession):
        user = await GetDetails.get_by_id(db, User, User.email, data.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email"
            )

        if not PasswordService.verify(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are blocked. Please contact admin."
            )

        token = TokenService.create_access_token({
            "sub": user.email,
            "id": user.id,
            "role": user.role.role,
        })

        user.logged_in = True
        await db.commit()

        return token


    @staticmethod
    async def get_user_details(current_user):
        return current_user