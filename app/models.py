from sqlalchemy import Column, String, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from .database import Base
import enum
import uuid

class RoleEnum(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    user = "user"

class StatusEnum(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class PriorityEnum(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.user, nullable=False)
    is_active = Column(Boolean, default=True)

    tasks_created = relationship("Task", back_populates="creator", foreign_keys="Task.created_by_id")
    tasks_assigned = relationship("Task", back_populates="assignee", foreign_keys="Task.assigned_to_id")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    description = Column(String(1000))
    status = Column(Enum(StatusEnum), default=StatusEnum.pending)
    assigned_to_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    created_by_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    due_date = Column(DateTime)
    priority = Column(Enum(PriorityEnum), default=PriorityEnum.medium)

    assignee = relationship("User", foreign_keys=[assigned_to_id], back_populates="tasks_assigned")
    creator = relationship("User", foreign_keys=[created_by_id], back_populates="tasks_created")
