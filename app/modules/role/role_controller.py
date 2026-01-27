from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.auth.auth_model import Role
from app.modules.role.role_schema import CreateRoleRequest
from app.modules.role.role_services import RoleService

class RoleController:

    @staticmethod
    async def create_role(data: CreateRoleRequest, db: AsyncSession):

        role = await RoleService.create_role(data, db)

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
        roles = await RoleService.get_roles(db)

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