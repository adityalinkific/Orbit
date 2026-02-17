from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.auth.auth_model import Role
from app.modules.role.role_schema import CreateRoleRequest
from app.modules.role.role_services import RoleService

class RoleController:

    @staticmethod
    async def create_role(data: CreateRoleRequest, db: AsyncSession, current_user):

        role = await RoleService._create_role(data, db, current_user)

        return {
            "status": True,
            "message": "Role created successfully",
            "data": {
                "id": role.id,
                "role": role.role,
                "description": role.description,
                "created_at": role.created_at,
                "updated_at": role.updated_at
            }
        }

    @staticmethod
    async def get_roles(db: AsyncSession):
        roles = await RoleService._get_roles(db)

        return {
            "status": True,
            "message": "Roles fetched successfully",
            "data": [
                {
                    "id": role.id,
                    "role": role.role,
                    "description": role.description,
                    "created_at": role.created_at,
                    "updated_at": role.updated_at
                }
                for role in roles
            ]
        }



    @staticmethod
    async def _get_perticular_role(role_id, db):
        role = await RoleService._get_role(role_id, db)

        return {
            "status": True,
            "message": "Roles fetched successfully",
            "data":  {
                "id": role.id,
                "role": role.role,
                "description": role.description,
                "created_at": role.created_at,
                "updated_at": role.updated_at
            }
        }
        
    
    @staticmethod
    async def _update_role(role_id, data, db):
        role = await RoleService._update(role_id, data, db)

        return {
            "status": True,
            "message": "Role updated successfully",
            "data": None
        }
        
    
    @staticmethod
    async def _delete_role(role_id, db):
        role = await RoleService._delete(role_id, db)

        return {
            "status": True,
            "message": "Role deleted successfully",
            "data": None
        }