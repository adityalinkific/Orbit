from sqlalchemy import Column, String, Integer, Text, Date, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class TaskTypeEnum(str, enum.Enum):
    daily = "daily"
    weekly = "weekly"


class TaskStatusEnum(str, enum.Enum):
    assigned = "assigned"
    in_progress = "in_progress"
    submitted = "submitted"
    reviewed = "reviewed"
    
class PriorityEnum(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index= True, autoincrement=True)
    task_id = Column(String(40), default=lambda: str(uuid.uuid4()), index= True, nullable= False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="RESTRICT"), index= True, nullable= False)
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="RESTRICT"), index= True, nullable= False)
    task_type = Column(Enum(TaskTypeEnum), default= TaskTypeEnum.daily, nullable=False)
    priority = Column(Enum(PriorityEnum), default= PriorityEnum.high, nullable=False)
    due_date = Column(Date, index= True, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # creator = relationship("User")
    # assignments = relationship("TaskAssignment", back_populates="task", cascade="all, delete-orphan")
    # update_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)


class TaskAssignment(Base):
    __tablename__ = "task_assignments"

    id = Column(Integer, primary_key=True, index= True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    assigned_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    due_date = Column(Date, index= True, nullable=True)    
    status = Column(Enum(TaskStatusEnum), default=TaskStatusEnum.assigned, nullable= False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # report = relationship("Report", uselist=False, backref="task_assignment")
    # review = relationship("ReportReview", uselist=False, backref="task_assignment")
    # task = relationship("Task")
    
    


class Report(Base):
    __tablename__ = "reports"

    __table_args__ = (UniqueConstraint("assign_task_id", "user_id", name="uq_reports_assign_task_user"),)
    
    id = Column(Integer, primary_key=True, index= True, autoincrement=True)
    assign_task_id = Column(Integer, ForeignKey("task_assignments.id", ondelete="CASCADE"), index= True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index= True, nullable=False)
    submission_text = Column(Text, nullable=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now(), index= True, nullable=False)
    
    created_at = Column(DateTime(timezone=True), index= True, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # review = relationship("ReportReview", back_populates="report", uselist=False)


class ReportAttachment(Base):
    __tablename__ = "assign_task_attachments"

    id = Column(Integer, primary_key=True)
    assign_task_id = Column(Integer, ForeignKey("task_assignments.id", ondelete="CASCADE"), index= True, nullable=False)
    document_url = Column(Text, default=None, nullable=True)
    file_path = Column(Text, default=None, nullable=True)
    uploaded_by = Column(Integer, ForeignKey('users.id', ondelete="SET NULL"), index= True, nullable= True)
    created_at = Column(DateTime(timezone=True), index= True, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # report = relationship("Report", back_populates="attachments")



class ReportReview(Base):
    __tablename__ = "submitted_task_reviews"

    id = Column(Integer, primary_key=True)
    assign_task_id = Column(Integer, ForeignKey("task_assignments.id", ondelete="CASCADE"), index= True, nullable=False)
    reviewed_by = Column(Integer, ForeignKey("users.id", ondelete= "SET NULL"), index= True, nullable=False)
    reviewer_comment = Column(Text, nullable=False)
    reviewed_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), index= True, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # report = relationship("Report", back_populates="review")
