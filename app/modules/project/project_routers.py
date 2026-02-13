from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependency import get_db, get_current_user, require_roles
from app.core.schema import ApiResponse
from app.modules.project.project_controller import ProjectController
from app.modules.project.project_schema import ProjectRequestSchema, ProjectUpdateSchema, ProjectResponseSchema

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model= ApiResponse[None], summary= "Create Project")
async def create_project(data: ProjectRequestSchema,  db: AsyncSession = Depends(get_db),  current_user=Depends(require_roles("super_admin", "admin"))):
    return await ProjectController.create_project(db, data, current_user)

@router.put("/update-project/{project_id}", response_model= ApiResponse[None], summary= "Update Project")
async def update_project(project_id: int,  data: ProjectUpdateSchema,  db: AsyncSession = Depends(get_db),  current_user=Depends(require_roles("super_admin", "admin"))):
    return await ProjectController.update_project(db, project_id, data)

@router.delete("/delete-project/{project_id}", response_model= ApiResponse[None], summary= "Delete Project")
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(require_roles("super_admin", "admin"))):
    return await ProjectController.delete_project(db, project_id)

@router.get("/project-detail", response_model= ApiResponse[list[ProjectResponseSchema]], summary= "Get Project Detail")
async def get_project_detail(db: AsyncSession = Depends(get_db), current_user=Depends(require_roles("super_admin", "admin"))):
    return await ProjectController.get_all_project_detail(db)

@router.get("/project-detail/{project_id}", response_model= ApiResponse[ProjectResponseSchema], summary= "Get Project Detail")
async def get_project_detail(project_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await ProjectController.get_project_detail(db, project_id, current_user)