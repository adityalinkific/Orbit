from app.modules.auth.auth_model import User
from app.modules.auth.auth_services import AuthService


class AuthController:

    @staticmethod
    async def _register(data, db, current_user):
        user = await AuthService.register_user(data, db, current_user)
        print(user)
        return {
            "status": True,
            "message": "User registered successfully",
            "data": {
                "id": user.id,
                "emp_id": user.emp_id,
                "name": user.name,
                "email": user.email,
                "role_id": user.role_id,
                "department_id": user.department_id,
                "reporting_manager_id": user.reporting_manager_id
            }
        }
        
        
    @staticmethod
    async def _login(data, db):
        token = await AuthService.login_user(data, db)

        return {
            "status": True,
            "message": "Login successful",
            "data": {
                "access_token": token,
                "token_type": "Bearer"
            }
        }
        
    
    @staticmethod
    async def _get_authenticated_user(current_user):
        user = await AuthService.get_user_details(current_user)
        
        return {
            "status": True,
            "message": "Authenticated user's details fetched successfully",
            "data": {
                "id": user.id,
                "emp_id": user.emp_id,
                "name": user.name,
                "email": user.email,
                "role_id": user.role_id,
                "reporting_manager_id": user.reporting_manager_id,
                "department_id": user.department_id,
                "is_active": user.is_active,
                "logged_in": user.logged_in,
                "joined_date": user.joined_date,
                "role": {
                    "id": current_user.role.id,
                    "role": current_user.role.role,
                    "description": current_user.role.description,
                },
                "department": {
                    "id": current_user.department.id,
                    "department": current_user.department.name,
                    "description": current_user.department.description,
                },
                "created_at": user.created_at,
                "updated_at": user.updated_at
            }
        }


    @staticmethod
    async def _logout(db, current_user):
        await AuthService.logout_user(db, current_user)

        return {
            "status": True,
            "message": "Logout successfully",
            "data": None
        }

    @staticmethod
    async def _delete_user_account(id: int, db):
        await AuthService.delete_user(id, db)

        return {
            "status": True,
            "message": "User account deleted successfully",
            "data": None
        }