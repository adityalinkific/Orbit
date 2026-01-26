from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.department.department_services import DepartmentService


class DepartmentController:

    @staticmethod
    async def create_department(data, db: AsyncSession):
        department = await DepartmentService.create_department(data, db)

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
    async def get_departments(db: AsyncSession):
        departments = await DepartmentService.get_departments(db)

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
