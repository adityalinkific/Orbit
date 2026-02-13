from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists, select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError

from app.modules.task.task_model import Task, TaskAssignment, Report, ReportAttachment, ReportReview, TaskStatusEnum


class TaskRepository:

    @staticmethod
    async def create(db: AsyncSession, task: Task):
        db.add(task)
        return task

    @staticmethod
    async def update(update_data: dict, instance: any):
        for field, value in update_data.items():
            setattr(instance, field, value)
        
        return instance

    @staticmethod
    async def delete(db: AsyncSession, instance: any):
        await db.delete(instance)
        return
    
    
class RecordExists():

    @staticmethod
    async def check(db: AsyncSession, *conditions) -> bool:
        stmt = select(exists().where(*conditions))
        result = await db.execute(stmt)
        return result.scalar()
        
        
class TaskDetails:
    @staticmethod
    async def get_by_id(db: AsyncSession, id: int):
        stmt = select(Task).where(Task.id == id)
        result = await db.execute(stmt)
        return result.scalars().first()
    
    @staticmethod
    async def get_one(db: AsyncSession, model, *conditions):
        stmt = select(model).where(*conditions)
        result = await db.execute(stmt)
        return result.scalars().first()
    
    @staticmethod
    async def get_all(db: AsyncSession, model, *conditions):
        stmt = select(model).order_by(model.id.desc())
        if conditions:
            stmt = stmt.where(*conditions)
        result = await db.execute(stmt)
        return result.scalars().all()
    
    @staticmethod
    async def get_by_task_id(db: AsyncSession, task_id: str):
        stmt = select(Task).where(Task.task_id == task_id)
        result = await db.execute(stmt)
        return result.scalars().first()
    
    @staticmethod
    async def get_assignment(db, assign_task_id):
        stmt = (
            select(TaskAssignment)
            .where(TaskAssignment.id == assign_task_id)
            .options(
                joinedload(TaskAssignment.task),
                joinedload(TaskAssignment.report)
            )
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

class TaskAssignmentRepository:
    
    @staticmethod
    async def create(db: AsyncSession, task_assignment):
        db.add(task_assignment)
        return task_assignment
    

# class ReportRepository:

#     @staticmethod
#     async def submit_report(db, report: Report):
#         db.add(report)
#         await db.commit()
#         await db.refresh(report)
#         return report

#     @staticmethod
#     async def get_submitted_tasks(db, user_id=None):
#         stmt = (
#             select(TaskAssignment)
#             .join(TaskAssignment.report)
#             .options(
#                 joinedload(TaskAssignment.task),
#                 joinedload(TaskAssignment.report)
#             )
#             .where(TaskAssignment.status == TaskStatusEnum.submitted)
#         )

#         if user_id:
#             stmt = stmt.where(TaskAssignment.user_id == user_id)

#         result = await db.execute(stmt)
#         return result.scalars().all()

#     @staticmethod
#     async def get_pending_reviews(db):
#         stmt = (
#             select(TaskAssignment)
#             .join(TaskAssignment.report)
#             .outerjoin(TaskAssignment.review)
#             .where(
#                 TaskAssignment.status == TaskStatusEnum.submitted,
#                 ReportReview.id.is_(None)
#             )
#             .options(
#                 joinedload(TaskAssignment.task),
#                 joinedload(TaskAssignment.report)
#             )
#         )
#         result = await db.execute(stmt)
#         return result.scalars().all()
