from fastapi import APIRouter
from app.modules.auth.auth_controller import Auth
from app.modules.auth.auth_schema import LoginRequest

router = APIRouter(prefix= '/auth', tags= ['Authentication'])

@router.post('/', summary= 'To Login The User')
async def sign_in(data: LoginRequest):
    return await Auth.login(data)