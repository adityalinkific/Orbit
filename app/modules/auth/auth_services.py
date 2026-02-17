from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.auth.auth_repository import AuthRepository, RecordExists, GetRecord, DeleteUser
from app.modules.auth.auth_model import User, Role
from app.modules.department.department_model import Department
from app.core.security import PasswordService, TokenService
from app.modules.auth.auth_schema import RegisterRequest, LoginRequest
import uuid


class AuthService:

    @staticmethod
    async def register_user(data: RegisterRequest, db: AsyncSession, current_user):
        
        if await RecordExists._check(db, User.email == data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )

        # role = await GetDetails.get_by_id(db, Role, Role.id, data.role_id)
        role = await GetRecord._get_one(db, Role, Role.id == data.role_id)

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
            
        # if not await DetailsExist.exists(db, Department.id, data.department_id):
        if not await RecordExists._check(db, Department.id == data.department_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail= 'Invalid department selected'
            )
        
        if data.reporting_manager_id:

            # reporting_manager = await GetDetails.get_by_id(db, User, User.id, data.reporting_manager_id)
            reporting_manager = await GetRecord._get_one(db, User, User.id == data.reporting_manager_id)
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

        hashed_password = PasswordService._hash(data.password)

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
            await AuthRepository._create_user(db, user)
            await db.commit()
            await db.refresh(user)
            return user

        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def login_user(data: LoginRequest, db: AsyncSession):
        # user = await GetDetails.get_by_id(db, User, User.email, data.email)
        user = await GetRecord._get_one(db, User, User.email == data.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email"
            )

        if not PasswordService._verify(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are blocked. Please contact admin."
            )

        try:
            token = TokenService._create_access_token({
                "sub": user.email,
                "id": user.id,
                "role": user.role.role,
            })

            user.logged_in = True
            await db.commit()

            return token
        
        except Exception:
            await db.rollback()
            raise


    @staticmethod
    async def get_user_details(current_user):
        return current_user
    

    @staticmethod
    async def logout_user(db: AsyncSession, current_user: User):
        try:
            await AuthRepository._update({"logged_in" : False}, current_user)
            await db.commit()
        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def delete_user(id: int, db: AsyncSession):
        user = await GetRecord._get_one(db, User, User.id == id)        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        try:
            await DeleteUser._delete_user(db, user)
            await db.commit()
            return
        
        except Exception:
            await db.rollback()
            raise
        

class RecordChecking:
    @staticmethod
    async def _check(db: AsyncSession, field, id: int, message: str):
        if not await RecordExists._check(message, field == id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail= f"Invalid {message} selected."
            )

class GetDetails:
    @staticmethod
    async def _get_details(db: AsyncSession, model, id: int, message: str):
        result = await GetRecord._get_one(db, model, model.id == id)
        if not result:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail= f"{message.upper()} not found."
            )
        return result