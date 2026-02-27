from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Boolean, text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False, index= True)
    description = Column(Text, nullable= True)
    department_head_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index= True, nullable=True)
    is_active = Column(Boolean, server_default=text("true"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    users = relationship("User", back_populates="department", foreign_keys="User.department_id")
    projects = relationship("Project", back_populates="department")

    head = relationship("User", foreign_keys=[department_head_id])