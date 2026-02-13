from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.project.project_services import ProjectService


class ProjectController:
    
    @staticmethod
    async def create_project(db: AsyncSession, data, current_user):
        await ProjectService.create_project(db, data, current_user)
        return {
            'status': True,
            'message': "Project created successfully",
            'data': None
        }
        
    @staticmethod
    async def update_project(db: AsyncSession, project_id: str, data):
        await ProjectService.update_project(db, project_id, data)
        return {
            'status': True,
            'message': "Project updated successfully",
            'data': None
        }
        
    @staticmethod
    async def delete_project(db: AsyncSession, project_id: str):
        await ProjectService.delete_project(db, project_id)
        return {
            'status': True,
            'message': "Project deleted successfully",
            'data': None
        }
        
        
    @staticmethod
    async def get_all_project_detail(db: AsyncSession):
        projects = await ProjectService.get_all_projects(db)
        return {
            'status' : True,
            'message' : "Project details fetched successfully",
            'data' : [
                {
                    'id': project.id,
                    'name': project.name,
                    'description': project.description,
                    'department_id': project.department_id,
                    'created_at': project.created_at,
                    'updated_at': project.updated_at
                } for project in projects
            ]
        }
        
    @staticmethod
    async def get_project_detail(db: AsyncSession, project_id: int, current_user):
        project = await ProjectService.get_project_by_id(db, project_id)
        return {
            'status' : True,
            'message' : "Project details fetched successfully",
            'data' : {
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'department_id': project.department_id,
                'created_at': project.created_at,
                'updated_at': project.updated_at
            }
        }