from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID
import enum

# ===================== Enums =====================

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

# ===================== User Schemas =====================

class UserBase(BaseModel):
    email: EmailStr
    role: RoleEnum = RoleEnum.user

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: UUID
    is_active: bool

    class Config:
        from_attributes = True

# ===================== Token Schema =====================

class Token(BaseModel):
    access_token: str
    token_type: str

# ===================== Task Schemas =====================

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: StatusEnum = StatusEnum.pending
    assigned_to_id: Optional[UUID] = None
    due_date: Optional[datetime] = None
    priority: PriorityEnum = PriorityEnum.medium

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: UUID
    created_by_id: UUID

    class Config:
        from_attributes = True
