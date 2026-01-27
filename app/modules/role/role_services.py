from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.modules.role.role_repository import RoleRepository


class RoleService:

    @staticmethod
    async def create_role(data, db: AsyncSession):

        # 1️⃣ Duplicate role check
        existing_role = await RoleRepository.get_by_role_name(db, data.role)
        current_user = "super_admin"  # This should be fetched from the request context or session
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
        if current_user != "super_admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )

        if existing_role:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Role already exists"
            )

        try:
            # 2️⃣ Create role
            new_role = await RoleRepository.create(
                db=db,
                role=data.role,
                description=data.description
            )

            # 3️⃣ Commit transaction
            await db.commit()
            await db.refresh(new_role)

            return new_role

        except Exception as e:
            # 4️⃣ Rollback on failure
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create role"
            ) from e
            
            
    @staticmethod
    async def get_roles(db: AsyncSession):
        roles = await RoleRepository.fetch_all(db)
        return roles
