from app.modules.auth.auth_schema import LoginRequest

class Auth():
    async def login(data: LoginRequest):
        return {
            'status' : True,
            'message' : 'Login successfully',
            'data' : data.email
        }