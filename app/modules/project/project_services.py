from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.modules.department.department_model import Department
from app.modules.project.project_model import Project
from app.modules.project.project_schema import ProjectRequestSchema, ProjectUpdateSchema
from app.modules.project.project_repository import ProjectRepository, DetailsExist, GetProjects

class ProjectService:

    @staticmethod
    async def create_project(db: AsyncSession, data: ProjectRequestSchema, current_user):
        
        project_exists = await DetailsExist._exists(db, Project.name, data.name)
        if project_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project with this name already exists"
            )
        
        department_exists = await DetailsExist._exists(db, Department.id, data.department_id)
        if not department_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid department selected"
            )
        
        project_data = Project(
            name=data.name,
            description=data.description,
            department_id=data.department_id,
        )
        try:
            project = await ProjectRepository._create(db, project_data)
            await db.commit()
            await db.refresh(project)
            return project
        except Exception:
            db.rollback()
            raise

    @staticmethod
    async def update_project(db: AsyncSession, project_id: int, data: ProjectUpdateSchema):
        if not data.model_dump(exclude_unset=True):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field is required for updating the project."
            )
            
        if not await DetailsExist._exists(db, Department.id, data.department_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid department selected"
            )

        project = await GetProjects._get_by_id(db, project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
            
        update_data = data.model_dump(exclude_unset=True)
        
        try:
            project = await ProjectRepository._update(db, update_data, project)
            await db.commit()
            await db.refresh(project)
            return project
        except Exception:
            db.rollback()
            raise

    @staticmethod
    async def delete_project(db: AsyncSession, project_id: int):
        project = await GetProjects._get_by_id(db, project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )

        try:
            await ProjectRepository._delete(db, project)
            await db.commit()
            return
        except Exception:
            db.rollback()
            raise

    @staticmethod
    async def get_all_projects(db: AsyncSession):
        all_projects = await GetProjects._get_all(db)
        return all_projects
    
    
    @staticmethod
    async def get_project_by_id(db: AsyncSession, project_id: int):
        project = await GetProjects._get_by_id(db, project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )

        return project  