from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.department.department_services import DepartmentService
from app.core.schema import Response


class DepartmentController:

    @staticmethod
    async def _create_department(data, db: AsyncSession):
        department = await DepartmentService._create_department(data, db)
        data = {
            "id": department.id,
            "name": department.name,
            "description": department.description,
            "created_at": department.created_at,
            "updated_at": department.updated_at
        }

        return await Response._success_response("Department created successfully", data)

    @staticmethod
    async def _get_departments(db: AsyncSession):
        departments = await DepartmentService._get_departments(db)
        data = [
            {
                "id": dept.id,
                "name": dept.name,
                "description": dept.description,
                "created_at": dept.created_at,
                "updated_at": dept.updated_at
            }
            for dept in departments
        ]

        return await Response._success_response("Departments fetched successfully", data)
        
        
        
    @staticmethod
    async def _get_perticular_department(department_id, db):
        dept = await DepartmentService._get_department(department_id, db)
        data = {
            "id": dept.id,
            "name": dept.name,
            "description": dept.description,
            "created_at": dept.created_at,
            "updated_at": dept.updated_at
        }

        return await Response._success_response("Department fetched successfully", data)
        
    
    @staticmethod
    async def _update_department(department_id, data, db):
        await DepartmentService._update_department(department_id, data, db)
        return await Response._success_response('Department updated successfully.')
        
    
    @staticmethod
    async def _delete_department(department_id, db):
        await DepartmentService._delete(department_id, db)
        return await Response._success_response('Department deleted successfully.')
