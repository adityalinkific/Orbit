from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.auth.auth_model import Role
from app.modules.role.role_schema import CreateRoleRequest
from app.modules.role.role_services import RoleService
from app.core.schema import Response

class RoleController:

    @staticmethod
    async def create_role(data: CreateRoleRequest, db: AsyncSession, current_user):

        role = await RoleService._create_role(data, db, current_user)
        data = {
            "id": role.id,
            "role": role.role,
            "description": role.description,
            "created_at": role.created_at,
            "updated_at": role.updated_at
        }
        return await Response._success_response("Role created successfully", data)

    @staticmethod
    async def get_roles(db: AsyncSession):
        roles = await RoleService._get_roles(db)
        data = [
            {
                "id": role.id,
                "role": role.role,
                "description": role.description,
                "created_at": role.created_at,
                "updated_at": role.updated_at
            }
            for role in roles
        ]
        return await Response._success_response("Roles fetched successfully", data)



    @staticmethod
    async def _get_perticular_role(role_id, db):
        role = await RoleService._get_role(role_id, db)
        data =  {
            "id": role.id,
            "role": role.role,
            "description": role.description,
            "created_at": role.created_at,
            "updated_at": role.updated_at
        }
        return await Response._success_response("Roles fetched successfully", data)
        
    
    @staticmethod
    async def _update_role(role_id, data, db):
        await RoleService._update(role_id, data, db)
        return await Response._success_response("Role updated successfully")
        
    
    @staticmethod
    async def _delete_role(role_id, db):
        await RoleService._delete(role_id, db)
        return await Response._success_response("Role deleted successfully")