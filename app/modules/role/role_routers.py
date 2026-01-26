from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.schema import ApiResponse
from app.core.dependency import get_db, require_roles
from app.modules.role.role_controller import RoleController
from app.modules.role.role_schema import CreateRoleRequest, RoleResponse

router = APIRouter(prefix= '/roles', tags= ['Roles'])

@router.post('/', response_model=ApiResponse[RoleResponse], summary= "Create a Role")
async def create_role(data: CreateRoleRequest, db: AsyncSession = Depends(get_db), _= Depends(require_roles("super_admin"))):
    return await RoleController.create_role(data, db)


@router.get('/', response_model=ApiResponse[list[RoleResponse]], summary= "Get All Roles")
async def get_role(db: AsyncSession = Depends(get_db)):
    return await RoleController.get_roles(db)