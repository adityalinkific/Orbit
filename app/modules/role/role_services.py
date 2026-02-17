from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.modules.role.role_repository import RoleRepository, GetDetail, RecordExists
from app.modules.auth.auth_model import Role
from app.modules.role.role_schema import CreateRoleRequest, RoleUpdateSchema


class RoleService:

    @staticmethod
    async def _create_role(data: CreateRoleRequest, db: AsyncSession, current_user):

        if await RecordExists._check(db, Role.role == data.role):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Role already exists"
            )

        new_role = Role(
            role=data.role,
            description=data.description
        )
        try:
            new_role = await RoleRepository._create(db, new_role)
            await db.commit()
            await db.refresh(new_role)
            return new_role

        except Exception as e:
            await db.rollback()
            raise 
            
            
    @staticmethod
    async def _get_roles(db: AsyncSession):
        roles = await GetDetail._get_all(db, Role)
        return roles
    
    
    @staticmethod
    async def _get_role(role_id: int, db: AsyncSession):
        role_detail = await GetDetail._get_one(db, Role, Role.id == role_id)
        if not role_detail:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail= "Role not found."
            )
        return role_detail
    
    
    
    @staticmethod
    async def _update(role_id: int, data: RoleUpdateSchema, db: AsyncSession):
        role_detail = await GetDetail._get_one(db, Role, Role.id == role_id)
        
        if not role_detail:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail= "Role not found."
            )
        
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field is required for updating the role."
            )
        
        try:
            result = await RoleRepository._update(update_data, role_detail)
            await db.commit()
            await db.refresh(result)
            return result
        except Exception:
            await db.rollback()
            raise
    
    
    
    @staticmethod
    async def _delete(role_id: int, db: AsyncSession):
        role_detail = await GetDetail._get_one(db, Role, Role.id == role_id)        
        if not role_detail:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        try:
            await RoleRepository._delete(db, role_detail)
            await db.commit()
            return
        
        except Exception:
            await db.rollback()
            raise
