from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.schema import ApiResponse
from app.core.dependency import get_db, require_roles, get_current_user
from app.modules.auth.auth_controller import AuthController
from app.modules.auth.auth_schema import RegisterRequest, LoginRequest, RegisterResponse, LoginResponse, UserResponse

router = APIRouter(prefix= '/auth', tags= ['Authentication'])

@router.post('/register', response_model= ApiResponse[RegisterResponse], summary= "Register an User")
async def sign_up(data: RegisterRequest, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles('super_admin'))):
    return await AuthController.register(data, db, current_user)

@router.post('/login', response_model=ApiResponse[LoginResponse], summary= 'To Login The User')
async def sign_in(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await AuthController.login(data, db)

@router.get('/me', response_model= ApiResponse[UserResponse], summary= "Get Current User Details")
async def get_current_user(current_user = Depends(get_current_user)):
    return await AuthController.get_authenticated_user(current_user)