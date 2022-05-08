from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class TasksSchema(BaseModel):
    id: UUID
    title: str
    description: str
    completed: bool
    created_at: datetime


class TaskCompleteSchema(TasksSchema):
    completed_at: datetime


class NewTaskSchema(BaseModel):
    title: str = Field(..., max_length=225)
    description: str = Field(..., max_length=455)