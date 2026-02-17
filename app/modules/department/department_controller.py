from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.department.department_services import DepartmentService


class DepartmentController:

    @staticmethod
    async def _create_department(data, db: AsyncSession):
        department = await DepartmentService._create_department(data, db)

        return {
            "status": True,
            "message": "Department created successfully",
            "data": {
                "id": department.id,
                "name": department.name,
                "description": department.description,
                "created_at": department.created_at,
                "updated_at": department.updated_at
            }
        }

    @staticmethod
    async def _get_departments(db: AsyncSession):
        departments = await DepartmentService._get_departments(db)

        return {
            "status": True,
            "message": "Departments fetched successfully",
            "data": [
                {
                    "id": dept.id,
                    "name": dept.name,
                    "description": dept.description,
                    "created_at": dept.created_at,
                    "updated_at": dept.updated_at
                }
                for dept in departments
            ]
        }
        
        
        
    @staticmethod
    async def _get_perticular_department(department_id, db):
        dept = await DepartmentService._get_department(department_id, db)

        return {
            "status": True,
            "message": "Department fetched successfully",
            "data": {
                "id": dept.id,
                "name": dept.name,
                "description": dept.description,
                "created_at": dept.created_at,
                "updated_at": dept.updated_at
            }
        }
        
    
    @staticmethod
    async def _update_department(department_id, data, db):
        department_detail = await DepartmentService._update_department(department_id, data, db)
        return {
            'status' : True,
            'message' : 'Department updated successfully.',
            'data' : None
        }
        
    
    @staticmethod
    async def _delete_department(department_id, db):
        await DepartmentService._delete(department_id, db)
        return {
            'status' : True,
            'message' : 'Department deleted successfully.',
            'data' : None
        }
